"""Shared mapping between documentation pages and their tutorial notebooks."""

CANCER = "notebooks/MDAS/cancer"
NOTEBOOKS = {
    "tutorials/kalecancer/live-coding": ("Classification", f"{CANCER}/classification_showcase.ipynb"),
    "tutorials/kalecancer/live-coding-survival": ("Survival Analysis", f"{CANCER}/survival_showcase.ipynb"),
}

# Each Cardiac tutorial is its own page, titled by the data it learns from, so participants can
# choose without knowing the model; its summary and notebook name the model.
CARDIAC = "notebooks/MDAS/cardiac"
CARDIAC_NOTEBOOKS = {
    "tutorials/kalecardiac/cardiovae": ("Chest X-ray and ECG", f"{CARDIAC}/tutorial-CardioVAE.ipynb"),
    "tutorials/kalecardiac/lsemvae": ("12-lead ECG", f"{CARDIAC}/tutorial-LSEMVAE.ipynb"),
}
# The sentence beneath each page's title, in MyST Markdown; [1] links to the model's paper in the
# notebook's own References section.
CARDIAC_SUMMARIES = {
    "tutorials/kalecardiac/cardiovae": "Learn from paired chest X-rays and 12-lead ECGs with the CardioVAE model "
                                       "[\\[1\\]](#references), which can still make predictions when one of the two "
                                       "is missing.",
    "tutorials/kalecardiac/lsemvae": "Learn from the 12 leads of an ECG, each as a separate input, with the LS-EMVAE "
                                     "model [\\[1\\]](#references), which can still make predictions when leads are "
                                     "missing.",
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
