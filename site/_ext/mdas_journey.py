"""Small, reusable learning-stage indicator; no client-side state or execution hooks."""
import re

STAGES = ("Discover", "Prepare", "Explore", "Run", "Interpret", "Continue")
DOC_STAGES = {
    "index": "Discover", "docs/about": "Discover", "docs/participation": "Prepare",
    "docs/quick-start": "Prepare", "tutorials/kalecancer/getting-started": "Explore",
    "tutorials/kalecardiac/getting-started": "Explore",
    "tutorials/kalecancer/live-coding": "Run", "tutorials/kalecancer/live-coding-survival": "Run",
    "tutorials/kalecardiac/cardiovae-hands-on": "Run", "tutorials/kalecardiac/lsemvae-hands-on": "Run",
    "tutorials/kalecancer/results": "Interpret", "tutorials/kalecardiac/results": "Interpret",
}


def render_journey(docname):
    current = DOC_STAGES.get(docname)
    if not current:
        return ""
    items = "".join('<li' + (' aria-current="step"' if label == current else '') + f'>{label}</li>' for label in STAGES)
    return '<div class="mdas-learning-journey" role="group" aria-label="Learning journey"><ol>' + items + '</ol></div>'


def prepare_journey(app, docname, source):
    if docname not in DOC_STAGES or docname.startswith("tutorials/kalecancer/live-coding"):
        return
    # Presentation-only adaptation; authoritative Markdown and Cardiac files stay intact.
    source[0] = re.sub(r"^(# [^\n]+\n)", lambda match: match[0] + "\n" + render_journey(docname) + "\n", source[0], count=1, flags=re.M)
