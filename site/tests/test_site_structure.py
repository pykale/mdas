"""Generated navigation and public-copy checks; run after a fresh enabled Sphinx build."""
from html import unescape
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
HTML = ROOT / "site/_build/html"

def page(doc):
    return (HTML / (doc + ".html")).read_text(encoding="utf-8")

def plain(html):
    return " ".join(re.sub(r"<[^>]+>", " ", unescape(html)).split())

class SiteStructure(unittest.TestCase):
    def test_navigation_has_two_examples_per_overview(self):
        navigation = json.loads((ROOT / "site/navigation.json").read_text())
        self.assertEqual(navigation["About the Session"], [["What is MDAS?", "docs/about"], ["Participation Guide", "docs/participation"]])
        self.assertEqual(navigation["Tutorials"], [["Cancer", "tutorials/kalecancer/index"], ["Cardiac", "tutorials/kalecardiac/index"]])
        for track, entries in (("kalecancer", ["KaleCancer Classification <live-coding>", "KaleCancer Survival Analysis <live-coding-survival>"]),
                               ("kalecardiac", ["Chest X-ray + ECG <cardiovae>", "12-lead ECG <lsemvae>"])):
            staged = (ROOT / f"site/_staged/tutorials/{track}/index.md").read_text(encoding="utf-8")
            for entry in entries:
                self.assertIn(entry, staged)
            self.assertNotIn("Getting Started <", staged)
            self.assertNotIn("Results and Interpretation <", staged)
            self.assertNotIn("Example Notebook <", staged)
        for doc in ("index", "tutorials/kalecancer/index", "tutorials/kalecardiac/index"):
            sidebar = page(doc).split('<div class="bd-toc-item navbar-nav active">')[1].split('</nav>')[0]
            # Each track's own entry opens its overview, so neither track lists a separate Overview.
            for obsolete in ("Live-Coding Notebook", "Example Notebook", "Results and Interpretation", "Overview"):
                self.assertNotIn(">" + obsolete + "</a>", sidebar)

    def test_retired_urls_redirect_to_current_pages(self):
        redirects = {"docs/agenda": "about.html#programme","docs/prerequisites": "participation.html",
                     "tutorials/kalecancer/getting-started": "index.html",
                     "tutorials/kalecardiac/getting-started": "index.html",
                     "tutorials/kalecancer/results": "live-coding.html#interpretation-and-next-steps",
                     "tutorials/kalecardiac/results": "cardiovae.html#step-3-evaluation",
                     "tutorials/kalecardiac/cardiovae-hands-on": "cardiovae.html",
                     "tutorials/kalecardiac/lsemvae-hands-on": "lsemvae.html",
                     "tutorials/kalecardiac/live-coding": "cardiovae.html",
                     "tutorials/kalecardiac/live-coding-lsemvae": "lsemvae.html"}
        for old, target in redirects.items():
            html = page(old)
            self.assertIn('name="robots" content="noindex"', html)
            self.assertIn(f'url={target}', html)
            self.assertIn(f'href="{target}"', html)
            self.assertFalse((ROOT / "site/_staged" / (old + ".md")).exists())

    def test_public_identity_and_session_details(self):
        venue = "Ada Lovelace Room (108), Level 1, Regent Court, University of Sheffield"
        for doc in ("index", "docs/about", "docs/participation"):
            text = plain(page(doc))
            self.assertIn(venue, text)
            self.assertIn("18 November 2026", text)
            self.assertIn("13:00–17:00", text)
        for doc in ("index", "docs/about"):
            self.assertIn("organised by the CMI AIRE team with the support of UKOMAIN", plain(page(doc)).replace("Organised", "organised"))
        self.assertIn("for the KaleCancer project", plain(page("index")))
        self.assertIn('_static/mdas-logo.png', page("index"))
        self.assertIn('href="tutorials/kalecancer/index.html"', page("index"))
        self.assertIn('href="tutorials/kalecardiac/index.html"', page("index"))
        for p in HTML.rglob("*.html"):
            text = p.read_text()
            if 'name="robots" content="noindex"' in text:
                continue
            self.assertNotIn("Live-Coding Notebook", text)
            self.assertNotIn("MDAS 1.0", text)
            self.assertNotIn('class="headerlink"', text)

    def test_overviews_and_setup_are_concise_and_parallel(self):
        cancer = page("tutorials/kalecancer/index")
        for obsolete in ("ABMIL", "32-dimensional", "40 training epochs"):
            self.assertNotIn(obsolete, cancer)
        self.assertIn('assets/kalecancer-fusion-workflow.svg', cancer)
        for track, examples in (("kalecancer", ("live-coding", "live-coding-survival")), ("kalecardiac", ("cardiovae", "lsemvae"))):
            overview = page(f"tutorials/{track}/index")
            for example in examples:
                self.assertIn(f'href="{example}.html"', overview)
        quick = page("docs/quick-start")
        for target in ("../tutorials/kalecancer/live-coding.html", "../tutorials/kalecancer/live-coding-survival.html", "../tutorials/kalecardiac/cardiovae.html", "../tutorials/kalecardiac/lsemvae.html"):
            self.assertIn(f'href="{target}"', quick)
        participation = plain(page("docs/participation"))
        self.assertNotIn("Choose an execution route", participation)
        self.assertIn("Do not upload identifiable patient data", participation)
        self.assertIn('href="quick-start.html"', page("docs/participation"))
        about = page("docs/about")
        self.assertEqual(about.count('<table'), 1)
        self.assertIn('id="programme"', about)
        self.assertIn('href="#programme"', about.split('id="pst-secondary-sidebar"')[1])
        self.assertIn("Closing remarks", plain(about))
        self.assertNotIn("Fusion approach", plain(about))
        self.assertNotIn("Session Agenda", plain(page("index")))


if __name__ == "__main__":
    unittest.main()
