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
    def test_four_independent_notebook_pages(self):
        import sys
        sys.path.insert(0, str(ROOT / "site/_ext"))
        from mdas_notebooks import ALL_NOTEBOOKS
        previous = {"tutorials/kalecancer/live-coding": "index.html",
                    "tutorials/kalecancer/live-coding-survival": "live-coding.html",
                    "tutorials/kalecardiac/live-coding": "index.html",
                    "tutorials/kalecardiac/live-coding-lsemvae": "live-coding.html"}
        next_page = {"tutorials/kalecancer/live-coding": "live-coding-survival.html",
                     "tutorials/kalecardiac/live-coding": "live-coding-lsemvae.html"}
        for doc, (title, path) in ALL_NOTEBOOKS.items():
            with self.subTest(doc=doc):
                original = json.loads((ROOT / path).read_text(encoding="utf-8"))
                html_path = ROOT / "site/_build/html" / (doc + ".html")
                html = html_path.read_text(encoding="utf-8")
                page = Page(html_path)
                self.assertEqual((ROOT / "site/_staged" / (doc + ".ipynb")).read_bytes(), (ROOT / path).read_bytes())
                self.assertEqual(set(re.findall(r"<h1[^>]*>([^<]*)", html)), {title})
                self.assertEqual(page.options, [])
                self.assertNotIn("mdas-notebook-select", html)
                self.assertNotIn("Live-Coding Notebook", html)
                self.assertNotIn('class="headerlink"', html)
                self.assertEqual([s.strip() for s in page.inputs], ["".join(c["source"]).strip() for c in original["cells"] if c["cell_type"] == "code"])
                self.assertEqual([tag for tag, _ in page.actions], ["button", "a"])
                self.assertEqual(page.actions[0][1]["onclick"], "mdasLaunchInteractive()")
                cardiac = "kalecardiac" in doc
                colab = path if cardiac else path.replace(".ipynb", "_colab.ipynb")
                self.assertEqual(page.actions[1][1]["href"], "https://colab.research.google.com/github/pykale/mdas/blob/main/" + colab)
                self.assertEqual(len(page.help_links), 1)
                self.assertEqual(page.help_links[0]["href"], "../../docs/notebook-execution.html" + ("#cardiac-setup" if cardiac else ""))
                self.assertEqual(page.help_links[0]["target"], "_blank")
                config = json.loads(page.scripts["text/x-thebe-config"])
                self.assertFalse(config["bootstrap"])
                self.assertEqual(config["kernelOptions"]["path"], "notebooks/MDAS/" + ("cardiac" if cardiac else "cancer"))
                required = json.loads(page.scripts["mdas-binder-check"])["required_files"]
                self.assertIn(path, required)
                for file in required:
                    self.assertTrue((ROOT / file).is_file(), file)
                if not cardiac:
                    self.assertIn("notebooks/MDAS/cancer/synthetic_showcase_data.py", required)
                self.assertRegex(html, r'class="left-prev"\s+href="' + re.escape(previous[doc]) + '"')
                if doc in next_page:
                    self.assertRegex(html, r'class="right-next"\s+href="' + re.escape(next_page[doc]) + '"')
                sidebar = html.split('<div class="bd-toc-item navbar-nav active">')[1].split('</nav>')[0]
                current = re.findall(r'<li class="toctree-l2 current active"><a class="current reference internal" href="[^"]*">([^<]+)</a>', sidebar)
                self.assertEqual(current, [title])
                self.assertNotIn('>Example Notebook</a>', sidebar)
                self.assertIn("mdas-presentation.js", html)
                self.assertIn("mdas-notebooks.js", html)
                self.assertIn('id="interpretation-and-next-steps"', html)
                toc = html.split('id="pst-secondary-sidebar"')[1]
                for anchor in re.findall(r'<section id="([^"]+)"', html):
                    self.assertIn(f'href="#{anchor}"', toc)

if __name__ == "__main__":
    unittest.main()
