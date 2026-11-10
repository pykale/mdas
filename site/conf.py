"""Sphinx configuration for the participant documentation."""

import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "_ext"))

from mdas_notebooks import CARDIAC_NOTEBOOKS, CARDIAC_TUTORIALS_TITLE, NOTEBOOKS

project = "Multimodal Data Analysis Session (MDAS)"
author = "CMI/UKOMAIN"
copyright = "2026, PyKale"
language = "en"
needs_sphinx = "9.2"
extensions = ["myst_nb", "sphinx.ext.githubpages", "sphinxcontrib.mermaid"]
MDAS_ENABLE_THEBE = os.environ.get("MDAS_ENABLE_THEBE", "1") != "0"
mdas_binder_pages = []  # Public notebook pages offer Colab only; retain the Binder environment separately.
if MDAS_ENABLE_THEBE:
    extensions += ["sphinx_thebe", "mdas_interactive"]
    thebe_config = {
        "always_load": False,
        "repository_url": "https://github.com/pykale/mdas",
        "repository_branch": os.environ.get("MDAS_BINDER_REF", "main"),
        "selector": ".cell",
        "selector_input": ".cell_input pre",
        "selector_output": ".cell_output",
        # Used by the page-scoped adapter, which also starts each kernel in its notebook's folder.
        "binder_url": os.environ.get("MDAS_BINDER_URL", "https://mybinder.org"),
    }
source_suffix = {".md": "myst-nb", ".ipynb": "myst-nb"}
nb_execution_mode = "off"
nb_execution_excludepatterns = ["**"]
nb_remove_code_source = False
nb_remove_code_outputs = False
nb_scroll_outputs = True
root_doc = "index"
exclude_patterns = ["_build", ".DS_Store", "Thumbs.db"]

myst_enable_extensions = ["alert", "colon_fence", "dollarmath", "amsmath"]
myst_heading_anchors = 4
myst_fence_as_directive = ["mermaid"]
nitpicky = True

html_theme = "sphinx_book_theme"
html_title = project
html_short_title = project
html_baseurl = "https://pykale.github.io/mdas/"
html_static_path = ["_static"]
templates_path = ["_templates"]
html_css_files = ["mdas.css"]
html_js_files = [("mdas-presentation.js", {"defer": "defer"})]
html_logo = "_static/mdas-logo.png"
html_permalinks = False
html_show_sourcelink = False
html_copy_source = False
html_show_sphinx = False
html_theme_options = {
    "repository_url": "https://github.com/pykale/mdas",
    "repository_branch": "main",
    "use_repository_button": True,
    "use_download_button": False,
    "use_fullscreen_button": False,
    "home_page_in_toc": True,
    "show_navbar_depth": 3,
    "max_navbar_depth": 4,
    "show_toc_level": 2,
    "toc_title": "On this page",
    "navigation_with_keys": False,
    "logo": {"text": ""},
}


BINDER_LAUNCH = """<button type="button" id="mdas-thebe-launch" class="btn btn-primary mdas-execution-button thebe-launch-button" onclick="mdasLaunchInteractive()">Run with Binder</button>""" if MDAS_ENABLE_THEBE else "<p>In-page execution is disabled for this build. Read the saved notebook below or use Colab.</p>"

def execution_help(target):
    """Secondary help link; it opens in a new tab so the notebook page stays in place."""
    return f"""<div class="mdas-notebook-tools"><a class="mdas-execution-help" href="{target}" target="_blank" rel="noopener" aria-label="Execution Help (opens in a new tab)"><svg class="mdas-help-icon" aria-hidden="true" focusable="false" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M12 6v15 M12 6C9 4 6 4 3 5v14c3-1 6-1 9 1 M12 6c3-2 6-2 9-1v14c-3-1-6-1-9 1"/></svg> Execution Help</a></div>"""


