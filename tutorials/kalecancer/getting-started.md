# Cancer: Getting Started

## Research question

How can clinical features and pathology patch features be combined to explore time-to-event prediction? The starter example trains an **intermediate-fusion Cox model** using a small synthetic cohort.

No real patient data are needed. Real-data HANCOCK examples require separate dataset access and additional setup.

## Prepare the repository

Use the [KaleCancer repository](https://github.com/pykale/cancer), Python **3.11 or 3.12**, and **uv**. From the repository root, follow its [quickstart](https://github.com/pykale/cancer/blob/main/docs/quickstart.md):

```sh
uv sync --all-extras
```

The public repository contains the example paths below. Confirm the session environment with the organisers before installing; these documentation checks do not replace testing the dependencies on your machine.

## Run the synthetic example

```sh
uv run python examples/synthetic/synthetic_survival.py
```

This CPU-capable, no-download demonstration generates clinical variables, pathology patch features and censored survival times, then trains the model.

The repository also provides [an equivalent synthetic example notebook](https://github.com/pykale/cancer/blob/main/examples/synthetic/synthetic_survival.ipynb). The session's [Live-Coding Notebook](../../notebooks/MDAS/cancer/cancer_live_coding.ipynb) is available here with its saved outputs and a Colab link.

## What to look for

- How the synthetic cohort is assembled.
- Which clinical and patch inputs are used.
- Where intermediate fusion occurs.
- Which evaluation metrics are printed.

## Continue the track

1. [Hands-on Tutorial](hands-on.md): locate the synthetic inputs and identify the prediction task.
2. [Live-Coding Notebook](../../notebooks/MDAS/cancer/cancer_live_coding.ipynb): follow data loading, modelling, training and evaluation.
3. [Results and Interpretation](results.md): understand the output and limits of a synthetic survival exercise.

## Technical references

Within the software repository, consult [README.md](https://github.com/pykale/cancer/blob/main/README.md), [docs/quickstart.md](https://github.com/pykale/cancer/blob/main/docs/quickstart.md), [examples/synthetic/synthetic_survival.py](https://github.com/pykale/cancer/blob/main/examples/synthetic/synthetic_survival.py), and [examples/hancock/](https://github.com/pykale/cancer/tree/main/examples/hancock).

For library support, use [PyKale discussions](https://github.com/pykale/pykale/discussions) or the repository's issue tracker.

> [!IMPORTANT]
> Synthetic scores are pipeline checks, not evidence of clinical predictive performance. Clinical data require appropriate permissions and secure infrastructure.
