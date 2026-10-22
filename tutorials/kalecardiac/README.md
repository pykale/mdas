# KaleCardiac

## Two practical examples

The `cardiac-main` development snapshot provides two synthetic-cohort workflows:

| Example | Inputs | What it demonstrates |
| --- | --- | --- |
| **CardioVAE** | Chest X-ray + ECG | Multimodal representation learning and a cardiac endpoint |
| **LS-EMVAE** | Multi-lead ECG | Lead-specific representations, transfer to a subset of leads and endpoint prediction |

Both examples can generate synthetic cohorts when no data path is supplied. They are **pipeline checks**, not clinically validated experiments.

## Suggested route

1. [Getting started](getting-started.md)
2. [CardioVAE hands-on](cardiovae-hands-on.md)
3. [LS-EMVAE hands-on](lsemvae-hands-on.md)
4. [Results and interpretation](results.md)

> [!WARNING]
> **Under development:** These tutorials use the `cardiac-main` development snapshot. Features, configurations and outputs may change before the session. Session-day support and final exercise selection are still to be confirmed.

**Technical references in `cardiac-main`:** `README.md`, `docs/quickstart.md`, `examples/README.md` and the example-specific READMEs. These paths are relative to the KaleCardiac repository root.

[Tutorials overview](../README.md) · [Notebooks](../../notebooks/README.md) · [Resources](../../docs/resources.md).