def cardiac_intro(docname):
    """Shared heading, tutorial picker and the Colab action for a Cardiac tutorial page."""
    label, path = CARDIAC_NOTEBOOKS[docname]
    pages = {name: (name.rsplit("/", 1)[1], title) for name, (title, _) in CARDIAC_NOTEBOOKS.items()}
    options = "".join(
        f'<option value="{page}.html"' + (" selected" if name == docname else "") + f">{title}</option>"
        for name, (page, title) in pages.items()
    )
    # Reset before leaving, so returning with the back button shows this page's tutorial.
    picker = ('<div class="mdas-tutorial-picker"><label for="mdas-tutorial-select">Choose a tutorial</label> '
              '<select id="mdas-tutorial-select" onchange="const target = this.value; '
              "this.value = this.querySelector('option[selected]').value; location.assign(target);\">"
              f"{options}</select></div>")
    fallback = " | ".join(f'<a href="{page}.html">{title}</a>' for page, title in pages.values())
    # The default page also holds the sidebar branch beneath the shared entry.
    branch = ""
    if docname == next(iter(CARDIAC_NOTEBOOKS)):
        items = "\n".join(f"{title} <{'self' if name == docname else page}>" for name, (page, title) in pages.items())
        branch = f"\n```{{toctree}}\n:hidden:\n:titlesonly:\n\n{items}\n```\n"
    return f"""{execution_help("../../docs/notebook-execution.html#cardiac-setup")}

# {CARDIAC_TUTORIALS_TITLE}

{picker}<noscript><p>Choose: {fallback}</p></noscript>

**{label}**

Run this tutorial in Google Colab, which provides the GPU it uses for training.

<div class="mdas-execution-actions">
<a class="btn btn-primary mdas-execution-button" href="https://colab.research.google.com/github/pykale/mdas/blob/main/{path}">Run in Google Colab</a>
</div>

In Colab, choose a T4 GPU runtime, then run Step 0 in order: install KaleCardiac, fetch configurations and download the tutorial data. For **Run locally**, see [Quick Start](../../docs/quick-start.md#cardiac).

> Sessions are temporary. Save code edits, important results and generated files before leaving or opening another example. Do not upload private or patient data to public services.
{branch}"""


def notebook_intro(docname):
    """Own title and matching execution routes; scientific cells are untouched."""
    if docname in CARDIAC_NOTEBOOKS:
        return cardiac_intro(docname)
    title, path = NOTEBOOKS[docname]
    colab = path.replace(".ipynb", "_colab.ipynb")
    setup = ("In Colab select the documented **Python 3.12 / 2026.07** runtime, then run the initial setup cell. "
             "Follow any restart instruction before continuing. ")
    return f"""{execution_help("../../docs/notebook-execution.html")}

# {title}

<span id="live-coding-notebook"></span>

Run this example in Google Colab, which opens the matching showcase copy in a separate runtime.

<div class="mdas-execution-actions">
<a class="btn btn-primary mdas-execution-button" href="https://colab.research.google.com/github/pykale/mdas/blob/main/{colab}">Run in Google Colab</a>
</div>

{setup}For **Run locally**, see [Quick Start](../../docs/quick-start.md#cancer).

> Sessions are temporary. Save code edits, important results and generated files before leaving or opening another example. Do not upload private or patient data to public services.
"""


def notebook_guidance(docname):
    if docname in CARDIAC_NOTEBOOKS:
        detail = "Attributions describe this model's use of its inputs, not a causal explanation or a clinical diagnosis. Compare performance when inputs are withheld and use independent evaluation before drawing clinical conclusions."
    elif docname.endswith("-survival"):
        detail = "A log-hazard score orders relative risk; it is not an event time or a survival probability. Interpret censored follow-up correctly. Ranking and calibration answer different questions: inspect the notebook's survival probabilities and calibration analysis separately from concordance. Censoring and follow-up assumptions limit comparisons, and synthetic time units do not establish a clinical horizon."
    else:
        detail = "Class probabilities describe the synthetic labels; discrimination does not establish calibration or reliable individual clinical predictions. Compare modalities and uncertainty rather than assuming that fusion must improve performance. An interval spanning zero does not establish a clear positive gain; intervals from a small synthetic cohort are not external clinical validation."
    research = ("" if docname in CARDIAC_NOTEBOOKS else
                "\n\nThe [KaleCancer HANCOCK research examples](https://github.com/pykale/cancer/tree/main/examples/hancock) require authorised local data, the expected dataset layout and appropriate compute; they are not no-data starter exercises.")
    return ("## Interpretation and next steps\n\n" + detail +
            "\n\nSynthetic results demonstrate a software workflow, not clinical validity, external generalisation or causality. Keep subjects separated across splits, fit preprocessing on training data, assess uncertainty and missing inputs, and plan external evaluation. Clinical data require permissions and secure infrastructure.\n\n"
            "Return to the [tutorial overview](index.md) or follow [Quick Start](../../docs/quick-start.md) to explore another example." + research)


