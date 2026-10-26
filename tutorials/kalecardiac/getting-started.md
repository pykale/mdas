# Cardiac: Getting Started

## Two practical examples

| Example | Inputs | What it demonstrates |
| --- | --- | --- |
| **CardioVAE** | Chest X-ray + ECG | Multimodal representation learning and a cardiac endpoint |
| **LS-EMVAE** | Multi-lead ECG | Lead-specific representations, transfer to a subset of leads and endpoint prediction |

Both can generate synthetic cohorts when no data path is supplied. They are pipeline checks, not clinically validated experiments.

## Prepare the repository

Use the [KaleCardiac repository](https://github.com/pykale/cardiac) with **Python 3.10, 3.11 or 3.12**. Install a compatible PyTorch build first; the core installation includes PyKale. Follow the [Cardiac Quick Start](../../docs/quick-start.md#cardiac-quick-start) to obtain a checkout, then run from its root:

```sh
pip install -e .
python -c "import kalecardiac, torch, kale; print(kalecardiac.__version__)"
```

Optional extras cover ECG file formats (`.[ecg]`), imaging (`.[imaging]`), interpretation (`.[interpret]`) and development (`.[dev]`). Starter examples do not require participant datasets.

Avoid mixing the checkout with an older installed package. Confirm the supported session environment with the organisers before setup.

## Choose a synthetic example

### CardioVAE: chest X-ray + ECG

```sh
python -m examples.cardiovae_multimodal.main --cfg examples/cardiovae_multimodal/configs/quick.yaml
```

Continue to [CardioVAE Hands-on](cardiovae-hands-on.md).

### LS-EMVAE: multi-lead ECG

```sh
python -m examples.lsemvae_ecg.main --cfg examples/lsemvae_ecg/configs/quick.yaml
```

Continue to [LS-EMVAE Hands-on](lsemvae-hands-on.md).

The quickstart describes CPU-capable examples that write predictions, metrics and configuration records under `outputs/`. Exact runtime depends on hardware and dependencies.

## Results and technical references

See [Results and Interpretation](results.md). For experiment-specific requirements, consult the repository's [quickstart](https://github.com/pykale/cardiac/blob/main/docs/quickstart.md), [examples overview](https://github.com/pykale/cardiac/blob/main/examples/README.md), [CardioVAE README](https://github.com/pykale/cardiac/blob/main/examples/cardiovae_multimodal/README.md) and [LS-EMVAE README](https://github.com/pykale/cardiac/blob/main/examples/lsemvae_ecg/README.md).

> [!NOTE]
> The software continues to evolve. Final session exercise selection remains to be confirmed. Synthetic results are not clinical findings.
