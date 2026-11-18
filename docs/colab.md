---
orphan: true
---

# Run the Cancer notebooks in Google Colab

Open [Classification](../notebooks/MDAS/cancer/classification_showcase.ipynb), [Survival Analysis](../notebooks/MDAS/cancer/survival_showcase.ipynb) or [Exploring HANCOCK](../notebooks/MDAS/cancer/hancock_questions.ipynb), then select **Run in Google Colab**.

- [Classification in Google Colab](https://colab.research.google.com/github/pykale/mdas/blob/main/notebooks/MDAS/cancer/classification_showcase_colab.ipynb)
- [Survival Analysis in Google Colab](https://colab.research.google.com/github/pykale/mdas/blob/main/notebooks/MDAS/cancer/survival_showcase_colab.ipynb)
- [Exploring HANCOCK in Google Colab](https://colab.research.google.com/github/pykale/mdas/blob/main/notebooks/MDAS/cancer/hancock_questions_colab.ipynb)

Each Colab copy is the full notebook with one setup cell added at the top. That cell installs KaleCancer (Git commit `f8dff11372587c4ae97ce86b7d869ace511a6a17`) with pip and downloads the notebook's helper files from the public MDAS repository. Everything KaleCancer does not constrain keeps Colab's own version.

## Before running: Python 3.12

In Colab select **Runtime > Change runtime type**, set **Runtime version** to **2026.07** and click **Save**. Google lists this Python 3.12 runtime in its [runtime documentation](https://research.google.com/colaboratory/runtime-version-faq.html). KaleCancer and PyKale need Python below 3.13, so Colab's default Python 3.13 won't work; the setup cell stops with this instruction if the runtime is wrong. If the runtime is not offered, run locally with [Quick Start](quick-start.md#cancer).

Exploring HANCOCK can also use a **T4 GPU** (set under **Hardware accelerator** in the same dialog). It trains on the GPU, but its models are small, so it is only a little faster, and setup downloads a larger PyTorch. Classification and Survival Analysis run on the CPU.

## Run the notebook

1. Run the setup cell under **Before you start**. The first run takes about 6 minutes: KaleCancer needs PyTorch 2.6, so setup replaces Colab's newer PyTorch (with the smaller CPU-only build on a CPU runtime).
2. When it prints **Ready**, run the remaining cells in order.
3. Save a copy through Colab's File menu, and download any results through its Files pane, before disconnecting. Colab sessions are temporary.

## If setup fails

- **"KaleCancer needs Python 3.12"**: change the runtime version as above, then run the setup cell again.
- **"Installation failed"**: pip's messages are shown above it. A download error usually means the session lost its internet connection; reconnect and run the setup cell again.

For switching notebooks, temporary sessions and saving work, see [Execution Help](notebook-execution.md).
