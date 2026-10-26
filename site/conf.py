"""Sphinx configuration for the participant documentation."""

import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "_ext"))

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
        "repository_url": "https://github.com/pykale/mmai-mdas",
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
html_baseurl = "https://pykale.github.io/mmai-mdas/"
html_static_path = ["_static"]
templates_path = ["_templates"]
html_css_files = ["mdas.css"]
html_logo = "_static/mdas-logo.png"
html_show_sourcelink = False
html_copy_source = False
html_show_sphinx = False
html_theme_options = {
    "repository_url": "https://github.com/pykale/mmai-mdas",
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
    "logo": {"text": "MDAS 2026"},
}


def prepare_notebook(app, docname, source):
    """Add access links at parse time; staged/original notebook bytes stay intact."""
    if docname != "tutorials/kalecancer/live-coding":
        return
    import json
    import re

    notebook = json.loads(source[0])
    notebook.setdefault("metadata", {}).setdefault("mystnb", {})["execution_mode"] = "off"
    # Nest the notebook's existing section headings beneath its page title.
    # Code, outputs, safety notes and scientific text are unchanged.
    for cell in notebook["cells"]:
        if cell["cell_type"] == "markdown":
            text = "".join(cell["source"])
            cell["source"] = re.sub(r"^(#{1,5}) ", r"#\1 ", text, flags=re.M)
    launch = """<button type="button" id="mdas-thebe-launch" class="btn btn-primary thebe-launch-button" onclick="mdasLaunchInteractive()">Run interactively on this website</button>
<p id="mdas-thebe-status" role="status" aria-live="polite">Not connected. An interactive session starts only when you choose to launch it.</p>""" if MDAS_ENABLE_THEBE else "<p>In-page execution is disabled for this build. Read the saved notebook below or use Colab.</p>"
    intro = """# Live-Coding Notebook

MDAS_INTERACTIVE_CONTROL

<a class="btn btn-primary" href="https://colab.research.google.com/github/pykale/mmai-mdas/blob/main/notebooks/MDAS/cancer/cancer_live_coding.ipynb">Open in Google Colab</a>

[View on GitHub](https://github.com/pykale/mmai-mdas/blob/main/notebooks/MDAS/cancer/cancer_live_coding.ipynb).

[Open Binder build logs](https://mybinder.org/v2/gh/pykale/mmai-mdas/main?urlpath=lab%2Ftree%2Fnotebooks%2FMDAS%2Fcancer%2Fcancer_live_coding.ipynb) · [Connection troubleshooting](../../docs/notebook-execution.md#connection-troubleshooting).

Read the notebook below, run its code directly on this page using a temporary Binder environment, or open it in Google Colab. Online execution requires an internet connection and may take time to initialise.

Joffray Hargreaves's original code and saved outputs remain readable without an online service. No cells run during the website build or automatically after connection. Once connected, edit and run cells individually in order; the training and advanced comparison cells may take longer.

Binder sessions are temporary, public resources are limited and availability is not guaranteed. Colab is an alternative if Binder is busy. Changes in temporary online sessions may not be saved: download work you want to keep.

The Colab button opens the original notebook. Colab execution needs additional dependency and companion-module setup; a Colab-ready edition is deferred. Use the in-page Binder kernel for the currently working interactive option.

> [!CAUTION]
> Do not upload identifiable patient data, confidential material or private datasets to public services. Use clinical data only with appropriate permissions and secure infrastructure.
""".replace("MDAS_INTERACTIVE_CONTROL", launch)
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


def setup(app):
    # The original notebook declares this legacy display lexer. Register an
    # alias rather than editing its metadata or suppressing highlighting warnings.
    from pygments.lexers import PythonLexer

    app.add_lexer("ipython2", PythonLexer)
    app.connect("source-read", prepare_notebook)
    app.connect("html-collect-pages", redirect_pages)
