"""Sphinx configuration for the participant documentation."""

import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "_ext"))

from mdas_notebooks import CARDIAC_NOTEBOOKS, NOTEBOOKS, SECONDARY_NOTEBOOKS

project = "Multimodal Data Analysis Session (MDAS)"
author = "PyKale"
copyright = "2026, PyKale"
language = "en"
needs_sphinx = "9.2"
extensions = ["myst_nb", "sphinx.ext.githubpages", "sphinxcontrib.mermaid"]
MDAS_ENABLE_THEBE = os.environ.get("MDAS_ENABLE_THEBE", "1") != "0"
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

CARDIAC_INTRO = """# Live-Coding Notebook

MDAS_NOTEBOOK_SELECTOR

**MDAS_NOTEBOOK_TITLE**

Choose Binder to run the notebook directly on this website, or Google Colab to open it in a Colab runtime.

<div class="mdas-execution-actions">
MDAS_INTERACTIVE_CONTROL
<a class="btn btn-primary mdas-execution-button" href="https://colab.research.google.com/github/pykale/mdas/blob/main/MDAS_NOTEBOOK_PATH">Run in Google Colab</a>
</div>
<p id="mdas-thebe-status" role="status" aria-live="polite">Not connected. Binder starts only when you choose to launch it.</p>

Run the cells in order, starting with the package installation cell in Step 0, which installs KaleCardiac into the session. Binder sessions run on a CPU; in Colab, choose a T4 GPU runtime. To run the notebook on your own computer, see [Getting Started](getting-started.md#run-a-tutorial).

> Sessions are temporary. Copy code edits and important results before switching or leaving. Do not upload private or patient data.
"""


def cardiac_intro(docname):
    """Page title, tutorial selector and execution actions for a Cardiac notebook page."""
    options = "".join(
        f'<option value="{name.rsplit("/", 1)[1]}.html"'
        + (' selected' if name == docname else '') + f'>{label}</option>'
        for name, (label, _) in CARDIAC_NOTEBOOKS.items()
    )
    selector = ('<div class="mdas-notebook-picker"><label for="mdas-notebook-select">Choose a tutorial</label> '
                f'<select id="mdas-notebook-select" onchange="mdasSwitchNotebook(this)">{options}</select></div>'
                '<noscript><p>Choose: <a href="live-coding.html">CardioVAE</a> | '
                '<a href="live-coding-lsemvae.html">LS-EMVAE</a></p></noscript>')
    title, notebook_path = CARDIAC_NOTEBOOKS[docname]
    return (CARDIAC_INTRO.replace("MDAS_INTERACTIVE_CONTROL", BINDER_LAUNCH).replace("MDAS_NOTEBOOK_SELECTOR", selector)
            .replace("MDAS_NOTEBOOK_TITLE", title).replace("MDAS_NOTEBOOK_PATH", notebook_path))


