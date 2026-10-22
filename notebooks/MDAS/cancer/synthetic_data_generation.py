import numpy as np
import pandas as pd
import h5py
from pathlib import Path

PATCH_DIM = 32

def make_cohort(
        folder: str,
        n_patients: int = 100,
        random_state: int = 42,
        missingness: float = 0.1
    ):
    """Write one h5 file of patch features per patient into ``folder``; return the clinical table and outcomes."""
    folder = Path(folder)
    folder.mkdir(parents = True, exist_ok=True)
    rng = np.random.default_rng(random_state)

    # tabular data
    ids = pd.Index([f"patient_{k:03d}" for k in range(n_patients)], name="patient_id")
    clinical = pd.DataFrame(
        {
            "age": rng.normal(60, 10, n_patients),
            "stage": rng.integers(1, 5, n_patients),
            "gender": rng.choice(['F', 'M'], size=n_patients)
        },
        index=ids)

    # patch features (i.e. what output from UNI could look like)
    aggressive_fraction = rng.uniform(0, 0.5, n_patients)
    for patient, fraction in zip(ids, aggressive_fraction, strict=True):
        n_patches = int(rng.integers(20, 200))
        features = rng.normal(size=(n_patches, PATCH_DIM)).astype(np.float32)
        features[: int(fraction * n_patches), 0] += 3.0  # aggressive patches stand out in one feature
        patches_folder = folder / 'patches'
        patches_folder.mkdir(exist_ok=True)
        with h5py.File(patches_folder / f"{patient}.h5", "w") as f:
            f["features"] = features
            f["coords"] = rng.integers(0, 50_000, size=(n_patches, 2))

    # target
    risk = 0.09 * (clinical["age"] - 60) + 1.2 * (clinical["stage"] - 2.5) + 12.0 * aggressive_fraction
    event_time = rng.exponential(2000 * np.exp(-risk))
    censoring_time = rng.uniform(200, 3000, n_patients)
    outcome = pd.DataFrame(
        {"time": np.minimum(event_time, censoring_time), "event": event_time <= censoring_time}, index=ids
    )

    # missingess for tabular data
    clinical = clinical.mask(
        rng.choice([True, False], size= clinical.shape, p = [missingness, 1.0-missingness])
    )

    # saving tabular + target
    clinical = clinical.join(outcome)
    clinical.to_csv(folder / 'clinical.csv')
