"""Scope sphinx-thebe to the Binder-enabled Cancer pages and use each notebook's real repository path."""

import json
import posixpath

from docutils import nodes

from mdas_notebooks import BINDER_FILES, NOTEBOOKS


def configure_page(app, doctree, docname):
    """Use supported Thebe options, after sphinx-thebe adds its configuration."""
    for node in list(doctree.findall(nodes.raw)):
        text = node.astext()
        if 'type="text/x-thebe-config"' not in text and "<script>kernelName =" not in text:
            continue
        if docname not in app.config.mdas_binder_pages:
            node.parent.remove(node)
            continue
        if 'type="text/x-thebe-config"' in text:
            config = app.config.thebe_config
            repo = config["repository_url"].removeprefix("https://github.com/").rstrip("/")
            options = {
                "bootstrap": False,
                "requestKernel": True,
                "binderOptions": {
                    "repo": repo,
                    "ref": config["repository_branch"],
                    "binderUrl": config["binder_url"],
                    "savedSession": {"enabled": False},
                },
                # The kernel starts in the notebook's own folder, beside its helper or configs.
                "kernelOptions": {"name": "python3", "path": posixpath.dirname(NOTEBOOKS[docname][1])},
                "codeMirrorConfig": {"theme": "default", "mode": "python"},
                "predefinedOutput": True,
                "mathjaxUrl": False,
            }
            preflight = {
                "repository": repo,
                "ref": config["repository_branch"],
                "required_files": [".binder/runtime.txt", ".binder/requirements.txt", *BINDER_FILES[docname]],
            }
            node["format"] = "html"
            node.children[:] = [nodes.Text(
                '<script type="text/x-thebe-config">' + json.dumps(options) + '</script>'
                '<script type="application/json" id="mdas-binder-check">' + json.dumps(preflight) + '</script>'
            )]


def scope_assets(app, pagename, templatename, context, doctree):
    if pagename in app.config.mdas_binder_pages:
        return

    def keep(asset):
        filename = str(getattr(asset, "filename", asset))
        body = getattr(asset, "attributes", {}).get("body", "") or ""
        return not ("sphinx-thebe" in filename or "mdas-interactive" in filename
                    or "const THEBE_JS_URL" in body)

    for key in ("script_files", "css_files"):
        context[key] = [asset for asset in context.get(key, []) if keep(asset)]


def setup(app):
    app.add_config_value("mdas_binder_pages", list(NOTEBOOKS), "html")
    app.add_js_file("mdas-interactive.js", defer="defer")
    app.add_css_file("mdas-interactive.css")
    app.connect("doctree-resolved", configure_page, priority=800)
    app.connect("html-page-context", scope_assets, priority=800)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
