"""Source/staging checks without invoking Sphinx or executing scientific notebooks."""
import importlib.util
import json
from pathlib import Path
import re
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded

class RestructureSource(unittest.TestCase):
    def test_staged_toctrees_assets_aliases_and_sources(self):
        build = module("mdas_build_source_test", ROOT / "site/build.py")
        conf = module("mdas_conf_source_test", ROOT / "site/conf.py")
        self.assertFalse(conf.html_permalinks)
        self.assertTrue(conf.nitpicky)
        with tempfile.TemporaryDirectory() as folder:
            build.STAGED = Path(folder) / "source"
            build.stage()
            for track, entries in (("kalecancer", ["Classification <live-coding>", "Survival Analysis <live-coding-survival>"]),
                                   ("kalecardiac", ["Chest X-ray and ECG <chest-xray-ecg>", "12-lead ECG <12-lead-ecg>"])):
                text = (build.STAGED / f"tutorials/{track}/index.md").read_text(encoding="utf-8")
                for entry in entries:
                    self.assertIn(entry, text)
                for old in ("getting-started", "results", "Example Notebook"):
                    self.assertNotIn(old + " <", text)
                self.assertFalse((build.STAGED / f"tutorials/{track}/results.md").exists())
            self.assertFalse((build.STAGED / "tutorials/kalecardiac/getting-started.md").exists())
            self.assertEqual((build.STAGED / "assets/kalecancer-fusion-workflow.svg").read_bytes(), (ROOT / "assets/kalecancer-fusion-workflow.svg").read_bytes())
            for doc, (title, path) in {**conf.NOTEBOOKS, **conf.CARDIAC_NOTEBOOKS}.items():
                self.assertEqual((build.STAGED / (doc + ".ipynb")).read_bytes(), (ROOT / path).read_bytes())
                source = [json.dumps(json.loads((ROOT / path).read_text()))]
                conf.prepare_notebook(None, doc, source)
                rendered = json.loads(source[0])
                intro = rendered["cells"][0]["source"]
                self.assertIn("# " + title, intro)  # every example, Cancer or Cardiac, has its own title
                self.assertNotIn("mdas-notebook-select", intro)
                self.assertNotIn("Live-Coding Notebook", intro)
                self.assertNotIn("orphan", rendered.get("metadata", {}))
                # Cancer pages close with guidance; Cardiac notebooks end with their own references.
                closing = self.assertIn if doc in conf.NOTEBOOKS else self.assertNotIn
                closing("## Interpretation and next steps", rendered["cells"][-1]["source"])
            for old in ("tutorials/kalecardiac/getting-started", "tutorials/kalecancer/results", "tutorials/kalecardiac/results"):
                self.assertIn(old, conf.REDIRECTS)
            self.assertFalse((build.STAGED / "docs/agenda.md").exists())
            self.assertEqual(conf.REDIRECTS["docs/agenda"], "about.html#programme")
            self.assertIn("## Programme", (build.STAGED / "docs/about.md").read_text())
            quick = (build.STAGED / "docs/quick-start.md").read_text()
            for track, pages in (("kalecancer", ("live-coding", "live-coding-survival")),
                                 ("kalecardiac", ("chest-xray-ecg", "12-lead-ecg"))):
                for page in pages:
                    self.assertIn(f"../tutorials/{track}/{page}.ipynb", quick)

    def test_about_consolidates_session_and_programme(self):
        text = (ROOT / "docs/about.md").read_text(encoding="utf-8")
        self.assertEqual(re.findall(r"^#{1,2} .+$", text, re.M),
                         ["# What is MDAS?", "## Session details", "## Programme"])
        self.assertEqual(text.count("Wednesday, 18 November 2026"), 1)
        self.assertEqual(text.count("13:00–17:00"), 1)
        self.assertEqual(text.count("Ada Lovelace Room (108), Level 1, Regent Court, University of Sheffield"), 1)
        self.assertEqual(text.count("](participation.md)"), 1)
        expected = [
            "| Time | Activity |", "| --- | --- |",
            "| 13:00–14:00 | **Block 1: Learn the Pipeline** |",
            "| 13:00–13:05 | Introductions and session outline |",
            "| 13:05–13:10 | Environment setup |",
            "| 13:10–13:50 | Core content: from data loading to model evaluation |",
            "| 13:50–14:00 | Discussion |",
            "| 14:00–14:10 | Break and refreshments |",
            "| 14:10–16:30 | **Block 2: Apply the Pipeline** |",
            "| 14:10–16:20 | Work on your own research question with support from the AIRE team. |",
            "| 16:20–16:30 | Closing remarks |",
        ]
        self.assertEqual([line for line in text.splitlines() if line.startswith("|")], expected)
        navigation = json.loads((ROOT / "site/navigation.json").read_text())
        self.assertEqual(navigation["About the Session"],
                         [["What is MDAS?", "docs/about"], ["Participation Guide", "docs/participation"]])
        self.assertIn("../tutorials/kalecancer/index.md", text)
        self.assertIn("../tutorials/kalecardiac/index.md", text)
        self.assertNotIn("Fusion approach", text)
        self.assertNotIn("agenda.md", (ROOT / "docs/participation.md").read_text())

    def test_disabled_binder_build_has_accurate_page_actions(self):
        import os
        from unittest.mock import patch
        with patch.dict(os.environ, {"MDAS_ENABLE_THEBE": "0"}):
            conf = module("mdas_disabled_source_test", ROOT / "site/conf.py")
        self.assertFalse(conf.MDAS_ENABLE_THEBE)
        for doc in {**conf.NOTEBOOKS, **conf.CARDIAC_NOTEBOOKS}:
            intro = conf.notebook_intro(doc)
            self.assertNotIn("Binder", intro)
            self.assertNotIn('onclick="mdasLaunchInteractive()"', intro)
            self.assertIn("Run in Google Colab", intro)

    def test_cancer_colab_only_actions_and_guidance(self):
        conf = module("mdas_colab_only_source_test", ROOT / "site/conf.py")
        self.assertEqual([title for title, _ in conf.NOTEBOOKS.values()],
                         ["Classification", "Survival Analysis"])
        navigation = json.loads((ROOT / "site/navigation.json").read_text())
        self.assertIn(["Cancer Overview", "tutorials/kalecancer/index"], navigation["Tutorials"])
        home = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("[Cancer](tutorials/kalecancer/index.md)", home)
        for path in ("README.md", "docs/quick-start.md", "docs/colab.md", "tutorials/kalecancer/index.md"):
            text = (ROOT / path).read_text(encoding="utf-8")
            self.assertNotIn("KaleCancer Classification", text)
            self.assertNotIn("KaleCancer Survival Analysis", text)
        self.assertEqual(conf.mdas_binder_pages, [])
        for doc, (_, path) in conf.NOTEBOOKS.items():
            intro = conf.notebook_intro(doc)
            self.assertNotIn("Binder", intro)
            self.assertNotIn("mdas-thebe", intro)
            self.assertEqual(intro.count('class="btn btn-primary mdas-execution-button"'), 1)
            self.assertIn(path.replace(".ipynb", "_colab.ipynb"), intro)
            self.assertTrue((ROOT / path.replace(".ipynb", "_colab.ipynb")).is_file())
            self.assertIn("Python 3.12 / 2026.07", intro)
            self.assertIn("quick-start.md#cancer", intro)
            self.assertIn("Do not upload private or patient data", intro)
        for path in ("README.md", "docs/quick-start.md", "docs/notebook-execution.md", "docs/colab.md", "tutorials/kalecancer/index.md"):
            self.assertNotIn("Run with Binder", (ROOT / path).read_text(encoding="utf-8"))
        overview = (ROOT / "tutorials/kalecancer/index.md").read_text(encoding="utf-8")
        self.assertIn("## What you will do", overview)
        self.assertEqual(len(re.findall(r"^[1-4]\. ", overview, re.M)), 4)

    def test_parallel_routes_and_preserved_local_commands(self):
        text = (ROOT / "docs/quick-start.md").read_text()
        self.assertEqual(text.count("### Run online"), 2)
        self.assertEqual(text.count("### Run locally"), 2)
        for command in ("uv sync --all-extras", "uv run python examples/synthetic/synthetic_survival.py", "git clone https://github.com/pykale/cardiac.git", "pip install -e .", 'pip install -e ".[imaging,interpret]"', "python -m examples.cardiovae_multimodal.main --cfg examples/cardiovae_multimodal/configs/quick.yaml", "python -m examples.lsemvae_ecg.main --cfg examples/lsemvae_ecg/configs/quick.yaml"):
            self.assertIn(command, text)
        self.assertNotIn("Choose an execution route", (ROOT / "docs/participation.md").read_text())
        self.assertNotIn("SECONDARY_NOTEBOOKS", (ROOT / "site/conf.py").read_text())

    def test_figure_flow_is_additive_accessible_and_reducible(self):
        figure = ROOT / "assets/kalecancer-fusion-workflow.svg"
        root = ET.parse(figure).getroot()
        self.assertEqual(root.get("viewBox"), "0 0 642 332")
        self.assertEqual(root.get("role"), "img")
        paths = [el for el in root.iter() if el.get("class") == "mdas-flow"]
        self.assertEqual(len(paths), 6)
        originals = {el.get("d") for el in root.iter() if el.tag.endswith("path") and not el.get("class")}
        self.assertTrue(all(el.get("d") in originals for el in paths))
        text = figure.read_text()
        self.assertIn("prefers-reduced-motion: reduce", text)
        self.assertIn("animation:none !important; display:none", text)
        self.assertIn("mdas-cancer-figure-description", root.get("aria-labelledby"))
        self.assertTrue(all("opacity:0" in el.get("style") for el in paths))

if __name__ == "__main__":
    unittest.main()
