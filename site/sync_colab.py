"""Generate/check direct Colab copies while preserving all original cell dictionaries.

Each copy is its source notebook with two cells in front: short instructions and one setup cell. The setup cell
installs KaleCancer with pip and downloads the notebook's helper files; nothing else is pinned, so Colab keeps its
own versions of everything KaleCancer does not constrain.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

CANCER = Path(__file__).resolve().parents[1] / "notebooks/MDAS/cancer"
KALECANCER = "kalecancer @ git+https://github.com/pykale/cancer.git@f8dff11372587c4ae97ce86b7d869ace511a6a17"
HELPER_URL = "https://raw.githubusercontent.com/pykale/mdas/main/notebooks/MDAS/cancer/"

# Helper files each notebook imports, and whether it can train on a GPU.
NOTEBOOKS = {
    "classification_showcase": {"helpers": ["synthetic_data_generation.py", "synthetic_showcase_data.py"], "gpu": False},
    "survival_showcase": {"helpers": ["synthetic_data_generation.py", "synthetic_showcase_data.py"], "gpu": False},
    "hancock_questions": {"helpers": ["hancock_data.py"], "gpu": True},
}


def intro(gpu: bool) -> str:
    runtime = ("A **T4 GPU** hardware accelerator is optional: training runs on it, but the models are small, so the "
               "notebook is only a little faster, and setup downloads a larger PyTorch (a couple of minutes longer). " if gpu else "")
    return f"""# Before you start

1. **Switch to Python 3.12:** go to **Runtime > Change runtime type**, set **Runtime version** to **2026.07** and click **Save**. {runtime}Colab's default Python 3.13 won't work.
2. **Run the setup cell below.** The first run takes about 6 minutes, while it installs KaleCancer.
3. **When it prints "Ready"**, run the rest of the notebook in order.

Colab sessions are temporary, so download anything you want to keep.
"""


def setup_cell(helpers: list[str], gpu: bool) -> str:
    if gpu:
        torch = '''# KaleCancer needs PyTorch 2.6. Without a GPU, the CPU-only build is a much smaller download.
if shutil.which("nvidia-smi"):
    torch_packages = ["torch==2.6.0", "torchvision==0.21.0"]
else:
    torch_packages = ["--extra-index-url", "https://download.pytorch.org/whl/cpu", "torch==2.6.0+cpu", "torchvision==0.21.0+cpu"]'''
    else:
        torch = '''# KaleCancer needs PyTorch 2.6. This notebook runs on the CPU, so get the much smaller CPU-only build.
torch_packages = ["--extra-index-url", "https://download.pytorch.org/whl/cpu", "torch==2.6.0+cpu", "torchvision==0.21.0+cpu"]'''
    device = 'device = "GPU" if torch.cuda.is_available() else "CPU"' if gpu else 'device = "CPU"'
    return f'''# Set up Colab: install KaleCancer and download this notebook's helper files.
import shutil
import subprocess
import sys
import urllib.request

if sys.version_info[:2] != (3, 12):
    raise SystemExit("KaleCancer needs Python 3.12. Choose Runtime > Change runtime type, set Runtime version to 2026.07, then run this cell again.")

{torch}

# Pip's output is shown only if the installation fails. Its notes about Colab's own packages are harmless.
print("Installing KaleCancer. This takes about 6 minutes...", flush=True)
install = subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", *torch_packages,
                          "{KALECANCER}"], capture_output=True, text=True)
if install.returncode != 0:
    print(install.stdout, install.stderr)
    raise SystemExit("Installation failed: see the messages above, then run this cell again.")

for file in {helpers!r}:
    urllib.request.urlretrieve("{HELPER_URL}" + file, file)

import torch
import kalecancer
{device}
print(f"Ready: PyTorch {{torch.__version__}} on the {{device}}. Run the rest of the notebook in order.")
'''


def additions(name: str) -> list[dict]:
    config = NOTEBOOKS[name]
    return [
        {"cell_type": "markdown", "id": "mdas-colab-intro", "metadata": {},
         "source": intro(config["gpu"]).splitlines(keepends=True)},
        {"cell_type": "code", "id": "mdas-colab-setup", "metadata": {}, "execution_count": None, "outputs": [],
         "source": setup_cell(config["helpers"], config["gpu"]).splitlines(keepends=True)},
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    for name in NOTEBOOKS:
        original = json.loads((CANCER / f"{name}.ipynb").read_text(encoding="utf-8"))
        notebook = copy.deepcopy(original)
        notebook["cells"] = additions(name) + notebook["cells"]
        target = CANCER / f"{name}_colab.ipynb"
        if args.check:
            if not target.is_file() or json.loads(target.read_text(encoding="utf-8")) != notebook:
                raise SystemExit(f"{target.name} is out of sync. Run python site/sync_colab.py.")
        else:
            target.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"{target.name}: original cells preserved; {'checked' if args.check else 'generated'}")


if __name__ == "__main__":
    main()