def prepare_notebook(app, docname, source):
    """Add access links at parse time; staged/original notebook bytes stay intact."""
    if docname not in NOTEBOOKS and docname not in CARDIAC_NOTEBOOKS:
        return
    import json
    import re

    notebook = json.loads(source[0])
    notebook.setdefault("metadata", {}).setdefault("mystnb", {})["execution_mode"] = "off"
    # Ignore VS Code-only viewer payloads in the in-memory rendering copy.
    # All affected outputs retain their standard HTML/text representation.
    for cell in notebook["cells"]:
        for output in cell.get("outputs", []):
            data = output.get("data", {})
            if "text/html" in data or "text/plain" in data:
                data.pop("application/vnd.microsoft.datawrangler.viewer.v0+json", None)
    # Nest the notebook's existing section headings beneath its page title.
    # Code, outputs, safety notes and scientific text are unchanged. Notebooks
    # whose sections already start at level 2 (no H1) need no nesting.
    markdown = [cell for cell in notebook["cells"] if cell["cell_type"] == "markdown"]
    if any(re.search(r"^# ", "".join(cell["source"]), flags=re.M) for cell in markdown):
        for cell in markdown:
            text = "".join(cell["source"])
            cell["source"] = re.sub(r"^(#{1,5}) ", r"#\1 ", text, flags=re.M)
    if docname in CARDIAC_NOTEBOOKS:
        notebook["metadata"].setdefault("language_info", {})["pygments_lexer"] = "ipython3"
    notebook["cells"].insert(0, {"cell_type": "markdown", "id": "mdas-access", "metadata": {},
                                 "source": notebook_intro(docname)})
    notebook["cells"].append({"cell_type": "markdown", "id": "mdas-next-step", "metadata": {},
                              "source": notebook_guidance(docname)})
    source[0] = json.dumps(notebook)



REDIRECTS = {
    "docs/agenda": "about.html#programme",
    "tutorials/kalecancer/results": "live-coding.html#interpretation-and-next-steps",
    "tutorials/kalecardiac/getting-started": "index.html",
    "docs/prerequisites": "participation.html",
    "tutorials/README": "../index.html#explore-the-examples",
    "tutorials/kalecancer/hands-on": "live-coding.html",
    "docs/overview": "about.html",
    "docs/resources": "quick-start.html",
    "notebooks/README": "../tutorials/kalecancer/live-coding.html",
    "tutorials/kalecancer/README": "index.html",
    "tutorials/kalecancer/getting-started": "index.html",
    "tutorials/kalecardiac/README": "index.html",
    "tutorials/kalecardiac/cardiovae-hands-on": "cardiovae.html",
    "tutorials/kalecardiac/lsemvae-hands-on": "lsemvae.html",
    "tutorials/kalecardiac/results": "cardiovae.html#interpretation-and-next-steps",
    "tutorials/kalecardiac/live-coding": "cardiovae.html",
    "tutorials/kalecardiac/live-coding-lsemvae": "lsemvae.html",
}


def cardiac_tutorial_page(app, pagename, templatename, context, doctree):
    """Load the picker style, and name the method in previous/next links (the pages share one heading)."""
    if pagename not in CARDIAC_NOTEBOOKS:
        return
    app.add_css_file("mdas-tutorial-picker.css")
    titles ={app.builder.get_relative_uri(pagename, name): label for name, (label, _) in CARDIAC_NOTEBOOKS.items()}
    for key in ("prev", "next"):
        if context.get(key) and context[key]["link"] in titles:
            context[key]["title"] = titles[context[key]["link"]]


def redirect_pages(app):
    for old, target in REDIRECTS.items():
        fragments = {}
        if old == "tutorials/kalecancer/results":
            fragments = {key: "live-coding-survival.html#interpretation-and-next-steps"
                         for key in ("#survival-analysis-results-and-interpretation", "#read-risk-alongside-follow-up")}
        yield old, {"redirect_target": target, "redirect_fragments": fragments}, "redirect.html"


def setup(app):
    # The original notebook declares this legacy display lexer. Register an
    # alias rather than editing its metadata or suppressing highlighting warnings.
    from pygments.lexers import PythonLexer

    app.add_lexer("ipython2", PythonLexer)
    app.connect("source-read", prepare_notebook)
    app.connect("html-page-context", cardiac_tutorial_page)
    app.add_js_file("mdas-notebooks.js", defer="defer")
    app.add_css_file("mdas-notebooks.css")
    app.connect("html-collect-pages", redirect_pages)
