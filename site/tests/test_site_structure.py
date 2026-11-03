"""Generated public identity, navigation and help checks; run after an enabled build."""
from html import unescape
from pathlib import Path
import json
import re
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[2]
HTML = ROOT / "site/_build/html"


def page(doc):
    return (HTML / (doc + ".html")).read_text(encoding="utf-8")


class SiteStructure(unittest.TestCase):
    def test_navigation_has_only_the_requested_entries(self):
        navigation = json.loads((ROOT / "site/navigation.json").read_text(encoding="utf-8"))
        self.assertEqual(navigation["Getting Started"], [["Quick Start", "docs/quick-start"]])
        self.assertEqual([title for title, _ in navigation["About the Session"]], ["What is MDAS?", "Session Agenda", "Participation Guide"])
        self.assertEqual(navigation["Tutorials"], [["Cancer", "tutorials/kalecancer/index"], ["Cardiac", "tutorials/kalecardiac/index"]])
        staged = (ROOT / "site/_staged/tutorials/kalecancer/index.md").read_text(encoding="utf-8")
        self.assertIn("Live-Coding Notebook <live-coding>", staged)
        self.assertNotIn("hands-on", staged)
        self.assertNotIn("Getting Started <getting-started>", staged)
        self.assertIn("# Cancer", staged)
        for term in ("Classification: predict a category", "Survival Analysis: predict relative event risk", "ABMIL", "Cox head"):
            self.assertIn(term, staged)
        for doc in ("index", "tutorials/kalecancer/live-coding", "tutorials/kalecancer/live-coding-survival", "tutorials/kalecardiac/cardiovae-hands-on"):
            sidebar = page(doc).split('<div class="bd-toc-item navbar-nav active">')[1].split('</nav>')[0]
            for removed in ("Tutorials Overview", "Prerequisites", "Hands-on Tutorial"):
                self.assertNotIn(removed, sidebar)

    def test_legacy_urls_are_redirects_and_retired_content_is_not_staged(self):
        for old, target in (("docs/prerequisites", "participation.html"), ("tutorials/README", "../index.html#explore-the-examples"), ("tutorials/kalecancer/hands-on", "live-coding.html"), ("tutorials/kalecancer/getting-started", "index.html"), ("tutorials/kalecancer/README", "index.html")):
            html = page(old)
            self.assertIn('name="robots" content="noindex"', html)
            self.assertIn(f'url={target}', html)
            self.assertIn(f'href="{target}"', html)
            self.assertFalse((ROOT / "site/_staged" / (old + ".md")).exists())
        # Internal links should go straight to the consolidated page.
        for doc in ("index", "docs/about", "docs/participation", "docs/quick-start", "docs/agenda", "tutorials/kalecancer/index", "tutorials/kalecancer/results"):
            links = re.findall(r'href="([^"#]+)', page(doc))
            for link in links:
                self.assertNotIn(link.rsplit("/", 1)[-1], ("prerequisites.html", "hands-on.html"), link)
                self.assertFalse(link.endswith("tutorials/README.html"), link)

    def test_public_identity_and_simple_homepage(self):
        for path in HTML.rglob("*"):
            if path.is_file() and path.suffix in {".html", ".js", ".css", ".json"}:
                text = unescape(path.read_text(encoding="utf-8"))
                self.assertNotIn("MDAS 1.0", text, str(path))
                self.assertNotIn("mdas-learning-journey", text, str(path))
                self.assertNotIn("mdas-track-card", text, str(path))
        self.assertFalse((ROOT / "site/_ext/mdas_journey.py").exists())
        home = page("index")
        self.assertIn("Multimodal Data Analysis Session (MDAS)", home)
        self.assertIn("Explore Cancer", home)
        self.assertIn("Explore Cardiac", home)
        self.assertIn('href="tutorials/kalecancer/index.html"', home)
        self.assertIn('href="tutorials/kalecardiac/getting-started.html"', home)
        self.assertIn("18 November 2026", home)
        self.assertIn("13:00" + chr(8211) + "17:00", unescape(home))
        for venue in ("Regent Court", "The Diamond", "Workroom 3 (Room 205)"):
            self.assertIn(venue, home)
        self.assertIn('_static/mdas-logo.png', home)

    def test_cancer_is_the_substantive_landing_page(self):
        html = page("tutorials/kalecancer/index")
        self.assertIn('<h1>Cancer', html)
        for term in ("Classification: predict a category", "Survival Analysis: predict relative event risk", "ABMIL", "Cox head"):
            self.assertIn(term, html)
        sidebar = html.split('<div class="bd-toc-item navbar-nav active">')[1].split('</nav>')[0]
        self.assertNotIn('kalecancer/getting-started.html', sidebar)
        self.assertNotIn('href="getting-started.html"', sidebar)
        self.assertIn('href="live-coding.html"', html)

    def test_actual_notebook_metrics_and_prediction_types_are_explained_separately(self):
        html = page("tutorials/kalecancer/results")
        classification = html.split('id="classification-results-and-interpretation"')[1].split('id="survival-analysis-results-and-interpretation"')[0]
        survival = html.split('id="survival-analysis-results-and-interpretation"')[1]
        for term in ("probability[early]", "probability[late]", "AUROC", "Balanced accuracy"):
            self.assertIn(term, classification)
        for term in ("log_hazard", "Harrell", "Uno", "1825.0", "censor"):
            self.assertIn(term, survival)
        self.assertNotIn("Uno", classification)
        for name in ("classification", "survival"):
            source = json.loads((ROOT / f"notebooks/MDAS/cancer/{name}.ipynb").read_text(encoding="utf-8"))
            code = "\n".join("".join(c["source"]) for c in source["cells"] if c["cell_type"] == "code")
            for expected in (("AUROC(positive_class='late')", "BalancedAccuracy()") if name == "classification" else ("HarrellC()", "UnoC(tau=1825.0)")):
                self.assertIn(expected, code)

    def test_help_is_secondary_top_right_and_not_hidden_in_presentation(self):
        css = (ROOT / "site/_static/mdas-notebooks.css").read_text(encoding="utf-8")
        self.assertIn('.mdas-notebook-tools { display: flex; justify-content: flex-end;', css)
        self.assertIn('.mdas-execution-help:focus-visible', css)
        self.assertIn('min-height: 44px', css)
        for doc in ("tutorials/kalecancer/live-coding", "tutorials/kalecancer/live-coding-survival"):
            html = page(doc)
            help_tag = re.search(r'<a class="mdas-execution-help"[^>]+>', html)[0]
            self.assertNotIn("btn-primary", help_tag)
            self.assertIn('target="_blank"', help_tag)
            self.assertIn('rel="noopener"', help_tag)
            self.assertIn('aria-label="Execution Help (opens in a new tab)"', help_tag)
            self.assertIn('<svg class="mdas-help-icon" aria-hidden="true" focusable="false"', html)
            self.assertIn('stroke="currentColor"', html)
            self.assertNotIn('>?</span>', html)
            self.assertIn('interpret the Cancer results', html)
            self.assertIn('href="results.html"', html)
        presentation_css = (ROOT / "site/_static/mdas.css").read_text(encoding="utf-8")
        self.assertNotIn("mdas-notebook-tools", presentation_css)
        self.assertNotIn("mdas-execution-help", presentation_css)

    def test_local_setup_commands_and_event_programme_are_preserved(self):
        for path in ("docs/quick-start.md", "docs/agenda.md"):
            old = subprocess.check_output(["git", "show", f"HEAD:{path}"], cwd=ROOT).decode("utf-8-sig")
            new = (ROOT / path).read_text(encoding="utf-8-sig")
            if path.endswith("quick-start.md"):
                self.assertEqual(re.findall(r"```sh\n(.*?)```", old, re.S), re.findall(r"```sh\n(.*?)```", new, re.S))
            else:
                self.assertEqual([line for line in old.splitlines() if line.startswith('|')], [line for line in new.splitlines() if line.startswith('|')])
                self.assertEqual(old.split('## Programme')[0], new.split('## Programme')[0])
                self.assertNotIn("[Prerequisites]", new)


if __name__ == "__main__":
    unittest.main()
