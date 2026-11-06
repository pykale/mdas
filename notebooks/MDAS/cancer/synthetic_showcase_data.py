import numpy as np
import pandas as pd
import h5py
from pathlib import Path

from synthetic_data_generation import PATCH_DIM

PATCH_SIZE = 256


def _tissue(rng: np.random.Generator, n_patches: int) -> np.ndarray:
    """Grow one connected piece of tissue on a grid, one patch at a time, and return its ``(n_patches, 2)`` cells."""
    cells = {(0, 0)}
    frontier = [(0, 0)]
    while len(cells) < n_patches:
        x, y = frontier[rng.integers(len(frontier))]
        dx, dy = [(1, 0), (-1, 0), (0, 1), (0, -1)][rng.integers(4)]
        if (x + dx, y + dy) not in cells:
            cells.add((x + dx, y + dy))
            frontier.append((x + dx, y + dy))
    grid = np.array(sorted(cells))
    return grid - grid.min(axis=0)


def make_showcase_cohort(
        folder: str,
        n_patients: int = 200,
        random_state: int = 42,
        missingness: float = 0.1,
        slide_missingness: float = 0.1
    ):
    """The ``make_cohort`` classification task, made messier and easier to see. Writes to a separate ``folder``.

    The recipe is the same (``stage`` follows the fraction of aggressive patches, plus age), with these changes:

    - Patches sit on a connected piece of tissue, and the aggressive ones form one region of it.
    - That region is small (up to 20% of the tissue), so a model has to find it. Age matters more as a result.
    - Aggressive patches stand out in half of the features rather than one, as they would in a real embedding.
    - ``slide_missingness`` of patients have no slide file at all.
    - Each h5 file also stores an ``aggressive`` mask: the ground truth to check attention against.
    """
    folder = Path(folder)
    patches_folder = folder / 'patches'
    patches_folder.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(random_state)

    # tabular data
    ids = pd.Index([f"patient_{k:03d}" for k in range(n_patients)], name="patient_id")
    clinical = pd.DataFrame(
        {
            "age": rng.normal(60, 10, n_patients),
            "gender": rng.choice(['F', 'M'], size=n_patients)
        },
        index=ids)

    # patch features (i.e. what output from UNI could look like)
    aggressive_fraction = rng.uniform(0, 0.2, n_patients)
    has_slide = rng.random(n_patients) >= slide_missingness
    for patient, fraction, slide in zip(ids, aggressive_fraction, has_slide, strict=True):
        n_patches = int(rng.integers(100, 400))
        features = rng.normal(size=(n_patches, PATCH_DIM)).astype(np.float32)
        grid = _tissue(rng, n_patches)

        # the aggressive region grows out from one random patch, with a slightly rough edge
        centre = grid[rng.integers(n_patches)]
        distance = np.linalg.norm(grid - centre, axis=1) + rng.normal(0, 0.5, n_patches)
        aggressive = np.zeros(n_patches, dtype=bool)
        aggressive[np.argsort(distance)[: int(fraction * n_patches)]] = True
        features[np.ix_(aggressive, range(PATCH_DIM // 2))] += 3.0

        if slide:
            with h5py.File(patches_folder / f"{patient}.h5", "w") as f:
                f["features"] = features
                f["coords"] = grid * PATCH_SIZE
                f["aggressive"] = aggressive

    # target: stage follows the slide and age; gender plays no part
    score = aggressive_fraction + 0.005 * (clinical["age"] - 60) + rng.normal(0, 0.03, n_patients)
    outcome = pd.DataFrame({"stage": np.where(score > 0.1, 'late', 'early')}, index=ids)

    # missingess for tabular data
    clinical = clinical.mask(
        rng.choice([True, False], size=clinical.shape, p=[missingness, 1.0 - missingness])
    )

    # saving tabular + target
    clinical = clinical.join(outcome)
    clinical.to_csv(folder / 'clinical.csv')
