"""Prepare the active Python kernel for the direct MDAS Colab notebook copies.

No kernel proxy, external execution notebook, or scientific-cell rewriting.
Binder's original notebooks never import this module.
"""
from __future__ import annotations

import hashlib
import importlib
import importlib.metadata as metadata
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from urllib.request import Request, urlopen

DATA_REF = "5e3eac4145944c38932b8ec2c78cbc08b7af068a"
DATA_SHA256 = "4c599967243fb0f8f782bbcac4ae2bf3978884598ffbd54c048c87c147d89a22"
CANCER_REF = "1f476fdba87f515286f732cd7eaa92ffeeffdbc2"
MODULES = {"numpy": "numpy", "pandas": "pandas", "torch": "torch", "torchvision": "torchvision",
           "scipy": "scipy", "scikit-learn": "sklearn", "h5py": "h5py", "lightning": "lightning",
           "pytorch-lightning": "pytorch_lightning", "torchmetrics": "torchmetrics", "pykale": "kale",
           "kalecancer": "kalecancer"}


def check_python() -> None:
    if sys.version_info[:2] != (3, 12):
        raise RuntimeError(
            f"The active kernel is Python {sys.version_info[0]}.{sys.version_info[1]}. "
            "KaleCancer and PyKale require Python below 3.13. In Colab choose Runtime > Change runtime type > "
            "Runtime Version > 2026.07 (Python 3.12), reconnect, then rerun this setup cell. "
            "If this runtime is not offered, use Run with Binder. Installing another interpreter does not change this kernel."
        )


def _pins(directory: Path) -> dict[str, str]:
    return dict(line.split("==", 1) for line in (directory / "colab-requirements.txt").read_text(encoding="utf-8").splitlines()
                if line and not line.startswith(("#", "--", " ")) and "==" in line)


def _matches(pins: dict[str, str]) -> bool:
    try:
        if any(metadata.version(name) != version for name, version in pins.items()):
            return False
        provenance = json.loads(metadata.distribution("kalecancer").read_text("direct_url.json") or "{}")
        return provenance.get("vcs_info", {}).get("commit_id") == CANCER_REF
    except (metadata.PackageNotFoundError, ValueError, OSError):
        return False


def _loaded_versions() -> dict[str, str]:
    # Inspect without importing: compiled libraries cannot be safely reloaded after pip changes them.
    return {package: str(getattr(sys.modules[module], "__version__", "unknown"))
            for package, module in MODULES.items() if module in sys.modules}


def _check_loaded(before: dict[str, str], pins: dict[str, str]) -> None:
    conflicts = [name for name, version in before.items() if name in pins and version != pins[name]]
    # The alpha version is the same across commits: require fresh imports if installation replaced it.
    if conflicts:
        raise RuntimeError(
            "Installed dependencies are ready, but this kernel still holds different versions of "
            + ", ".join(conflicts) + ". Choose Runtime > Restart session, then rerun the setup cell. "
            "Do not run the scientific cells until setup prints MDAS ready. Your notebook file is unchanged."
        )


def _ensure_helper(directory: Path) -> None:
    path = directory / "synthetic_data_generation.py"
    if path.is_file():
        return  # Never overwrite an existing repository's scientific helper.
    url = f"https://raw.githubusercontent.com/pykale/mdas/{DATA_REF}/notebooks/MDAS/cancer/{path.name}"
    with urlopen(Request(url, headers={"User-Agent": "MDAS-Colab"}), timeout=60) as response:
        contents = response.read()
    if hashlib.sha256(contents).hexdigest() != DATA_SHA256:
        raise RuntimeError("Companion-module checksum mismatch; downloaded code was not executed. Reopen the latest Colab copy.")
    temporary = path.with_suffix(".py.tmp")
    temporary.write_bytes(contents)
    temporary.replace(path)


def prepare(directory: Path | None = None) -> None:
    """Install in this kernel's interpreter and preserve the originals' cwd/imports."""
    check_python()  # Before installation or download.
    started = time.monotonic()
    directory = (directory or Path(__file__).resolve().parent).resolve()
    before = _loaded_versions()
    try:
        pins = _pins(directory)
        installed = False
        if not _matches(pins):
            print("MDAS: installing the pinned Python 3.12 CPU research dependencies. This may take several minutes.", flush=True)
            # Ordinary pip resolution: no --no-deps/--ignore-requires-python overrides.
            subprocess.run([sys.executable, "-m", "pip", "install", "--disable-pip-version-check",
                            "-r", str(directory / "colab-requirements.txt")], check=True)
            importlib.invalidate_caches()
            if not _matches(pins):
                raise RuntimeError("The installed packages do not match the research pins. Inspect the pip output and retry setup.")
            installed = True
        else:
            print("MDAS: compatible pinned dependencies already installed; reusing them.", flush=True)
        _check_loaded(before, pins)
        if installed and "kalecancer" in before:
            raise RuntimeError("KaleCancer was replaced while imported. Choose Runtime > Restart session and rerun setup.")
        _ensure_helper(directory)
        if str(directory) not in sys.path:
            sys.path.insert(0, str(directory))
        os.chdir(directory)
        importlib.invalidate_caches()
        import torch
        import numpy
        import pandas
        import h5py
        import kale
        from synthetic_data_generation import make_cohort
        from kalecancer.loaddata import Tabular, Classification, TimeToEvent, PatchFeatures, MultimodalDataset
        from kalecancer.model import ABMIL, Concat, ClassificationHead, CoxHead, IntermediateFusion, Unimodal
        from kalecancer.pipeline import Pipeline
        from kalecancer.evaluate import AUROC, BalancedAccuracy, HarrellC, UnoC, EvalContext, bootstrap_ci
        print(f"MDAS ready in {time.monotonic() - started:.1f}s: Python {sys.version.split()[0]}, PyTorch {torch.__version__}. Run the scientific cells below in order.", flush=True)
    except (subprocess.CalledProcessError, OSError, ImportError) as error:
        raise RuntimeError(
            f"MDAS setup failed: {error}. Check internet access and the pip/import output, then rerun setup. "
            "If packages were already imported, restart the session first. Use Run with Binder if the supported Colab runtime is unavailable."
        ) from error
