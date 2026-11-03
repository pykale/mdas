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
        for name, page_name in (("classification", "live-coding"), ("survival", "live-coding-survival")):
            with self.subTest(name=name):
                path = f"notebooks/MDAS/cancer/{name}.ipynb"
                original = json.loads((ROOT / path).read_text(encoding="utf-8"))
                html_path = ROOT / f"site/_build/html/tutorials/kalecancer/{page_name}.html"
                html = html_path.read_text(encoding="utf-8")
                page = Page(html_path)
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
                self.assertIn(f'href="https://colab.research.google.com/github/pykale/mdas/blob/main/{colab_path}"', html)
                self.assertEqual(len(page.actions), 2)
                self.assertEqual([tag for tag, _ in page.actions], ["button", "a"])
                self.assertEqual(page.actions[0][1]["onclick"], "mdasLaunchInteractive()")
                self.assertIn('>Run with Binder</button>', html)
                self.assertIn('>Run in Google Colab</a>', html)
                self.assertNotIn('Prepare Colab Environment', html)
                self.assertNotIn('prepare_colab.ipynb', html)
                config = json.loads(page.scripts["text/x-thebe-config"])
                self.assertEqual(config["kernelOptions"]["path"], "notebooks/MDAS/cancer")
                self.assertFalse(config["bootstrap"])
                self.assertIn(path, json.loads(page.scripts["mdas-binder-check"])["required_files"])
                sidebar = html.split('<div class="bd-toc-item navbar-nav active">')[1].split('</nav>')[0]
                self.assertEqual(sidebar.count('>Live-Coding Notebook</a>'), 1)
                self.assertIn('current active', sidebar)
                self.assertIn('mdas-presentation.js', html)
                toc = html.split('id="pst-secondary-sidebar"')[1]
                # Every rendered section must have a matching local ToC link.
                for anchor in re.findall(r'<section id="([^"]+)"', html):
                    self.assertIn(f'href="#{anchor}"', toc)

if __name__ == "__main__":
    unittest.main()
