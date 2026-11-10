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
    def test_cancer_notebook_pages(self):
        import sys
        sys.path.insert(0, str(ROOT / "site/_ext"))
        from mdas_notebooks import NOTEBOOKS
        previous = {"tutorials/kalecancer/live-coding": "index.html",
                    "tutorials/kalecancer/live-coding-survival": "live-coding.html"}
        next_page = {"tutorials/kalecancer/live-coding": "live-coding-survival.html"}
        for doc, (title, path) in NOTEBOOKS.items():
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
                self.assertEqual([tag for tag, _ in page.actions], ["a"])
                colab = path.replace(".ipynb", "_colab.ipynb")
                self.assertEqual(page.actions[0][1]["href"], "https://colab.research.google.com/github/pykale/mdas/blob/main/" + colab)
                self.assertNotIn("binder", html.lower())
                self.assertNotIn("thebe", html.lower())
                self.assertNotIn("mdas-interactive", html)
                self.assertEqual(len(page.help_links), 1)
                self.assertEqual(page.help_links[0]["href"], "../../docs/notebook-execution.html")
                self.assertEqual(page.help_links[0]["target"], "_blank")
                self.assertNotIn("mdas-tutorial-picker", html)
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

    def test_cardiac_tutorial_pages(self):
        """Colab only, each with its own title and sidebar entry, as the Cancer examples have."""
        import sys
        sys.path.insert(0, str(ROOT / "site/_ext"))
        from mdas_notebooks import CARDIAC_NOTEBOOKS
        labels = [label for label, _ in CARDIAC_NOTEBOOKS.values()]
        previous = {"tutorials/kalecardiac/cardiovae": "index.html",
                    "tutorials/kalecardiac/lsemvae": "cardiovae.html"}
        for doc, (label, path) in CARDIAC_NOTEBOOKS.items():
            with self.subTest(doc=doc):
                source = (ROOT / path).read_text(encoding="utf-8")
                original = json.loads(source)
                html_path = ROOT / "site/_build/html" / (doc + ".html")
                html = html_path.read_text(encoding="utf-8")
                page = Page(html_path)
                self.assertEqual((ROOT / "site/_staged" / (doc + ".ipynb")).read_bytes(), (ROOT / path).read_bytes())
                self.assertEqual(set(re.findall(r"<h1[^>]*>([^<]*)", html)), {label})
                # The sidebar switches tutorials, so there is no picker.
                self.assertEqual(page.options, [])
                self.assertNotIn("mdas-tutorial-select", html)
                self.assertNotIn("live-coding", doc)
                self.assertNotIn("live-coding", html.split('<article class="bd-article">')[1].split("</article>")[0])
                self.assertEqual([s.strip() for s in page.inputs], ["".join(c["source"]).strip() for c in original["cells"] if c["cell_type"] == "code"])
                # Google Colab is the only execution route: no Binder or Thebe anywhere.
                self.assertEqual([tag for tag, _ in page.actions], ["a"])
                self.assertEqual(page.actions[0][1]["href"], "https://colab.research.google.com/github/pykale/mdas/blob/main/" + path)
                self.assertNotIn("binder", html.lower())
                self.assertNotIn("thebe", html.lower())
                self.assertNotIn("binder", source.lower())
                self.assertNotIn("mdas-interactive", html)
                self.assertEqual(len(page.help_links), 1)
                self.assertEqual(page.help_links[0]["href"], "../../docs/notebook-execution.html#cardiac-setup")
                self.assertRegex(html, r'class="left-prev"\s+href="' + re.escape(previous[doc]) + '"')
                sidebar = html.split('<div class="bd-toc-item navbar-nav active">')[1].split('</nav>')[0]
                entries = re.findall(r'<li class="toctree-l(\d)[^"]*"><a class="[^"]*reference internal" href="[^"]*">([^<]+)</a>', sidebar)
                start = entries.index(("1", "Cardiac Overview"))
                self.assertEqual(entries[start:], [("1", "Cardiac Overview")] + [("2", title) for title in labels])
                current = re.findall(r'<li class="toctree-l2 current active"><a class="[^"]*reference internal" href="[^"]*">([^<]+)</a>', sidebar)
                self.assertEqual(current, [label])
                # The notebook ends with its own references, which the summary's [1] links to.
                self.assertNotIn('id="interpretation-and-next-steps"', html)
                self.assertIn('id="references"', html)
                self.assertIn('href="#references">[1]</a>', html)
                toc = html.split('id="pst-secondary-sidebar"')[1]
                for anchor in re.findall(r'<section id="([^"]+)"', html):
                    self.assertIn(f'href="#{anchor}"', toc)

if __name__ == "__main__":
    unittest.main()
