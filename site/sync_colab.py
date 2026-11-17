"""Generate/check direct Colab copies while preserving all original cell dictionaries."""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

CANCER = Path(__file__).resolve().parents[1] / "notebooks/MDAS/cancer"


SUPPORT_FILES = ["colab_setup.py", "colab-requirements.txt", "synthetic_data_generation.py", "synthetic_showcase_data.py"]
# Helpers only some notebooks need, downloaded after the shared ones.
EXTRA_FILES = {"hancock_questions": ["hancock_data.py"]}


def additions(extra: list[str] = ()) -> list[dict]:
    intro = """# Before you start

1. **Switch to Python 3.12:** go to **Runtime > Change runtime type**, set **Runtime version** to **2026.07** and click **Save**. Colab's default Python 3.13 won't work.
2. **Run the setup cell below.** The first run takes a few minutes. If it asks you to restart, choose **Runtime > Restart session** and run it again.
3. **When you see "MDAS ready"**, run the rest of the notebook in order.

Colab sessions are temporary, so download anything you want to keep.
"""
    bootstrap = f'''# Set up Colab: download the tutorial's helper files, then install the packages it needs.
import sys
from pathlib import Path
from urllib.request import urlretrieve

folder = Path.cwd() if Path("colab_setup.py").exists() else Path("/content/mdas")
folder.mkdir(exist_ok=True)
for file in {SUPPORT_FILES + list(extra)!r}:
    if not (folder / file).exists():
        urlretrieve("https://raw.githubusercontent.com/pykale/mdas/main/notebooks/MDAS/cancer/" + file, folder / file)

sys.path.insert(0, str(folder))
import colab_setup
colab_setup.prepare(folder, showcase=True)
'''
    return [
        {"cell_type": "markdown", "id": "mdas-colab-intro", "metadata": {}, "source": intro.splitlines(keepends=True)},
        {"cell_type": "code", "id": "mdas-colab-setup", "metadata": {}, "execution_count": None, "outputs": [],
         "source": bootstrap.splitlines(keepends=True)},
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    for name in ("classification_showcase", "survival_showcase", "hancock_questions"):
        original = json.loads((CANCER / f"{name}.ipynb").read_text(encoding="utf-8"))
        notebook = copy.deepcopy(original)
        notebook["cells"] = additions(EXTRA_FILES.get(name, [])) + notebook["cells"]
        target = CANCER / f"{name}_colab.ipynb"
        if args.check:
            if not target.is_file() or json.loads(target.read_text(encoding="utf-8")) != notebook:
                raise SystemExit(f"{target.name} is out of sync. Run python site/sync_colab.py.")
        else:
            target.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"{target.name}: original cells preserved; {'checked' if args.check else 'generated'}")


if __name__ == "__main__":
    main()
