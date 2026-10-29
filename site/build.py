"""Stage authoritative Markdown and build Sphinx without the research environment."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from urllib.parse import unquote, urlsplit

SITE = Path(__file__).resolve().parent
ROOT = SITE.parent
STAGED = SITE / "_staged"
HTML = SITE / "_build" / "html"
REPOSITORY = "https://github.com/pykale/mdas"
sys.path.insert(0, str(SITE / "_ext"))
from mdas_notebooks import NOTEBOOKS


def find_uv() -> str:
    """Support PowerShell terminals that have not refreshed WinGet's PATH."""
    if candidate := os.environ.get("UV_EXECUTABLE") or shutil.which("uv"):
        return candidate
    local = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local"))
    for candidate in sorted((local / "Microsoft/WinGet/Packages").glob("astral-sh.uv_*/uv.exe")):
        return str(candidate)
    raise RuntimeError("uv was not found. Add uv to PATH or set UV_EXECUTABLE to uv.exe.")


def toctree(entries: list[list[str]], caption: str | None = None) -> str:
    options = ":hidden:\n:maxdepth: 2\n:titlesonly:\n"
    if caption:
        options += f":caption: {caption}\n"
    items = "\n".join(f"{title} <{target}>" for title, target in entries)
    return f"\n\n```{{toctree}}\n{options}\n{items}\n```\n"


def stage() -> None:
    # Only replace generated directories within site/.
    if STAGED.exists():
        if STAGED.is_symlink() or STAGED.resolve().parent != SITE:
            raise RuntimeError("Refusing to replace a staging directory outside site/.")
        shutil.rmtree(STAGED)
    STAGED.mkdir()
    excluded = {"docs/overview.md", "docs/resources.md", "notebooks/README.md",
                "tutorials/kalecancer/README.md", "tutorials/kalecardiac/README.md"}
    paths = [ROOT / "README.md", *sorted((ROOT / "docs").rglob("*.md")),
             *sorted((ROOT / "tutorials").rglob("*.md"))]
    paths = [p for p in paths if p.relative_to(ROOT).as_posix() not in excluded]
    mapping = {p.relative_to(ROOT).as_posix(): p.relative_to(ROOT).as_posix() for p in paths}
    mapping["README.md"] = "index.md"
    for docname, (_, notebook_path) in NOTEBOOKS.items():
        mapping[notebook_path] = docname + ".ipynb"
    aliases = {"docs/overview.md": "docs/about.md", "docs/resources.md": "docs/quick-start.md",
               "notebooks/README.md": "tutorials/kalecancer/live-coding.ipynb",
               "tutorials/kalecancer/README.md": "tutorials/kalecancer/getting-started.md",
               "tutorials/kalecardiac/README.md": "tutorials/kalecardiac/getting-started.md"}

    def rewrite_link(match: re.Match, original: Path, destination: Path) -> str:
        label, target = match.groups()
        url = urlsplit(target)
        if url.scheme or url.netloc or not url.path or url.path.startswith("/"):
            return match.group(0)
        resolved = (original.parent / unquote(url.path)).resolve()
        try:
            key = resolved.relative_to(ROOT).as_posix().rstrip("/")
        except ValueError:
            raise RuntimeError(f"Link escapes the repository: {original}: {target}")
        if key in aliases:
            new = aliases[key]
        elif key in mapping:
            new = mapping[key]
        elif resolved.is_file() and key.startswith("assets/"):
            new = key
            output = STAGED / new
            output.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(resolved, output)
        else:
            raise RuntimeError(f"Unresolved local link: {original.relative_to(ROOT)}: {target}")
        relative = Path(os.path.relpath(STAGED / new, destination.parent)).as_posix()
        suffix = ("?" + url.query if url.query else "") + ("#" + url.fragment if url.fragment else "")
        return f"[{label}]({relative}{suffix})"

    for path in paths:
        name = path.relative_to(ROOT).as_posix()
        destination = STAGED / mapping[name]
        destination.parent.mkdir(parents=True, exist_ok=True)
        text = path.read_text(encoding="utf-8-sig")
        parts = re.split(r"(^```[^\n]*\n.*?^```[^\n]*$)", text, flags=re.M | re.S)
        for i in range(0, len(parts), 2):
            parts[i] = re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
                              lambda m: rewrite_link(m, path, destination), parts[i])
        text = "".join(parts)
        if name == "README.md":
            text = '<img class="mdas-home-logo" src="_static/mdas-logo.png" alt="Multimodal Data Analysis Session logo">\n\n' + text
            nav = json.loads((SITE / "navigation.json").read_text(encoding="utf-8"))
            text += "".join(toctree(entries, caption) for caption, entries in nav.items())
        destination.write_text(text, encoding="utf-8")
    # Byte-for-byte copy: never execute or alter the original notebook.
    for _, notebook_path in NOTEBOOKS.values():
        shutil.copyfile(ROOT / notebook_path, STAGED / mapping[notebook_path])
    for track, entries in {
        "kalecancer": [["Getting Started", "getting-started"], ["Hands-on Tutorial", "hands-on"],
                       ["Live-Coding Notebook", "live-coding"], ["Results and Interpretation", "results"]],
        "kalecardiac": [["Getting Started", "getting-started"], ["CardioVAE Hands-on", "cardiovae-hands-on"],
                        ["LS-EMVAE Hands-on", "lsemvae-hands-on"], ["Results and Interpretation", "results"]],
    }.items():
        title = "Cancer" if track == "kalecancer" else "Cardiac"
        # Navigation-only landing page, no duplicated introduction or setup.
        (STAGED / f"tutorials/{track}/index.md").write_text(
            f"# {title}\n\n[Begin with Getting Started](getting-started.md).\n" + toctree(entries), encoding="utf-8")
    print(f"Staged {len(paths)} Markdown pages and {len(NOTEBOOKS)} original notebooks in {STAGED}", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage-only", action="store_true", help="Prepare sources without running Sphinx")
    args = parser.parse_args()
    stage()
    if args.stage_only:
        return 0
    if HTML.exists():
        if HTML.is_symlink() or HTML.resolve().parent != SITE / "_build":
            raise RuntimeError("Refusing to replace an HTML directory outside site/_build/.")
        shutil.rmtree(HTML)
    requirements = [line.strip() for line in (SITE / "requirements.txt").read_text().splitlines()
                    if line.strip() and not line.startswith("#")]
    command = [find_uv(), "tool", "run", "--from", requirements[0]]
    for requirement in requirements[1:]:
        command += ["--with", requirement]
    command += ["sphinx-build", "-b", "html", "-n", "-W", "--keep-going", "-E", "-a",
                "-c", str(SITE), str(STAGED), str(HTML)]
    subprocess.run(command, cwd=ROOT, check=True)
    subprocess.run([sys.executable, str(SITE / "check_links.py")], cwd=ROOT, check=True)
    print(f"\nOpen {HTML / 'index.html'}\nFor search, serve over HTTP (see site/README.md).")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"Build failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
