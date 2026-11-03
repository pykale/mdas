# Quick Start

Start with Cancer in a browser, or run a Cardiac example locally. Local commands belong in the corresponding **software repository**, not this MDAS documentation checkout.

## Cancer Quick Start

**Online:** [Open the Live-Coding Notebook](../notebooks/MDAS/cancer/classification.ipynb), choose Classification or Survival Analysis, then select Binder or Google Colab. Binder runs here; Colab opens a dedicated copy and requires a compatible Python 3.12 runtime and its initial setup cell.

### Optional local example

Use Python **3.11 or 3.12**, [uv](https://docs.astral.sh/uv/), and a checkout of [KaleCancer](https://github.com/pykale/cancer). From its repository root, the [repository quickstart](https://github.com/pykale/cancer/blob/main/docs/quickstart.md) provides:

```sh
uv sync --all-extras
uv run python examples/synthetic/synthetic_survival.py
```

This CPU-capable starter generates clinical variables, pathology patch features and censored survival times, then trains an intermediate-fusion Cox model. No patient dataset is required. The MDAS browser notebooks are a separate entry point with both classification and survival tasks.

## Cardiac Quick Start

Use Python **3.10, 3.11 or 3.12**. Install a [PyTorch build compatible with your hardware](https://pytorch.org/get-started/locally/), then follow the [KaleCardiac quickstart](https://github.com/pykale/cardiac/blob/main/docs/quickstart.md):

```sh
git clone https://github.com/pykale/cardiac.git
cd cardiac
pip install -e .
python -c "import kalecardiac, torch, kale; print(kalecardiac.__version__)"
```

The core install includes PyKale. Optional extras cover ECG file formats (`.[ecg]`), imaging (`.[imaging]`), interpretation (`.[interpret]`) and development (`.[dev]`); only add those your experiment needs. Avoid mixing a local checkout with an older installed package.

### CardioVAE: chest X-ray + ECG

```sh
python -m examples.cardiovae_multimodal.main --cfg examples/cardiovae_multimodal/configs/quick.yaml
```

### LS-EMVAE: multi-lead ECG

```sh
python -m examples.lsemvae_ecg.main --cfg examples/lsemvae_ecg/configs/quick.yaml
```

With no dataset path, these examples use generated cohorts. They can run on CPU and save configurations, predictions and metrics under `outputs/`; runtime depends on hardware. [Explore the Cardiac track](../tutorials/kalecardiac/getting-started.md) to understand the two examples and choose what to inspect.

Keep private data off public services. Synthetic scores are software checks, not clinical findings.
