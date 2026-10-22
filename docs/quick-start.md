# Quick Start

The source Quick Start covers KaleCardiac. For the other track, see [KaleCancer getting started](../tutorials/kalecancer/getting-started.md). Review the [prerequisites](prerequisites.md) before setup.

## Installation

The uploaded cardiac quickstart supports **Python 3.10, 3.11 and 3.12**. Install a compatible PyTorch build and PyKale first, following their installation guidance. From the extracted **`cardiac-main` repository root**:

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

The uploaded quickstart says these synthetic examples run on CPU and write predictions, metrics and configuration records under `outputs/`. Exact runtime depends on hardware and dependencies.

> [!WARNING]
> These commands come from `cardiac-main/docs/quickstart.md`; they have not been independently executed here. If using the uploaded ZIP offline, extract it first and run commands from its root. Avoid mixing it with an older installed KaleCardiac version.

> [!IMPORTANT]
> Synthetic examples are pipeline checks, not evidence of clinical performance.

Source: PDF pages 2–3. See [resources](resources.md) for snapshot references and [KaleCardiac getting started](../tutorials/kalecardiac/getting-started.md).
