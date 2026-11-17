"""Build the small HANCOCK bundle used by ``hancock_questions.ipynb``.

Organisers run this once, on a machine with the full HANCOCK download. Participants never need it: the notebook
downloads the finished bundle instead (see ``hancock_data.py``).

HANCOCK (https://hancock.research.fau.eu) is released under CC BY 4.0. Cite:
Dörrich, M., Balk, M., Heusinger, T. et al. A multimodal dataset for precision oncology in head and neck cancer.
Nat Commun 16, 7163 (2025). https://doi.org/10.1038/s41467-025-62386-6

What the bundle changes from the original, so it fits a one-hour session on a free CPU runtime:

- clinical.csv: baseline clinical variables and outcomes, one row per patient.
- pathology.csv: a subset of the pathology report variables.
- blood.csv: pre-treatment blood tests, pivoted to one row per patient (the measurement closest to first treatment).
- splits.csv: the published "in", "out" and "Oropharynx" train/test assignments.
- slides/<patient>.h5: UNI features of the primary-tumour slides, with a patient's slides joined and a random
  ``--patches`` patches kept per patient, stored as float16.

    uv run python notebooks/MDAS/cancer/prepare_hancock_bundle.py --hancock ~/datasets/HANCOCK/raw
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import zipfile
from pathlib import Path

import h5py
import numpy as np
import pandas as pd

VERSION = "v1"
CLINICAL = ["age_at_initial_diagnosis", "sex", "smoking_status", "primarily_metastasis",
            "days_to_last_information", "survival_status", "recurrence", "days_to_recurrence"]
PATHOLOGY = ["primary_tumor_site", "pT_stage", "pN_stage", "grading", "hpv_association_p16", "histologic_type",
             "number_of_positive_lymph_nodes", "infiltration_depth_in_mm", "lymphovascular_invasion_L",
             "vascular_invasion_V", "perineural_invasion_Pn", "perinodal_invasion", "carcinoma_in_situ",
             "resection_status"]
SPLITS = ["in", "out", "Oropharynx"]
BLOOD_COVERAGE = 0.8  # Keep analytes measured in at least this share of patients with any blood test.


def _read(path: Path) -> pd.DataFrame:
    return pd.read_json(path, dtype={"patient_id": str}).set_index("patient_id").sort_index()


def _blood(raw: Path) -> pd.DataFrame:
    long = pd.read_json(raw / "StructuredData" / "blood_data.json", dtype={"patient_id": str})
    closest = long.sort_values("days_before_first_treatment").drop_duplicates(["patient_id", "analyte_name"])
    wide = closest.pivot(index="patient_id", columns="analyte_name", values="value").sort_index()
    wide = wide.loc[:, wide.notna().mean() >= BLOOD_COVERAGE]
    wide.columns = [re.sub(r"[^0-9a-zA-Z]+", "_", name.replace("%", " pct")).strip("_").lower() for name in wide.columns]
    return wide.round(3)


def _slides(raw: Path, out: Path, n_patches: int, seed: int) -> int:
    pattern = re.compile(r"PrimaryTumor_HE_(\d{3})(?:_[a-z])?\.h5$")
    files: dict[str, list[Path]] = {}
    for path in sorted((raw / "WSI_PrimaryTumor_UNI_Encodings").glob("*/h5_files/*.h5")):
        if match := pattern.search(path.name):
            files.setdefault(match.group(1), []).append(path)
    out.mkdir(parents=True)
    rng = np.random.default_rng(seed)
    for patient, paths in files.items():
        features, coords = [], []
        for path in paths:
            with h5py.File(path) as f:
                features.append(f["features"][:])
                coords.append(f["coords"][:, :2])
        features, coords = np.concatenate(features), np.concatenate(coords)
        keep = np.sort(rng.choice(len(features), size=min(n_patches, len(features)), replace=False))
        with h5py.File(out / f"{patient}.h5", "w") as f:
            # No timestamps, so rebuilding gives byte-identical files and the same checksum
            f.create_dataset("features", data=features[keep].astype(np.float16), track_times=False)
            f.create_dataset("coords", data=coords[keep].astype(np.int32), track_times=False)
    return len(files)


def build(raw: Path, out: Path, n_patches: int, seed: int) -> Path:
    folder = out / f"hancock_mdas_{VERSION}"
    if folder.exists():
        shutil.rmtree(folder)
    folder.mkdir(parents=True)

    _read(raw / "StructuredData" / "clinical_data.json")[CLINICAL].to_csv(folder / "clinical.csv")
    _read(raw / "StructuredData" / "pathological_data.json")[PATHOLOGY].to_csv(folder / "pathology.csv")
    _blood(raw).to_csv(folder / "blood.csv")
    splits = pd.concat(
        {name: _read(raw / "DataSplits_DataDictionaries" / f"dataset_split_{name}.json")["dataset"] for name in SPLITS},
        axis=1)
    splits.to_csv(folder / "splits.csv")
    n_slides = _slides(raw, folder / "slides", n_patches, seed)

    (folder / "README.md").write_text(
        f"# HANCOCK MDAS bundle {VERSION}\n\n"
        "A reduced copy of HANCOCK for the MDAS hands-on session, built by "
        "`notebooks/MDAS/cancer/prepare_hancock_bundle.py`.\n\n"
        "Source: HANCOCK, https://hancock.research.fau.eu, released under CC BY 4.0 "
        "(https://creativecommons.org/licenses/by/4.0/).\n\n"
        "Cite: Dörrich, M., Balk, M., Heusinger, T. et al. A multimodal dataset for precision oncology in head and "
        "neck cancer. Nat Commun 16, 7163 (2025). https://doi.org/10.1038/s41467-025-62386-6\n\n"
        "Changes from the original: a subset of clinical and pathology variables; blood tests pivoted to the "
        "measurement closest to first treatment, keeping analytes measured in at least "
        f"{BLOOD_COVERAGE:.0%} of tested patients; primary-tumour UNI patch features joined per patient, randomly "
        f"subsampled to at most {n_patches} patches (seed {seed}) and stored as float16. Not for clinical use.\n",
        encoding="utf-8")
    (folder / "manifest.json").write_text(json.dumps(
        {"version": VERSION, "patients": int(len(splits)), "patients_with_slides": n_slides,
         "patches_per_slide": n_patches, "seed": seed}, indent=2), encoding="utf-8")

    archive = out / f"hancock_mdas_{VERSION}.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_STORED) as zf:  # float16 features barely compress
        for path in sorted(folder.rglob("*")):
            if path.is_file():
                # A fixed date keeps the archive, and so its checksum, identical across rebuilds
                info = zipfile.ZipInfo(path.relative_to(out).as_posix(), date_time=(2026, 1, 1, 0, 0, 0))
                info.external_attr = 0o644 << 16
                zf.writestr(info, path.read_bytes())
    return archive


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--hancock", type=Path, required=True, help="Folder holding the original HANCOCK download")
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parents[3] / "data")
    parser.add_argument("--patches", type=int, default=128)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    archive = build(args.hancock.expanduser(), args.out, args.patches, args.seed)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    print(f"{archive} ({archive.stat().st_size / 1e6:.0f} MB)\nsha256 {digest}")


if __name__ == "__main__":
    main()
