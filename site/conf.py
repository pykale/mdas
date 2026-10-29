"""Sphinx configuration for the participant documentation."""

import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "_ext"))

from mdas_notebooks import NOTEBOOKS

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
        # Used by the page-scoped adapter to override Sphinx's staged URL path.
        "binder_url": os.environ.get("MDAS_BINDER_URL", "https://mybinder.org"),
        "kernel_path": "notebooks/MDAS/cancer",
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
html_title = "MDAS: Cancer & Cardiac Research"
html_short_title = "MDAS 2026"
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


def prepare_notebook(app, docname, source):
    """Add access links at parse time; staged/original notebook bytes stay intact."""
    if docname not in NOTEBOOKS:
        return
    import json
    import re

    title, notebook_path = NOTEBOOKS[docname]
    blank_path = notebook_path.replace(".ipynb", "_blank.ipynb")
    notebook = json.loads(source[0])
    if docname.endswith("-survival"):
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
    # Code, outputs, safety notes and scientific text are unchanged.
    for cell in notebook["cells"]:
        if cell["cell_type"] == "markdown":
            text = "".join(cell["source"])
            cell["source"] = re.sub(r"^(#{1,5}) ", r"#\1 ", text, flags=re.M)
    launch = """<button type="button" id="mdas-thebe-launch" class="btn btn-primary thebe-launch-button" onclick="mdasLaunchInteractive()">Run interactively on this website</button>
<p id="mdas-thebe-status" role="status" aria-live="polite">Not connected. An interactive session starts only when you choose to launch it.</p>""" if MDAS_ENABLE_THEBE else "<p>In-page execution is disabled for this build. Read the saved notebook below or use Colab.</p>"
    options = "".join(
        f'<option value="{name.rsplit("/", 1)[1]}.html"'
        + (' selected' if name == docname else '') + f'>{label}</option>'
        for name, (label, _) in NOTEBOOKS.items()
    )
    selector = ('<div class="mdas-notebook-picker"><label for="mdas-notebook-select">Choose a notebook</label> '
                f'<select id="mdas-notebook-select" onchange="mdasSwitchNotebook(this)">{options}</select></div>'
                '<noscript><p>Choose: <a href="live-coding.html">Classification</a> | '
                '<a href="live-coding-survival.html">Survival Analysis</a></p></noscript>')
    # Store the original notebook for a client-side export of edited code cells.
    download = json.loads(source[0])
    for cell in download["cells"]:
        if cell["cell_type"] == "code":
            cell["outputs"] = []
            cell["execution_count"] = None
    payload = json.dumps(download).replace("<", "\\u003c")
    export = (f'<script type="application/json" id="mdas-notebook-source">{payload}</script>'
              f'<button type="button" class="btn btn-secondary" onclick="mdasDownloadNotebook()">Download notebook with edits</button>'
              f'<p id="mdas-download-status" role="status"></p>')
    intro = """# Live-Coding Notebook

MDAS_NOTEBOOK_SELECTOR

**MDAS_NOTEBOOK_TITLE**

Run cells on this page using the built-in **Binder kernel**, or open the notebook in **Google Colab** as an alternative. Colab requires additional dependency and companion-module setup.

MDAS_INTERACTIVE_CONTROL

MDAS_NOTEBOOK_EXPORT

<a class="btn btn-primary" href="https://colab.research.google.com/github/pykale/mdas/blob/main/MDAS_NOTEBOOK_PATH">Open in Google Colab</a>

[View on GitHub](https://github.com/pykale/mdas/blob/main/MDAS_NOTEBOOK_PATH) | [Optional blank exercise](https://github.com/pykale/mdas/blob/main/MDAS_BLANK_PATH) | [Execution help](../../docs/notebook-execution.md).

> Sessions are temporary; save work you want to keep. Use synthetic data only: do not upload private or patient data. Synthetic results do not demonstrate clinical performance.
""".replace("MDAS_INTERACTIVE_CONTROL", launch).replace("MDAS_NOTEBOOK_SELECTOR", selector).replace("MDAS_NOTEBOOK_TITLE", title).replace("MDAS_NOTEBOOK_PATH", notebook_path).replace("MDAS_BLANK_PATH", blank_path).replace("MDAS_NOTEBOOK_EXPORT", export)
    notebook["cells"].insert(0, {"cell_type": "markdown", "id": "mdas-access", "metadata": {}, "source": intro})
    source[0] = json.dumps(notebook)


REDIRECTS = {
    "docs/overview": "about.html",
    "docs/resources": "quick-start.html",
    "notebooks/README": "../tutorials/kalecancer/live-coding.html",
    "tutorials/kalecancer/README": "getting-started.html",
    "tutorials/kalecardiac/README": "getting-started.html",
}


def redirect_pages(app):
    for old, target in REDIRECTS.items():
        yield old, {"redirect_target": target}, "redirect.html"


def notebook_navigation(app, pagename, templatename, context, doctree):
    if pagename != "tutorials/kalecancer/live-coding-survival":
        return
    from sphinx.environment.adapters.toctree import TocTree
    canonical = "tutorials/kalecancer/live-coding"
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
