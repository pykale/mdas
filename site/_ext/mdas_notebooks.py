"""Shared mapping between documentation pages and their tutorial notebooks."""

CANCER = "notebooks/MDAS/cancer"
NOTEBOOKS = {
    "tutorials/kalecancer/live-coding": ("KaleCancer Classification", f"{CANCER}/classification_showcase.ipynb"),
    "tutorials/kalecancer/live-coding-survival": ("KaleCancer Survival Analysis", f"{CANCER}/survival_showcase.ipynb"),
}

# The Cardiac tutorials share one sidebar entry and heading; the first is its default page.
CARDIAC = "notebooks/MDAS/cardiac"
CARDIAC_TUTORIALS_TITLE = "KaleCardiac API Notebooks"
CARDIAC_NOTEBOOKS = {
    "tutorials/kalecardiac/cardiovae": ("CardioVAE", f"{CARDIAC}/tutorial-CardioVAE.ipynb"),
    "tutorials/kalecardiac/lsemvae": ("LS-EMVAE", f"{CARDIAC}/tutorial-LSEMVAE.ipynb"),
}

# Every staged notebook page.
ALL_NOTEBOOKS = {**NOTEBOOKS, **CARDIAC_NOTEBOOKS}

# Binder runs the Cancer notebooks only: the Cardiac tutorials need a GPU, so they use Colab.
# Files each page's Binder launch checks on the public revision, besides .binder/.
BINDER_FILES = {
    docname: [path, f"{CANCER}/synthetic_data_generation.py"]
    + ([f"{CANCER}/synthetic_showcase_data.py"] if path.endswith("_showcase.ipynb") else [])
    for docname, (_, path) in NOTEBOOKS.items()
}
