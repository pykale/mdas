# Quick Start

Choose a track and use its own environment. Run the commands from the corresponding software repository root, not this documentation repository. The linked public repository files contain these commands; confirm the session environment with the organisers before running them.

## Cancer Quick Start

**Repository:** [KaleCancer](https://github.com/pykale/cancer). Use Python **3.11 or 3.12** and [uv](https://docs.astral.sh/uv/). From a local checkout, follow the [repository quickstart](https://github.com/pykale/cancer/blob/main/docs/quickstart.md):

```sh
uv sync --all-extras
uv run python examples/synthetic/synthetic_survival.py
```

The [synthetic example](https://github.com/pykale/cancer/blob/main/examples/synthetic/synthetic_survival.py) generates clinical variables, pathology patch features and censored survival times, then trains an intermediate-fusion Cox model. It is a CPU-capable, no-download starter exercise.

Continue with [Cancer Getting Started](../tutorials/kalecancer/getting-started.md), the [Hands-on Tutorial](../tutorials/kalecancer/hands-on.md), or the [Live-Coding Notebook](../notebooks/MDAS/cancer/classification.ipynb). The live-coding notebook imports the accompanying `synthetic_data_generation.py`; review its access notes before attempting local or Colab execution.

## Cardiac Quick Start

**Repository:** [KaleCardiac](https://github.com/pykale/cardiac). Use Python **3.10, 3.11 or 3.12**. Install a [PyTorch build compatible with your hardware](https://pytorch.org/get-started/locally/), then follow the [repository quickstart](https://github.com/pykale/cardiac/blob/main/docs/quickstart.md):

```sh
git clone https://github.com/pykale/cardiac.git
cd cardiac
pip install -e .
python -c "import kalecardiac, torch, kale; print(kalecardiac.__version__)"
```

The core install includes PyKale. Optional extras cover ECG file formats (`.[ecg]`), imaging (`.[imaging]`), interpretation (`.[interpret]`) and development (`.[dev]`). The starter examples need no participant dataset.

### CardioVAE: chest X-ray + ECG

```sh
python -m examples.cardiovae_multimodal.main --cfg examples/cardiovae_multimodal/configs/quick.yaml
```

[CardioVAE Hands-on](../tutorials/kalecardiac/cardiovae-hands-on.md).

### LS-EMVAE: multi-lead ECG

```sh
python -m examples.lsemvae_ecg.main --cfg examples/lsemvae_ecg/configs/quick.yaml
```

[LS-EMVAE Hands-on](../tutorials/kalecardiac/lsemvae-hands-on.md).

These examples can run on CPU and save predictions, metrics and configuration records under `outputs/`. Runtime depends on hardware and dependencies. Avoid mixing the local checkout with an older installed package.

> [!IMPORTANT]
> Synthetic runs check the pipeline; their scores are not clinical results. Use real clinical data only with appropriate permissions and secure infrastructure, and never upload identifiable or confidential data to public services.
