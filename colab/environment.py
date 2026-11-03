"""Prepare an isolated research environment; never replace the Colab host kernel."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
import venv

ROOT = Path(__file__).resolve().parents[1]
ENV = ROOT / ".venv" / "colab"


def environment_python(directory: Path = ENV) -> Path:
    return directory / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")


def prepare() -> Path:
    """Install once, check package metadata, and reuse only a matching lock."""
    if sys.version_info[:2] != (3, 12):
        raise RuntimeError(
            f"This kernel is Python {sys.version_info[0]}.{sys.version_info[1]}; the research packages require Python 3.12. "
            "In Colab select Runtime > Change runtime type > Runtime Version > 2026.07 (Python 3.12), "
            "then reconnect and run this preparation notebook again. Installing another Python executable "
            "does not change the Python version of this notebook kernel."
        )
    started = time.monotonic()
    inputs = [ROOT / ".binder" / "requirements.txt", ROOT / "colab" / "requirements.txt"]
    fingerprint = hashlib.sha256(b"\n".join(path.read_bytes() for path in inputs)).hexdigest()
    marker = ENV / ".mdas-lock.json"
    python = environment_python()
    if not python.is_file():
        print("MDAS: creating an isolated Python 3.12 CPU environment…", flush=True)
        # Colab images need not ship ensurepip. The host's pip can manage an
        # unseeded venv via its documented --python option (pip >= 22.3).
        venv.EnvBuilder(with_pip=False).create(ENV)
    pip = [sys.executable, "-m", "pip", "--python", str(python)]
    try:
        current = json.loads(marker.read_text(encoding="utf-8")) if marker.is_file() else {}
    except (ValueError, OSError):
        current = {}
    try:
        if current.get("lock") != fingerprint:
            print("MDAS: installing the pinned research and notebook-runner dependencies…", flush=True)
            subprocess.run(pip + ["install", "--disable-pip-version-check", "-r", str(inputs[1])], check=True)
        subprocess.run(pip + ["check"], check=True)
        subprocess.run([str(python), "-c", (
            "import torch, kale, pandas, numpy, h5py; "
            "from kalecancer.loaddata import Classification, TimeToEvent, Tabular, PatchFeatures, MultimodalDataset; "
            "from kalecancer.model import ABMIL, ClassificationHead, CoxHead, IntermediateFusion, Concat, Unimodal; "
            "from kalecancer.pipeline import Pipeline; "
            "from kalecancer.evaluate import AUROC, BalancedAccuracy, HarrellC, UnoC, EvalContext, bootstrap_ci; "
            "import nbclient, nbconvert; "
            "print('MDAS research imports OK; PyTorch', torch.__version__)"
        )], check=True)
        marker.write_text(json.dumps({"lock": fingerprint, "python": sys.version}), encoding="utf-8")
    except subprocess.CalledProcessError as error:
        marker.unlink(missing_ok=True)
        raise RuntimeError(
            "MDAS preparation failed; read the pip/import error above. Check internet access and rerun. "
            "A failed installation is not marked ready. The Colab host packages and source notebooks are unchanged."
        ) from error
    print(f"MDAS: isolated environment ready in {time.monotonic() - started:.1f}s. The Colab host kernel is unchanged.", flush=True)
    return python


if __name__ == "__main__":
    prepare()
