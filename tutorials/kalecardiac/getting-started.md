# KaleCardiac: getting started

Set up KaleCardiac and choose a synthetic example below. For a shorter route, see the [Quick Start](../../docs/quick-start.md).

## Prepare the snapshot

Use the **`cardiac-main` development snapshot** and run commands from its repository root, with **Python 3.10, 3.11 or 3.12**. Install a compatible PyTorch build and PyKale first, following their installation guidance.

```sh
pip install -e .
python -c "import kalecardiac, torch, kale; print(kalecardiac.__version__)"
```

Optional extras are documented for ECG file formats (`.[ecg]`), imaging (`.[imaging]`), interpretation (`.[interpret]`) and development (`.[dev]`). The starter synthetic examples do not require participant datasets.

## Choose a synthetic example

### CardioVAE: chest X-ray + ECG

```sh
python -m examples.cardiovae_multimodal.main --cfg examples/cardiovae_multimodal/configs/quick.yaml
```

Continue to [CardioVAE hands-on](cardiovae-hands-on.md).

### LS-EMVAE: multi-lead ECG

```sh
python -m examples.lsemvae_ecg.main --cfg examples/lsemvae_ecg/configs/quick.yaml
```

Continue to [LS-EMVAE hands-on](lsemvae-hands-on.md).

The `cardiac-main` quickstart describes CPU-capable examples that write predictions, metrics and configuration records under `outputs/`. Exact runtime depends on hardware and dependencies.

> [!WARNING]
> Run these commands from the `cardiac-main` development snapshot, not this documentation repository. Avoid mixing it with an older installed KaleCardiac version. Compatibility with the current public default branch is not guaranteed; confirm the session revision with the organisers.

[About KaleCardiac](README.md) · [Results and interpretation](results.md) · [Prerequisites](../../docs/prerequisites.md).
