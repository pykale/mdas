# KaleCancer: getting started

## Prepare the repository

Use the **`cancer-refactor` development snapshot**. Compatibility with the public default branch is not guaranteed. From the `cancer-refactor` repository root, with **Python 3.11 or 3.12** and **uv** installed:

```sh
uv sync --all-extras
```

## Run the synthetic example

```sh
uv run python examples/synthetic/synthetic_survival.py
```

The repository describes this as a CPU-capable, no-download demonstration. It generates a cohort with clinical variables, pathology patch features and censored survival times, and trains an intermediate-fusion Cox model.

The `cancer-refactor` snapshot documents an equivalent notebook at `examples/synthetic/synthetic_survival.ipynb`. Session notebooks are not yet available in this repository; see [notebook availability](../../notebooks/README.md).

## What to look for

- How the synthetic cohort is assembled.
- Which clinical and patch inputs are used.
- Where intermediate fusion occurs.
- Which evaluation metrics are printed.

> [!WARNING]
> These commands require the `cancer-refactor` development snapshot. Confirm the session revision and supported environment with the organisers before installing.

[About KaleCancer](README.md) · [Hands-on activity](hands-on.md) · [Results](results.md).
