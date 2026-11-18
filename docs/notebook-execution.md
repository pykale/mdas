---
orphan: true
---

# Execution Help

This guide opens in a new tab so your notebook page and active kernel can stay in place. Choose the notebook first, then one execution route. Reading the saved cells alone does not run code.

## Colab: run the dedicated copy

**Run in Google Colab** opens a copy of the notebook with one setup cell added at the top: `classification_showcase_colab.ipynb` for Classification, `survival_showcase_colab.ipynb` for Survival Analysis and `hancock_questions_colab.ipynb` for Exploring HANCOCK. For local execution, see [Quick Start](quick-start.md#cancer). See the [Colab guide](colab.md) for details.

1. Select the **Python 3.12** runtime as explained at the top of that notebook (**Runtime > Change runtime type**, runtime version **2026.07**).
2. Run the setup cell. It installs KaleCancer and downloads the notebook's helper files. The first run takes about 6 minutes.
3. When it prints **Ready**, run the remaining cells in order.
4. Save a notebook copy and download needed results using Colab's File menu and Files pane before disconnecting. A new Colab session does not keep an earlier session's files or variables.

If the setup cell stops with a message, follow it, or see the [Colab guide](colab.md). Don't skip ahead to the other cells until setup prints **Ready**.

## Cardiac setup

Open the [Chest X-ray and ECG](../notebooks/MDAS/cardiac/tutorial-CardioVAE.ipynb) or [12-lead ECG](../notebooks/MDAS/cardiac/tutorial-LSEMVAE.ipynb) tutorial. **Run in Google Colab** opens that authored notebook in Colab; its own Step 0 prepares the environment.

1. Run the package installation cell. It installs KaleCardiac from PyPI with the extras the tutorials need, `kalecardiac[imaging,interpret]`. Each configuration cell later downloads the configuration file it reads.
2. Run the dataset cell. It downloads and extracts about **400 MB** of public tutorial DICOM data. The unlabelled cohort is for pretraining; the labelled cohort is for fine-tuning. Both examples can reuse this data in a shared folder.
3. Run the remaining cells in order. Each tutorial loads separate pretraining and fine-tuning configuration files; its notebook cells expose settings to explore. Checkpoints and training logs are written in separate output folders.
4. For Cardiac Colab, use a compatible Python 3.12 runtime where offered; that is the Python version used in the local shared-environment checks. A T4 GPU can accelerate training, while CPU execution also works. The current default Colab runtime has not been verified here. If a compatible runtime is unavailable, use Run locally; installing another interpreter does not change the kernel. Resolve any installation error before proceeding.

For **Run locally**, use [Quick Start](quick-start.md#cardiac). Do not mix a local checkout and an older installed copy. Public services must use only the tutorial data; save work before leaving a temporary session.

## Privacy and interpretation

Use synthetic data only on public execution services. Do not upload identifiable patient data, confidential research, private datasets or credentials. Synthetic metrics demonstrate a workflow, not clinical usefulness.
