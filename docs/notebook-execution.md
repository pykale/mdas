---
orphan: true
---

# Online notebook execution

The [Cancer Live-Coding Notebook](../notebooks/MDAS/cancer/classification.ipynb) offers **Classification** (default) and **Survival Analysis** in the **Choose a notebook** dropdown. Each selection opens its own documentation page with the selected notebook's cells, contents and launch links. Both can be read as a static page, connected to a temporary Binder kernel through Thebe, or opened in Google Colab. No code is run by opening the documentation page.

## Run on this website

Choose **Run with Binder** and wait for the connection status to show that the kernel is connected. The first Binder build may take several minutes. Code cells become editable, and you can run them individually, in order. A connection alone does not execute the notebook or verify that every research dependency works.

The kernel is configured to start in `notebooks/MDAS/cancer/`, so the companion `synthetic_data_generation.py` module can be imported. Both notebooks' `../../../data/synthetic_data` path resolves to `data/synthetic_data` inside the temporary repository checkout. The helper generates synthetic data there; no patient dataset is needed.

Binder uses the repository on GitHub, not your local checkout. The organiser has confirmed a successful remote launch and Thebe kernel connection after publishing the Binder configuration. A subsequent complete execution test passed all original Classification and Survival code cells; see the [notebook validation report](https://github.com/pykale/mdas/blob/main/notebooks/MDAS/cancer/README-colab.md). This does not establish direct Colab UI compatibility.

## Switch notebooks and save edits

Switching loads a new page and starts with its saved cells; kernels and variables are not transferred. After interactive launch, switching asks for confirmation. Cancel to stay on the current page and choose **Download notebook with edits** before leaving. The download includes current code edits and original Markdown, with outputs cleared; it does not include kernel variables or generated files. Check that the download succeeded. Copy important results or download generated files separately. Reloading, closing the tab and following documentation links also trigger the browser's leave-page warning after launch.

Each notebook links its corresponding `_blank.ipynb` as an **Optional blank exercise** on GitHub. These exercise notebooks are not the displayed defaults.

## Connection troubleshooting

If the launch reports **No environment specification found**, Binder has not reached package installation or kernel startup. It cannot see a usable environment definition in the selected public revision. Installing more packages locally does not fix that remote failure.

The launch control now checks the public revision for `.binder/runtime.txt`, `.binder/requirements.txt`, the notebook and its companion module **before requesting Binder**. If files are absent, the status names them and explains that local files are not sent to Binder. Once present, it launches the exact commit checked. A GitHub API timeout, blocked request or rate limit is reported separately and is not treated as evidence that packages failed to install.

Open the **Binder build logs** link on the notebook page to distinguish repository retrieval, environment discovery/build, server launch and kernel connection. A generic Thebe `failed` status alone does not identify the stage. A successful environment-file check is not a guarantee that the image or kernel will work.

The earlier revision `ed163a322186055c8c5b79885288ad9a051f89c4` lacked Binder files. The organiser subsequently published them in `090f1ff68a57cd2f04ab1df9008fd802e6caa278` and confirmed a ready server and working Thebe connection. See the maintainer build guide for diagnostics; a future failure still needs its actual launch stage checked.

## Open in Google Colab

Use the **Run in Google Colab** button on the selected notebook page: [Classification](https://colab.research.google.com/github/pykale/mdas/blob/main/notebooks/MDAS/cancer/classification_colab.ipynb) or [Survival Analysis](https://colab.research.google.com/github/pykale/mdas/blob/main/notebooks/MDAS/cancer/survival_colab.ipynb).

Each link opens a dedicated Colab copy with an initial **Google Colab Environment Setup** section. Select the supported Python 3.12 runtime, run setup, then run the scientific cells directly in that notebook. The [Colab runtime guide](colab.md) explains runtime selection and a possible session restart if incompatible libraries are already imported. All original scientific cells are preserved in the copies; Binder continues to use the original notebooks.

## Compute and privacy limits

The helper defaults to 100 synthetic subjects and 20–199 patches per subject, each with 32 features. That feature data is small, but importing the ML stack, training for 40 epochs, fitting the optional baseline and computing bootstrap intervals need additional memory and CPU time. Measured full-run timings are recorded in the [validation report](https://github.com/pykale/mdas/blob/main/notebooks/MDAS/cancer/README-colab.md); memory use and public-service completion times are not guaranteed. Run training deliberately; avoid repeated or simultaneous advanced runs.

Binder resources are limited and sessions are temporary; availability and completion are not guaranteed. Download work you need to keep: edits and generated files in temporary online sessions may be lost.

> [!CAUTION]
> Never upload identifiable patient data, confidential research data, private datasets, credentials or other secrets to public execution services. Synthetic workflow scores are not clinical evidence.
