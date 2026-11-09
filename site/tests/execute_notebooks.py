"""Validation-only execution of original or direct Colab notebooks in fresh kernels."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
import time


def execute(name: str, root: Path, output: Path, timeout: int = 1200, variant: str = "original") -> dict:
    import nbformat
    from nbclient import NotebookClient
    from nbconvert import HTMLExporter
    from jupyter_client import KernelManager
    from jupyter_client.kernelspec import KernelSpecManager

    if name not in {"classification", "survival", "classification_showcase", "survival_showcase", "tutorial-CardioVAE", "tutorial-LSEMVAE"}:
        raise ValueError("Choose a complete Cancer or Cardiac tutorial notebook.")
    stem = name + ("_colab" if variant == "colab" else "")
    track = "cardiac" if name.startswith("tutorial-") else "cancer"
    if track == "cardiac" and variant != "original":
        raise ValueError("Cardiac notebooks run directly; no generated Colab variant is used.")
    source = root / "notebooks" / "MDAS" / track / f"{stem}.ipynb"
    source_bytes = source.read_bytes()
    notebook = nbformat.reads(source_bytes.decode("utf-8"), as_version=4)
    # This affects the execution copy only; source bytes/metadata/outputs are never written.
    for cell in notebook.cells:
        if cell.cell_type == "code":
            cell.outputs = []
            cell.execution_count = None
    output.mkdir(parents=True, exist_ok=True)
    # A failed rerun must not leave an earlier successful HTML report beside it.
    (output / f"{stem}.html").unlink(missing_ok=True)
    # Explicit interpreter argv: no reliance on a global/Colab 'python3' kernel spec.
    spec_root = output / ".kernels"
    spec = spec_root / "mdas-colab"
    spec.mkdir(parents=True, exist_ok=True)
    (spec / "kernel.json").write_text(json.dumps({
        "argv": [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
        "display_name": "MDAS isolated Python 3.12", "language": "python",
    }), encoding="utf-8")
    manager = KernelManager(ip="127.0.0.1", kernel_name="mdas-colab", kernel_spec_manager=KernelSpecManager(kernel_dirs=[str(spec_root)]))
    cell_times = []
    started = time.monotonic()
    cell_started = started

    def begin(cell, cell_index):
        nonlocal cell_started
        cell_started = time.monotonic()
        print(f"{name}: executing cell {cell_index + 1}/{len(notebook.cells)}", flush=True)

    def complete(cell, cell_index, execute_reply):
        cell_times.append({"index": cell_index, "seconds": round(time.monotonic() - cell_started, 3),
                           "status": execute_reply["content"]["status"]})

    # Validation must execute authored setup/download cells even when tagged
    # skip-execution for automated documentation builds. Source metadata is untouched.
    client = NotebookClient(notebook, km=manager, timeout=timeout, allow_errors=False, skip_cells_with_tag="",
                            resources={"metadata": {"path": str(source.parent)}},
                            on_cell_execute=begin, on_cell_executed=complete)
    result = {"notebook": stem, "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
              "python": sys.version, "executable": sys.executable, "working_directory": str(source.parent),
              "cells": cell_times}
    try:
        client.execute(cleanup_kc=True, cwd=str(source.parent))
        expected = sum(cell.cell_type == "code" and bool(cell.source.strip()) for cell in notebook.cells)
        if len(cell_times) != expected or any(cell["status"] != "ok" for cell in cell_times):
            raise RuntimeError("Not every original code cell completed successfully.")
        result["status"] = "passed"
    except Exception as error:
        result["status"] = "failed"
        result["error"] = f"{type(error).__name__}: {error}"
        raise
    finally:
        # A supplied KernelManager is externally owned: explicitly stop its kernel.
        if manager.has_kernel:
            manager.shutdown_kernel(now=True)
        result["seconds"] = round(time.monotonic() - started, 2)
        result["source_unchanged"] = source.read_bytes() == source_bytes
        if not result["source_unchanged"]:
            result["status"] = "failed"
            result["error"] = "Source notebook changed during execution"
        nbformat.write(notebook, output / f"{stem}.executed.ipynb")
        (output / f"{stem}.execution.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
        if not result["source_unchanged"]:
            raise RuntimeError("Source notebook changed during execution; investigate before continuing.")
    html, _ = HTMLExporter().from_notebook_node(notebook)
    (output / f"{stem}.html").write_text(html, encoding="utf-8")
    print(f"{name}: all {len(cell_times)} code cells passed in {result['seconds']:.1f}s; source unchanged.", flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notebook", choices=["classification", "survival", "classification_showcase", "survival_showcase", "tutorial-CardioVAE", "tutorial-LSEMVAE", "both"])
    parser.add_argument("--variant", choices=["original", "colab"], default="colab")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--timeout", type=int, default=1200, help="Timeout per code cell, in seconds")
    args = parser.parse_args()
    root = args.root.resolve()
    output = (args.output or root / "outputs" / "colab-validation").resolve()
    if output.is_relative_to(root / "notebooks"):
        parser.error("Output must be outside the source notebooks directory.")
    if sys.version_info[:2] != (3, 12):
        parser.error("Run this worker with the prepared Python 3.12 interpreter.")
    for name in (["classification", "survival"] if args.notebook == "both" else [args.notebook]):
        execute(name, root, output, args.timeout, args.variant)


if __name__ == "__main__":
    main()
