# Jupyter notebooks

The Cancer [Classification](MDAS/cancer/classification_showcase.ipynb) and [Survival Analysis](MDAS/cancer/survival_showcase.ipynb) notebooks are in `notebooks/MDAS/cancer/`, alongside their `synthetic_data_generation.py` and `synthetic_showcase_data.py` helpers. View it on GitHub or open it in a Jupyter-compatible editor.

Open in Google Colab: [Classification](https://colab.research.google.com/github/pykale/mdas/blob/main/notebooks/MDAS/cancer/classification_showcase_colab.ipynb) or [Survival Analysis](https://colab.research.google.com/github/pykale/mdas/blob/main/notebooks/MDAS/cancer/survival_showcase_colab.ipynb). The first cell of each Colab copy sets up the environment and helpers.

## Cancer hands-on: Exploring HANCOCK

[Exploring HANCOCK](MDAS/cancer/hancock_questions.ipynb) asks research questions on the real, public [HANCOCK](https://hancock.research.fau.eu) head and neck cancer cohort, in three levels from "change a value" to "write your own encoder". [Open it in Google Colab](https://colab.research.google.com/github/pykale/mdas/blob/main/notebooks/MDAS/cancer/hancock_questions_colab.ipynb).

Participants don't download anything from the HANCOCK website. `hancock_data.py` fetches a reduced bundle (about 190 MB) from a Dropbox shared link, checks its SHA-256 and unpacks it into `data/`. To use a copy on a shared drive or USB stick instead, set `MDAS_HANCOCK_ZIP` to its path.

Organisers rebuild the bundle from the full download with `prepare_hancock_bundle.py`. The build is deterministic, so the checksum in `hancock_data.py` stays valid. To host it elsewhere, upload `data/hancock_mdas_v1.zip` and set `URL` in `hancock_data.py` to a direct-download link (for Dropbox, end the shared link with `dl=1`).

```sh
uv run python notebooks/MDAS/cancer/prepare_hancock_bundle.py --hancock ~/datasets/HANCOCK/raw
```

The Cardiac tutorial notebooks, [CardioVAE](MDAS/cardiac/tutorial-CardioVAE.ipynb) and [LS-EMVAE](MDAS/cardiac/tutorial-LSEMVAE.ipynb), are in `notebooks/MDAS/cardiac/` with their `configs/` folder. See the [Cardiac tutorial](../tutorials/kalecardiac/getting-started.md) to choose and run one.

> [!CAUTION]
> Synthetic results are not clinical evidence. Do not upload identifiable patient data, confidential material or private datasets to public services or this repository.
