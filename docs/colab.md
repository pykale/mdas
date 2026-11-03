---
orphan: true
---

# Prepare a Google Colab environment

The four original Cancer notebooks are unchanged. Opening an original notebook in Colab does not retrieve its companion module, install research packages, or arrange its working directory. Colab notebooks opened independently do not automatically share a runtime, packages, files, or kernel state. Preparing a separate notebook cannot silently prepare another tab.

Use [Prepare Colab Environment](https://colab.research.google.com/github/pykale/mdas/blob/main/colab/prepare_colab.ipynb) to **execute the original unchanged** from a repository checkout in that preparation session. It runs every code cell, including training and advanced analysis, and produces downloadable executed copies and HTML reports. It does not turn a separately opened original notebook into a prepared interactive runtime. For editing and running individual cells in the original tutorial page, use the website's Binder option.

## Select a supported runtime

In the preparation notebook choose **Runtime → Change runtime type → Runtime Version → 2026.07**, then reconnect. Verify that the actual kernel is **Python 3.12**. CPU is sufficient; the scientific notebooks explicitly train on CPU.

Google documents Python 3.13 for runtime 2026.10, and Python 3.12 for 2026.07. Both the pinned KaleCancer and PyKale releases require Python below 3.13. PyKale also requires PyTorch at most 2.6; KaleCancer requires at least 2.6. Installing another Python executable in a cell does not change the Colab kernel's Python version. This workflow checks the actual kernel version and stops on an unsupported version rather than ignoring package constraints.

The preparation notebook creates a **separate Python 3.12 virtual environment** with PyTorch 2.6 CPU and the pinned research requirements. It then starts explicit notebook kernels with that environment's interpreter. Colab's host kernel and preinstalled PyTorch are left intact. Dependency isolation avoids breaking Colab's own installed packages.

Past Colab runtimes have a limited availability window. If Python 3.12 is no longer offered, use Binder; this workflow does not claim support for Python 3.13. See [Google's runtime version documentation](https://research.google.com/colaboratory/runtime-version-faq.html).

## Prepare and execute

1. Open **Prepare Colab Environment**, select the supported runtime, then run its checkout and preparation cells. The first run clones the public `pykale/mdas` repository and installs the isolated dependencies. No file upload or Drive mount is required.
2. In its notebook selector choose `classification`, `survival`, or `both`, and run the execution cell. Each notebook gets its own fresh kernel. Every code cell runs in its original order; epochs, model definitions, evaluation and advanced analyses are preserved.
3. Run the download cell to save the executed notebook copy, HTML report, timings and source checksum. These files are separate results, not replacements for the source notebooks.
4. To run the other notebook, change the selector and rerun the execution cell. The checkout and matching installation are reused; a fresh kernel prevents hidden state from the previous notebook.

The checkout follows `main` **once per fresh session** and records the resolved commit. Rerunning does not update it or reclone. This keeps notebooks, helper and requirements on one revision throughout the session. For reproducibility, record the printed commit and execution report. A future fresh session may obtain a newer reviewed `main` revision.

Each worker starts in `notebooks/MDAS/cancer/`. This makes `synthetic_data_generation.py` importable and preserves the original `../../../data/synthetic_data` path. The original cells generate the correct classification or survival cohort; sequential reruns deterministically replace files at the same path instead of creating duplicate datasets. Do not execute two workers simultaneously against the same checkout: the originals share a synthetic-data directory. The optional blank survival exercise retains its authored `./data/synthetic/` path. Blank notebooks are exercises with intentionally omitted scientific code, not candidates for automatic full execution.

## Original notebook links

The website's **Open in Google Colab** and **View on GitHub** links continue to target the original files:

- [Classification in Colab](https://colab.research.google.com/github/pykale/mdas/blob/main/notebooks/MDAS/cancer/classification.ipynb)
- [Survival Analysis in Colab](https://colab.research.google.com/github/pykale/mdas/blob/main/notebooks/MDAS/cancer/survival.ipynb)

They remain reading/source links when opened in a separate runtime. Google Colab cannot automatically run a repository bootstrap before the first cell of an unchanged notebook, or guarantee that an independently opened notebook will attach to this preparation session. Fully automatic interactive execution in the original Colab tab would require changing its setup cells or manually configuring that tab's runtime. The external runner avoids modifying the scientific notebooks.

## Limits and validation

Initial CPU-library downloads may take several minutes. Training and bootstrap analysis run in full, so wait for each cell's progress report. The runner stops on the first error and saves a partial execution copy/report; it never treats skipped or failed scientific cells as success. Download results before the temporary Colab session ends. Use synthetic data only.

Direct Colab UI execution has not been verified in this development environment. The [maintainer validation report](https://github.com/pykale/mdas/blob/main/colab/README.md) distinguishes actual notebook execution tests, dependency checks and remaining manual checks. The new preparation notebook and support files must be reviewed and published together before their public links can work. No publication is performed by this change.
