# KaleCardiac: getting started

The PDF does not contain a separate KaleCardiac getting-started page. Its [Quick Start](../../docs/quick-start.md) provides the setup and commands reproduced here for this tutorial route.

## Prepare the snapshot

Use the extracted **`cardiac-main` repository root**, with **Python 3.10, 3.11 or 3.12**. Install a compatible PyTorch build and PyKale first, following their installation guidance.

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

The uploaded quickstart says these examples run on CPU and write predictions, metrics and configuration records under `outputs/`. Exact runtime depends on hardware and dependencies.

> [!WARNING]
> These commands come from `cardiac-main/docs/quickstart.md`; they have not been independently executed here. If using the uploaded ZIP offline, extract it first and run commands from its root. Avoid mixing it with an older installed KaleCardiac version. Do not assume these commands work on the current public default branch.

Source: PDF pages 2–3. [About KaleCardiac](README.md) · [Results and interpretation](results.md) · [Prerequisites](../../docs/prerequisites.md).
