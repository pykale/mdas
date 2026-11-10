# Quick Start

Choose a Cancer or Cardiac example and an execution route. Local commands belong in the corresponding **software repository**, not this MDAS documentation checkout.

## Cancer

### Run online

Open [KaleCancer Classification](../notebooks/MDAS/cancer/classification_showcase.ipynb) or [KaleCancer Survival Analysis](../notebooks/MDAS/cancer/survival_showcase.ipynb).

**Run with Binder** starts a temporary kernel on this website. **Run in Google Colab** opens the corresponding dedicated notebook in Colab. Follow [Execution Help](notebook-execution.md); Cancer Colab requires the documented **Python 3.12 / 2026.07** runtime and its initial setup cell, including any requested restart. This Colab requirement is separate from the local Python guidance below.

### Run locally

Use Python **3.11 or 3.12**, [uv](https://docs.astral.sh/uv/), and a checkout of [KaleCancer](https://github.com/pykale/cancer). Run these commands from the **KaleCancer repository root**, not the MDAS checkout. The [repository quickstart](https://github.com/pykale/cancer/blob/main/docs/quickstart.md) provides:

```sh
uv sync --all-extras
uv run python examples/synthetic/synthetic_survival.py
```

This CPU-capable starter generates clinical variables, pathology patch features and censored survival times, then trains an intermediate-fusion Cox model. No patient dataset is required. The MDAS browser notebooks are a separate entry point with both classification and survival tasks. To run those authored showcases locally, select the installed KaleCancer environment as your kernel in Jupyter or VS Code and open `classification_showcase.ipynb` or `survival_showcase.ipynb` from the **MDAS checkout's `notebooks/MDAS/cancer/` directory**. Keep both synthetic helper modules beside them and keep the kernel working in that directory so the authored imports and relative data paths remain valid.

## Cardiac

### Run online

Open [KaleCardiac CardioVAE](../notebooks/MDAS/cardiac/tutorial-CardioVAE.ipynb) or [KaleCardiac LS-EMVAE](../notebooks/MDAS/cardiac/tutorial-LSEMVAE.ipynb).

**Run in Google Colab** opens the corresponding notebook in Colab. Run the notebook's Step 0 installation and dataset cells in order; they install KaleCardiac with the required extras, fetch configurations and download the tutorial dataset (about 400 MB). For Colab, follow the compatible Python runtime guidance in Cardiac setup; a T4 GPU can accelerate training, and CPU execution is also supported. See [Cardiac setup instructions](notebook-execution.md#cardiac-setup).

### Run locally

Use Python **3.11 or 3.12**, the shared local recommendation for both tracks. Install a [PyTorch build compatible with your hardware](https://pytorch.org/get-started/locally/), then follow the [KaleCardiac quickstart](https://github.com/pykale/cardiac/blob/main/docs/quickstart.md):

```sh
git clone https://github.com/pykale/cardiac.git
cd cardiac
pip install -e .
python -c "import kalecardiac, torch, kale; print(kalecardiac.__version__)"
```

The commands above clone **KaleCardiac** and change into its repository root. Run the commands below from that same **cardiac repository root**.

The core install includes PyKale. Optional extras cover ECG file formats (`.[ecg]`), imaging (`.[imaging]`), interpretation (`.[interpret]`) and development (`.[dev]`); only add those your experiment needs. Avoid mixing a local checkout with an older installed package.

#### CardioVAE: chest X-ray + ECG

```sh
python -m examples.cardiovae_multimodal.main --cfg examples/cardiovae_multimodal/configs/quick.yaml
```

#### LS-EMVAE: multi-lead ECG

```sh
python -m examples.lsemvae_ecg.main --cfg examples/lsemvae_ecg/configs/quick.yaml
```

To run the full DICOM notebooks locally, install their required extras in the **cardiac repository root**:

```sh
pip install -e ".[imaging,interpret]"
```

Open `tutorials/mdas_tutorial/tutorial-CardioVAE.ipynb` or `tutorials/mdas_tutorial/tutorial-LSEMVAE.ipynb` in Jupyter or VS Code. Skip its package installation cell because this environment is already installed, and run the remaining cells, including the dataset download, in order. Keep the kernel working in `tutorials/mdas_tutorial/` so `configs/` and `data/` resolve beside the notebook. The imaging extra supplies DICOM reading and interpretation adds attribution tools. Keep generated checkpoints and logs separately from the source notebooks.

The two command-line examples above generate cohorts when no dataset path is configured; the DICOM notebooks use the downloaded tutorial dataset. They can run on CPU and save configurations, predictions and metrics under `outputs/`; runtime depends on hardware. [Explore the Cardiac track](../tutorials/kalecardiac/index.md) to understand the two examples and choose what to inspect.

Keep private data off public services. Synthetic scores are software checks, not clinical findings.
