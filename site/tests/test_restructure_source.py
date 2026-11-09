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
            for track, titles in (("kalecancer", ["KaleCancer Classification", "KaleCancer Survival Analysis"]),
                                  ("kalecardiac", ["KaleCardiac CardioVAE", "KaleCardiac LS-EMVAE"])):
                text = (build.STAGED / f"tutorials/{track}/index.md").read_text()
                for title in titles:
                    self.assertIn(title + " <live-coding", text)
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
                self.assertIn("# " + title, intro)
                self.assertNotIn("mdas-notebook-select", intro)
                self.assertNotIn("Live-Coding Notebook", intro)
                self.assertNotIn("orphan", rendered.get("metadata", {}))
                self.assertIn("## Interpretation and next steps", rendered["cells"][-1]["source"])
            for old in ("tutorials/kalecardiac/getting-started", "tutorials/kalecancer/results", "tutorials/kalecardiac/results"):
                self.assertIn(old, conf.REDIRECTS)
            quick = (build.STAGED / "docs/quick-start.md").read_text()
            for track, suffix in (("kalecancer", "survival"), ("kalecardiac", "lsemvae")):
                self.assertIn(f"../tutorials/{track}/live-coding.ipynb", quick)
                self.assertIn(f"../tutorials/{track}/live-coding-{suffix}.ipynb", quick)

    def test_disabled_binder_build_has_accurate_page_actions(self):
        import os
        from unittest.mock import patch
        with patch.dict(os.environ, {"MDAS_ENABLE_THEBE": "0"}):
            conf = module("mdas_disabled_source_test", ROOT / "site/conf.py")
        self.assertFalse(conf.MDAS_ENABLE_THEBE)
        for doc in {**conf.NOTEBOOKS, **conf.CARDIAC_NOTEBOOKS}:
            intro = conf.notebook_intro(doc)
            self.assertIn("In-page execution is disabled", intro)
            self.assertNotIn('onclick="mdasLaunchInteractive()"', intro)
            self.assertIn("Run in Google Colab", intro)

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
