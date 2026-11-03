"""Generate/check direct Colab copies while preserving all original cell dictionaries."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

CANCER = Path(__file__).resolve().parents[1] / "notebooks/MDAS/cancer"


def additions() -> list[dict]:
    checksums = {name: hashlib.sha256((CANCER / name).read_bytes().replace(b"\r\n", b"\n")).hexdigest()
                 for name in ("colab_setup.py", "colab-requirements.txt")}
    intro = """# Google Colab Environment Setup

**Python 3.12 required.** Before running, select **Runtime > Change runtime type > Runtime Version > 2026.07**, then reconnect. Google currently lists this Python 3.12 runtime; if it is no longer offered, use **Run with Binder** on the MDAS website. The default Python 3.13 runtime is incompatible with the published KaleCancer/PyKale requirements.

Run the setup cell below, then run the scientific cells individually in order. Setup downloads the companion module and installs a pinned CPU stack in **this notebook's active Python environment**; no separate notebook, Drive mount or upload is needed. The first installation may take several minutes. If libraries with different versions are already loaded, setup will ask you to **Restart session** and rerun setup before continuing. Reruns reuse the installed packages and downloaded files.

Every cell below this setup section is preserved from the original MDAS notebook, including its full training and advanced analyses. Use synthetic data only. Colab sessions are temporary; download work you want to keep.
"""
    bootstrap = '''# Bootstrap only: scientific code below is unchanged.
import hashlib
from pathlib import Path
import runpy
import sys
from urllib.request import Request, urlopen

if sys.version_info[:2] != (3, 12):
    raise RuntimeError("Python 3.12 is required. Choose Runtime > Change runtime type > Runtime Version > 2026.07, reconnect, then rerun setup. If unavailable, use Run with Binder.")

# Prefer a local checkout when testing; a fresh Colab session uses /content.
_candidates = [Path.cwd(), *(p / "notebooks/MDAS/cancer" for p in [Path.cwd(), *Path.cwd().parents])]
_mdas_dir = next((p for p in _candidates if (p / "colab_setup.py").is_file()), Path("/content/mdas-cancer/notebooks/MDAS/cancer"))
_mdas_dir.mkdir(parents=True, exist_ok=True)
_checksums = CHECKSUMS
try:
    for _name, _digest in _checksums.items():
        _path = _mdas_dir / _name
        if not _path.is_file() or hashlib.sha256(_path.read_bytes().replace(b"\\r\\n", b"\\n")).hexdigest() != _digest:
            print("MDAS: downloading", _name, flush=True)
            _url = "https://raw.githubusercontent.com/pykale/mdas/main/notebooks/MDAS/cancer/" + _name
            with urlopen(Request(_url, headers={"User-Agent": "MDAS-Colab"}), timeout=60) as _response:
                _contents = _response.read().replace(b"\\r\\n", b"\\n")
            if hashlib.sha256(_contents).hexdigest() != _digest:
                raise RuntimeError("Setup revision mismatch. Reopen the latest Colab notebook from the MDAS website; no downloaded code was executed.")
            _temporary = _path.with_suffix(_path.suffix + ".tmp")
            _temporary.write_bytes(_contents)
            _temporary.replace(_path)
    runpy.run_path(str(_mdas_dir / "colab_setup.py"))["prepare"](_mdas_dir)
except OSError as _error:
    raise RuntimeError("MDAS download/install failed. Check internet access and rerun setup. The reviewed Colab support files must exist on public main.") from _error
'''.replace("CHECKSUMS", repr(checksums))
    return [
        {"cell_type": "markdown", "id": "mdas-colab-intro", "metadata": {}, "source": intro.splitlines(keepends=True)},
        {"cell_type": "code", "id": "mdas-colab-setup", "metadata": {}, "execution_count": None, "outputs": [],
         "source": bootstrap.splitlines(keepends=True)},
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    for name in ("classification", "survival"):
        original = json.loads((CANCER / f"{name}.ipynb").read_text(encoding="utf-8"))
        notebook = copy.deepcopy(original)
        notebook["cells"] = additions() + notebook["cells"]
        target = CANCER / f"{name}_colab.ipynb"
        if args.check:
            if not target.is_file() or json.loads(target.read_text(encoding="utf-8")) != notebook:
                raise SystemExit(f"{target.name} is out of sync. Run python site/sync_colab.py.")
        else:
            target.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"{target.name}: original cells preserved; {'checked' if args.check else 'generated'}")


if __name__ == "__main__":
    main()
