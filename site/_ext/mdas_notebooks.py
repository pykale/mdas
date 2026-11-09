"""Shared mapping between documentation pages and their tutorial notebooks."""

CANCER = "notebooks/MDAS/cancer"
NOTEBOOKS = {
    "tutorials/kalecancer/live-coding": ("Classification", f"{CANCER}/classification_showcase.ipynb"),
    "tutorials/kalecancer/live-coding-survival": ("Survival Analysis", f"{CANCER}/survival_showcase.ipynb"),
}

CARDIAC = "notebooks/MDAS/cardiac"
CARDIAC_NOTEBOOKS = {
    "tutorials/kalecardiac/live-coding": ("CardioVAE", f"{CARDIAC}/tutorial-CardioVAE.ipynb"),
    "tutorials/kalecardiac/live-coding-lsemvae": ("LS-EMVAE", f"{CARDIAC}/tutorial-LSEMVAE.ipynb"),
}

# Every staged notebook page, and the canonical (sidebar) page of each non-default one.
ALL_NOTEBOOKS = {**NOTEBOOKS, **CARDIAC_NOTEBOOKS}
SECONDARY_NOTEBOOKS = {
    "tutorials/kalecancer/live-coding-survival": "tutorials/kalecancer/live-coding",
    "tutorials/kalecardiac/live-coding-lsemvae": "tutorials/kalecardiac/live-coding",
}

# Files each page's Binder launch checks on the public revision, besides .binder/.
# Binder kernels start in the notebook's own folder. The Cardiac notebooks install
# KaleCardiac in the session from their first code cell; .binder/ is shared and unchanged.
BINDER_FILES = {
    **{docname: [path, f"{CANCER}/synthetic_data_generation.py"]
       + ([f"{CANCER}/synthetic_showcase_data.py"] if path.endswith("_showcase.ipynb") else [])
       for docname, (_, path) in NOTEBOOKS.items()},
    "tutorials/kalecardiac/live-coding": [f"{CARDIAC}/tutorial-CardioVAE.ipynb",
                                          f"{CARDIAC}/configs/config_cardiovae_pretrain.yaml",
                                          f"{CARDIAC}/configs/config_cardiovae_finetune.yaml"],
    "tutorials/kalecardiac/live-coding-lsemvae": [f"{CARDIAC}/tutorial-LSEMVAE.ipynb",
                                                  f"{CARDIAC}/configs/config_lsemvae_pretrain.yaml",
                                                  f"{CARDIAC}/configs/config_lsemvae_finetune.yaml"],
}
