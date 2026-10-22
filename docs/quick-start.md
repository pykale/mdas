# Quick Start

This Quick Start covers KaleCardiac. For the other track, see [KaleCancer getting started](../tutorials/kalecancer/getting-started.md). Review the [prerequisites](prerequisites.md) before setup.

## Installation

The `cardiac-main` development snapshot supports **Python 3.10, 3.11 and 3.12**. Install a compatible PyTorch build and PyKale first, following their installation guidance. From the **`cardiac-main` repository root**:

```sh
pip install -e .
python -c "import kalecardiac, torch, kale; print(kalecardiac.__version__)"
```

Optional extras are documented for ECG file formats (`.[ecg]`), imaging (`.[imaging]`), interpretation (`.[interpret]`) and development (`.[dev]`). The starter synthetic examples do not require participant datasets.

## Choose an example

### Chest X-ray + ECG (CardioVAE)

```sh
python -m examples.cardiovae_multimodal.main --cfg examples/cardiovae_multimodal/configs/quick.yaml
```

See [CardioVAE hands-on](../tutorials/kalecardiac/cardiovae-hands-on.md).

### Multi-lead ECG (LS-EMVAE)

```sh
python -m examples.lsemvae_ecg.main --cfg examples/lsemvae_ecg/configs/quick.yaml
```

See [LS-EMVAE hands-on](../tutorials/kalecardiac/lsemvae-hands-on.md).

The `cardiac-main` quickstart describes CPU-capable synthetic examples that write predictions, metrics and configuration records under `outputs/`. Exact runtime depends on hardware and dependencies.

> [!WARNING]
> Run these commands from the `cardiac-main` development snapshot, not this documentation repository. Avoid mixing it with an older installed KaleCardiac version. Compatibility with the current public default branch is not guaranteed; confirm the session revision with the organisers.

> [!IMPORTANT]
> Synthetic examples are pipeline checks, not evidence of clinical performance.

[Resources](resources.md) · [KaleCardiac getting started](../tutorials/kalecardiac/getting-started.md).
