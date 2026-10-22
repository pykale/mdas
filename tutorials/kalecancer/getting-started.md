# KaleCancer: getting started

## Prepare the repository

Use the uploaded **refactor checkout**, not an unspecified `main` branch clone. From the extracted `cancer-refactor` repository root, with **Python 3.11 or 3.12** and **uv** installed:

```sh
uv sync --all-extras
```

## Run the synthetic example

```sh
uv run python examples/synthetic/synthetic_survival.py
```

The repository describes this as a CPU-capable, no-download demonstration. It generates a cohort with clinical variables, pathology patch features and censored survival times, and trains an intermediate-fusion Cox model.

The source says an equivalent notebook is provided at `examples/synthetic/synthetic_survival.ipynb` **in the refactor snapshot**. That notebook has not been supplied to this documentation repository; see [notebook availability](../../notebooks/README.md).

## What to look for

- How the synthetic cohort is assembled.
- Which clinical and patch inputs are used.
- Where intermediate fusion occurs.
- Which evaluation metrics are printed.

> [!WARNING]
> These instructions are transcribed from the uploaded refactor README and quickstart. They have not been run in a clean session environment as part of preparing this documentation.

Source: PDF page 17. [About KaleCancer](README.md) · [Hands-on activity](hands-on.md) · [Results](results.md).
