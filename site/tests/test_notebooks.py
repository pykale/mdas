"""Regression checks against a fresh Sphinx build (no external dependencies)."""
import json
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.scripts = {}
        self.options = []
        self.actions = []
        self.help_links = []
        self.inputs = []
        self.depth = 0
        self.input_depth = None
        self.script = None
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "div":
            self.depth += 1
            if "cell_input" in attrs.get("class", "").split():
                self.input_depth = self.depth
                self.inputs.append("")
        if "mdas-execution-button" in attrs.get("class", "").split():
            self.actions.append((tag, attrs))
        if "mdas-execution-help" in attrs.get("class", "").split():
            self.help_links.append(attrs)
        if tag == "option":
            self.options.append(attrs)
        if tag == "script":
            self.script = attrs.get("id") or attrs.get("type")
            self.scripts[self.script] = ""

    def handle_endtag(self, tag):
        if tag == "div":
            if self.depth == self.input_depth:
                self.input_depth = None
            self.depth -= 1
        if tag == "script":
            self.script = None

    def handle_data(self, data):
        if self.script:
            self.scripts[self.script] += data
        elif self.input_depth is not None:
            self.inputs[-1] += data

class Notebooks(unittest.TestCase):
    def test_generated_notebooks(self):
        for name, page_name in (("classification_showcase", "live-coding"), ("survival", "live-coding-survival")):
            with self.subTest(name=name):
                path = f"notebooks/MDAS/cancer/{name}.ipynb"
                original = json.loads((ROOT / path).read_text(encoding="utf-8"))
                html_path = ROOT / f"site/_build/html/tutorials/kalecancer/{page_name}.html"
                html = html_path.read_text(encoding="utf-8")
                page = Page(html_path)
                self.assertIn('<h1>Live-Coding Notebook', html)
                self.assertIn('id="live-coding-notebook"', html)
                self.assertEqual((ROOT / f"site/_staged/tutorials/kalecancer/{page_name}.ipynb").read_bytes(), (ROOT / path).read_bytes())
                self.assertEqual([x["value"] for x in page.options], ["live-coding.html", "live-coding-survival.html"])
                self.assertEqual([x["value"] for x in page.options if "selected" in x], [page_name + ".html"])
                self.assertEqual([s.strip() for s in page.inputs], ["".join(c["source"]).strip() for c in original["cells"] if c["cell_type"] == "code"])
                self.assertNotIn("mdas-notebook-source", page.scripts)
                self.assertNotIn("mdasDownloadNotebook", html)
                self.assertNotIn("Download notebook with edits", html)
                self.assertNotIn("_blank.ipynb", html)
                self.assertNotIn("Optional blank exercise", html)
                self.assertEqual(len(page.help_links), 1)
                help_link = page.help_links[0]
                self.assertEqual(help_link["href"], "../../docs/notebook-execution.html")
                self.assertEqual(help_link["target"], "_blank")
                self.assertIn("noopener", help_link["rel"])
                self.assertEqual(help_link["aria-label"], "Execution Help (opens in a new tab)")
                self.assertLess(html.index('class="mdas-notebook-tools"'), html.index('id="mdas-notebook-select"'))
                self.assertIn('class="mdas-help-icon" aria-hidden="true"', html)
                self.assertNotIn("mdas-learning-journey", html)
                self.assertIn('<svg class="mdas-help-icon" aria-hidden="true" focusable="false"', html)
                self.assertRegex(html, r'class="left-prev"\s+href="index.html"')
                self.assertRegex(html, r'class="right-next"\s+href="results.html"')
                colab_path = path.replace(".ipynb", "_colab.ipynb")
                if name == "classification_showcase":
                    self.assertNotIn('href="https://colab.research.google.com/github/', html)
                    self.assertIn('disabled aria-describedby="mdas-showcase-blocker"', html)
                    self.assertIn("Showcase execution setup pending", html)
                    required = json.loads(page.scripts["mdas-binder-check"])["required_files"]
                    self.assertIn("notebooks/MDAS/cancer/synthetic_showcase_data.py", required)
                    self.assertIn("notebooks/MDAS/cancer/synthetic_data_generation.py", required)
                else:
                    self.assertIn(f'href="https://colab.research.google.com/github/pykale/mdas/blob/main/{colab_path}"', html)
                self.assertEqual(len(page.actions), 2)
                self.assertEqual([tag for tag, _ in page.actions], ["button", "button"] if name == "classification_showcase" else ["button", "a"])
                self.assertEqual(page.actions[0][1]["onclick"], "mdasLaunchInteractive()")
                self.assertIn('>Run with Binder</button>', html)
                self.assertIn('>Google Colab unavailable</button>' if name == 'classification_showcase' else '>Run in Google Colab</a>', html)
                self.assertNotIn('Prepare Colab Environment', html)
                self.assertNotIn('prepare_colab.ipynb', html)
                config = json.loads(page.scripts["text/x-thebe-config"])
                self.assertEqual(config["kernelOptions"]["path"], "notebooks/MDAS/cancer")
                self.assertFalse(config["bootstrap"])
                self.assertIn(path, json.loads(page.scripts["mdas-binder-check"])["required_files"])
                sidebar = html.split('<div class="bd-toc-item navbar-nav active">')[1].split('</nav>')[0]
                entries = re.findall(r'<a class="[^"]*reference internal" href="([^"]*)">Example Notebook</a>', sidebar)
                # One Cancer entry (Survival adds none), plus the separate Cardiac track's entry.
                self.assertEqual(len([href for href in entries if "kalecardiac/" not in href]), 1)
                self.assertEqual(len([href for href in entries if "kalecardiac/" in href]), 1)
                self.assertIn('current active', sidebar)
                self.assertIn('mdas-presentation.js', html)
                toc = html.split('id="pst-secondary-sidebar"')[1]
                # Every rendered section must have a matching local ToC link.
                for anchor in re.findall(r'<section id="([^"]+)"', html):
                    self.assertIn(f'href="#{anchor}"', toc)

    def test_generated_cardiac_notebooks(self):
        """Cardiac pages: tutorial selector, unchanged code, and Binder/Colab actions in the notebook's folder."""
        for name, page_name in (("tutorial-CardioVAE", "live-coding"), ("tutorial-LSEMVAE", "live-coding-lsemvae")):
            with self.subTest(name=name):
                path = f"notebooks/MDAS/cardiac/{name}.ipynb"
                original = json.loads((ROOT / path).read_text(encoding="utf-8"))
                html_path = ROOT / f"site/_build/html/tutorials/kalecardiac/{page_name}.html"
                html = html_path.read_text(encoding="utf-8")
                page = Page(html_path)
                self.assertEqual((ROOT / f"site/_staged/tutorials/kalecardiac/{page_name}.ipynb").read_bytes(), (ROOT / path).read_bytes())
                self.assertIn('<h1>Live-Coding Notebook', html)
                self.assertIn('<label for="mdas-notebook-select">Choose a tutorial</label>', html)
                self.assertEqual([(x["value"], html.split(f'value="{x["value"]}"')[1].split(">")[1].split("<")[0]) for x in page.options],
                                 [("live-coding.html", "CardioVAE"), ("live-coding-lsemvae.html", "LS-EMVAE")])
                self.assertEqual([x["value"] for x in page.options if "selected" in x], [page_name + ".html"])
                self.assertEqual([s.strip() for s in page.inputs], ["".join(c["source"]).strip() for c in original["cells"] if c["cell_type"] == "code"])
                # The notebook supplies no title of its own (the page title comes first) and no Colab badge.
                self.assertEqual(set(re.findall(r"<h1[^>]*>([^<]*)", html)), {"Live-Coding Notebook"})
                article = html.split('<article class="bd-article">')[1].split('</article>')[0]
                self.assertEqual(re.findall(r"<h2>([^<]*)", article)[0], "Step 0: Environment Preparation")
                self.assertNotIn("Cardiac Abnormality Assessment", html)
                self.assertNotIn("colab-badge", html)
                # Binder and Colab, as on the Cancer pages; no Cancer-only Execution Help.
                self.assertEqual([tag for tag, _ in page.actions], ["button", "a"])
                self.assertEqual(page.actions[0][1]["onclick"], "mdasLaunchInteractive()")
                self.assertIn('>Run with Binder</button>', html)
                self.assertIn(f'href="https://colab.research.google.com/github/pykale/mdas/blob/main/{path}">Run in Google Colab</a>', html)
                self.assertIn('id="mdas-thebe-status"', html)
                self.assertIn('mdas-interactive.js', html)
                self.assertEqual(page.help_links, [])
                self.assertNotIn("notebook-execution.html", html)
                config = json.loads(page.scripts["text/x-thebe-config"])
                self.assertEqual(config["kernelOptions"]["path"], "notebooks/MDAS/cardiac")
                self.assertFalse(config["bootstrap"])
                self.assertEqual(config["binderOptions"]["repo"], "pykale/mdas")
                model = "cardiovae" if name.endswith("CardioVAE") else "lsemvae"
                required = json.loads(page.scripts["mdas-binder-check"])["required_files"]
                self.assertEqual(required, [".binder/runtime.txt", ".binder/requirements.txt", path,
                                            f"notebooks/MDAS/cardiac/configs/config_{model}_pretrain.yaml",
                                            f"notebooks/MDAS/cardiac/configs/config_{model}_finetune.yaml"])
                for required_file in required:
                    self.assertTrue((ROOT / required_file).is_file(), required_file)
                self.assertIn('href="getting-started.html#run-a-tutorial"', html)
                self.assertIn('mdas-notebooks.js', html)
                self.assertRegex(html, r'class="left-prev"\s+href="getting-started.html"')
                sidebar = html.split('<div class="bd-toc-item navbar-nav active">')[1].split('</nav>')[0]
                current = re.findall(r'<li class="toctree-l2 current active"><a class="current reference internal" href="[^"]*">([^<]+)</a>', sidebar)
                self.assertEqual(current, ["Example Notebook"])
                for removed in ("CardioVAE Hands-on", "LS-EMVAE Hands-on", "kalecardiac/results.html", 'href="results.html"'):
                    self.assertNotIn(removed, sidebar)
                toc = html.split('id="pst-secondary-sidebar"')[1]
                for anchor in re.findall(r'<section id="([^"]+)"', html):
                    self.assertIn(f'href="#{anchor}"', toc)

if __name__ == "__main__":
    unittest.main()