def prepare_notebook(app, docname, source):
    """Add access links at parse time; staged/original notebook bytes stay intact."""
    if docname not in NOTEBOOKS and docname not in CARDIAC_NOTEBOOKS:
        return
    import json
    import re

    notebook = json.loads(source[0])
    if docname in SECONDARY_NOTEBOOKS:
        notebook.setdefault("metadata", {})["orphan"] = True
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
        # Their install cell uses IPython shell escapes (!pip, !git) and magics (%cd), which
        # the plain Python lexer rejects. Highlight with IPython's lexer in this copy only.
        notebook["metadata"].setdefault("language_info", {})["pygments_lexer"] = "ipython3"
        notebook["cells"].insert(0, {"cell_type": "markdown", "id": "mdas-access", "metadata": {},
                                     "source": cardiac_intro(docname)})
        source[0] = json.dumps(notebook)
        return
    title, notebook_path = NOTEBOOKS[docname]
    launch = BINDER_LAUNCH
    options = "".join(
        f'<option value="{name.rsplit("/", 1)[1]}.html"'
        + (' selected' if name == docname else '') + f'>{label}</option>'
        for name, (label, _) in NOTEBOOKS.items()
    )
    selector = ('<div class="mdas-notebook-picker"><label for="mdas-notebook-select">Choose a notebook</label> '
                f'<select id="mdas-notebook-select" onchange="mdasSwitchNotebook(this)">{options}</select></div>'
                '<noscript><p>Choose: <a href="live-coding.html">Classification</a> | '
                '<a href="live-coding-survival.html">Survival Analysis</a></p></noscript>')
    intro = """<div class="mdas-notebook-tools"><a class="mdas-execution-help" href="../../docs/notebook-execution.html" target="_blank" rel="noopener" aria-label="Execution Help (opens in a new tab)"><svg class="mdas-help-icon" aria-hidden="true" focusable="false" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 6v15"/><path d="M12 6C9 4 6 4 3 5v14c3-1 6-1 9 1"/><path d="M12 6c3-2 6-2 9-1v14c-3-1-6-1-9 1"/></svg> Execution Help</a></div>

# Live-Coding Notebook

MDAS_NOTEBOOK_SELECTOR

**MDAS_NOTEBOOK_TITLE**

Choose Binder to run directly on this website, or Google Colab to open a self-configuring notebook.

<div class="mdas-execution-actions">
MDAS_INTERACTIVE_CONTROL
<a class="btn btn-primary mdas-execution-button" href="https://colab.research.google.com/github/pykale/mdas/blob/main/MDAS_COLAB_PATH">Run in Google Colab</a>
</div>
<p id="mdas-thebe-status" role="status" aria-live="polite">Not connected. Binder starts only when you choose to launch it.</p>

Colab needs a compatible **Python 3.12** runtime. Select it and run the initial setup cell; follow any restart instruction before continuing.

> Sessions are temporary. Copy code edits and important results before switching or leaving; keep generated files separately. Use synthetic data only: do not upload private or patient data. Synthetic results do not demonstrate clinical performance.
""".replace("MDAS_INTERACTIVE_CONTROL", launch).replace("MDAS_NOTEBOOK_SELECTOR", selector).replace("MDAS_NOTEBOOK_TITLE", title).replace("MDAS_NOTEBOOK_PATH", notebook_path).replace("MDAS_COLAB_PATH", notebook_path.replace(".ipynb", "_colab.ipynb"))
    notebook["cells"].insert(0, {"cell_type": "markdown", "id": "mdas-access", "metadata": {}, "source": intro})
    notebook["cells"].append({"cell_type": "markdown", "id": "mdas-next-step", "metadata": {},
        "source": "When you have inspected the predictions, metrics and baseline comparison, [interpret the Cancer results](results.md) before drawing conclusions."})
    source[0] = json.dumps(notebook)


REDIRECTS = {
    "docs/prerequisites": "participation.html",
    "tutorials/README": "../index.html#explore-the-examples",
    "tutorials/kalecancer/hands-on": "live-coding.html",
    "docs/overview": "about.html",
    "docs/resources": "quick-start.html",
    "notebooks/README": "../tutorials/kalecancer/live-coding.html",
    "tutorials/kalecancer/README": "index.html",
    "tutorials/kalecancer/getting-started": "index.html",
    "tutorials/kalecardiac/README": "getting-started.html",
    "tutorials/kalecardiac/cardiovae-hands-on": "live-coding.html",
    "tutorials/kalecardiac/lsemvae-hands-on": "live-coding-lsemvae.html",
    "tutorials/kalecardiac/results": "live-coding.html",
}


def redirect_pages(app):
    for old, target in REDIRECTS.items():
        yield old, {"redirect_target": target}, "redirect.html"


def notebook_navigation(app, pagename, templatename, context, doctree):
    """Give each non-default notebook page its track's canonical sidebar and prev/next links."""
    canonical = SECONDARY_NOTEBOOKS.get(pagename)
    if canonical is None:
        return
    from sphinx.environment.adapters.toctree import TocTree
    def toctree(**kwargs):
        tree = TocTree(app.env).get_toctree_for(canonical, app.builder, **kwargs)
        return app.builder.render_partial(tree)["fragment"] if tree is not None else ""

    context["toctree"] = toctree
    relations = app.env.collect_relations().get(canonical)
    if relations:
        for key, target in zip(("prev", "next"), relations[1:]):
            if target:
                context[key] = {"link": app.builder.get_relative_uri(pagename, target),
                                "title": app.env.titles[target].astext()}


def setup(app):
    # The original notebook declares this legacy display lexer. Register an
    # alias rather than editing its metadata or suppressing highlighting warnings.
    from pygments.lexers import PythonLexer

    app.add_lexer("ipython2", PythonLexer)
    app.connect("source-read", prepare_notebook)
    app.connect("html-page-context", notebook_navigation, priority=400)
    app.add_js_file("mdas-notebooks.js", defer="defer")
    app.add_css_file("mdas-notebooks.css")
    app.connect("html-collect-pages", redirect_pages)
