"""Data and helpers for ``hancock_questions.ipynb``.

``fetch_hancock`` gets the data. Participants do not download anything from the HANCOCK website: a reduced bundle
(about 190 MB), built once by ``prepare_hancock_bundle.py``, is hosted on Dropbox. It is downloaded on
first use, checked against its SHA-256 and unpacked; later calls reuse the unpacked copy. To use a copy you already
have (for example on a shared drive or a USB stick), set ``MDAS_HANCOCK_ZIP`` to its path or URL.

The other helpers keep the notebook's questions to a line or two. ``experiment`` does exactly what section 1 of the
notebook does step by step: build a ``MultimodalDataset``, split it, fit a ``Pipeline``, predict and score.

HANCOCK is released under CC BY 4.0. Cite: Dörrich, M., Balk, M., Heusinger, T. et al. A multimodal dataset for
precision oncology in head and neck cancer. Nat Commun 16, 7163 (2025). https://doi.org/10.1038/s41467-025-62386-6
"""
from __future__ import annotations

import hashlib
import os
import shutil
import zipfile
from functools import partial
from pathlib import Path
from urllib.request import urlopen

import matplotlib.pyplot as plt
import pandas as pd
import torch
from IPython.display import display
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder, StandardScaler

from kalecancer.evaluate import EvalContext, HarrellC, bootstrap_ci
from kalecancer.loaddata import MultimodalDataset, PatchFeatures, Tabular, TimeToEvent
from kalecancer.model import ABMIL, MLP, CoxHead, IntermediateFusion, MaskedMean
from kalecancer.pipeline import Pipeline
from kalecancer.prepdata import ColumnGroup, TableTransform

BUNDLE = "hancock_mdas_v1"
# A Dropbox shared link; dl=1 makes it download the file instead of opening a preview page
URL = ("https://www.dropbox.com/scl/fi/7rh423jkx8xfpp0y4axqb/hancock_mdas_v1.zip"
       "?rlkey=bhxa5juvmah7c7vrxqflej93h&st=f5d7emaf&dl=1")
SHA256 = "4643ad148d0cb1cb146a66a89fe032a86ef1e3328d6e5d804df096c3c0a5199a"

# Chosen by 5-fold cross-validation; training longer overfits the slide encoder
HIDDEN, LEARNING_RATE, EPOCHS, RANDOM_STATE = 64, 1e-3, 10, 0
MODEL_COLOUR = "#1baf7a"

results: list[dict] = []  # Every experiment() run, for plot_results()
_folder: Path | None = None


# Data

def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _download(source: str, archive: Path) -> None:
    partial_file = archive.with_suffix(".part")
    print(f"Downloading the HANCOCK bundle from {source} ...", flush=True)
    with urlopen(source, timeout=60) as response, partial_file.open("wb") as out:
        total, done, shown = int(response.headers.get("Content-Length") or 0), 0, -1
        while block := response.read(1 << 20):
            out.write(block)
            done += len(block)
            if total and (percent := 100 * done // total) // 10 != shown:
                shown = percent // 10
                print(f"  {done / 1e6:.0f} of {total / 1e6:.0f} MB", flush=True)
    partial_file.replace(archive)


def fetch_hancock(data_folder: str | Path = "../../../data") -> Path:
    """Return the folder holding the HANCOCK bundle, downloading and unpacking it the first time."""
    global _folder
    data_folder = Path(data_folder)
    folder = data_folder / BUNDLE
    if not (folder / "manifest.json").exists():
        data_folder.mkdir(parents=True, exist_ok=True)
        archive = data_folder / f"{BUNDLE}.zip"
        source = os.environ.get("MDAS_HANCOCK_ZIP", URL)
        if not archive.exists():
            if Path(source).expanduser().is_file():
                shutil.copyfile(Path(source).expanduser(), archive)
            else:
                _download(source, archive)
        if (actual := _sha256(archive)) != SHA256:
            archive.unlink()
            raise RuntimeError(f"The HANCOCK bundle from {source} has SHA-256 {actual}, expected {SHA256}. "
                               "It was deleted; rerun this cell to download it again.")
        with zipfile.ZipFile(archive) as zf:
            zf.extractall(data_folder)
        print(f"HANCOCK bundle ready in {folder}")
    _folder = folder
    return folder


def _bundle() -> Path:
    if _folder is None:
        raise RuntimeError("Run fetch_hancock() first.")
    return _folder


def _overall_survival() -> TimeToEvent:
    clinical = pd.read_csv(_bundle() / "clinical.csv", index_col=0, dtype={"patient_id": str})
    return TimeToEvent(time=clinical["days_to_last_information"], event=clinical["survival_status"] == "deceased")


def official_split(data: MultimodalDataset, name: str = "in") -> tuple[MultimodalDataset, MultimodalDataset]:
    """The published HANCOCK train/test assignment ("in", "out" or "Oropharynx") for the patients in ``data``."""
    splits = pd.read_csv(_bundle() / "splits.csv", index_col=0, dtype={"patient_id": str})
    split = splits[name].reindex(data.ids)
    return data.subset(split.index[split == "training"]), data.subset(split.index[split == "test"])


def table_transform(table: pd.DataFrame) -> TableTransform:
    """Impute and scale the numeric columns; number the text categories, with -1 for missing or unseen."""
    numeric = [column for column in table.columns if pd.api.types.is_numeric_dtype(table[column])]
    text = [column for column in table.columns if column not in numeric]
    groups = {}
    if numeric:
        groups["numeric"] = ColumnGroup(numeric, [SimpleImputer(), StandardScaler()])
    if text:
        groups["categorical"] = ColumnGroup(text, [OrdinalEncoder(
            encoded_missing_value=-1, handle_unknown="use_encoded_value", unknown_value=-1)])
    return TableTransform(groups=groups, drop=[])


# Experiments

def _pipeline(modalities: dict[str, pd.DataFrame | PatchFeatures]) -> Pipeline:
    torch.manual_seed(RANDOM_STATE)  # The same starting weights every time, so comparisons are fair
    tables = {name: data for name, data in modalities.items() if isinstance(data, pd.DataFrame)}
    encoders = {
        name: [MLP(in_dim=data.shape[1], hidden_dims=[HIDDEN], out_dim=HIDDEN, dropout=0.25)] if name in tables
        else [ABMIL(in_dim=1024, hidden_dim=HIDDEN, attention_dim=HIDDEN // 2, dropout=0.25)]
        for name, data in modalities.items()
    }
    return Pipeline(
        model=IntermediateFusion(encoders=encoders, fusion=MaskedMean(), head=CoxHead(in_dim=HIDDEN, ties="efron")),
        transforms={name: table_transform(table) for name, table in tables.items()},
        optimizer=partial(torch.optim.AdamW, lr=LEARNING_RATE, weight_decay=1e-2),
        batch_size=64, drop_last=False, max_epochs=EPOCHS, validation=None, early_stopping=None,
        accelerator="cpu", precision="32-true", random_state=RANDOM_STATE,
    )


def experiment(name: str, modalities: dict[str, pd.DataFrame | PatchFeatures], target: TimeToEvent | None = None,
               split: str = "in") -> dict:
    """Train one survival model on an official split, print its test C-index with a 95% CI, and log it.

    ``modalities`` is what you would give ``MultimodalDataset``, except that tables are plain DataFrames: each table
    gets a ``table_transform`` and an ``MLP`` encoder, and each ``PatchFeatures`` an ``ABMIL`` encoder. ``target``
    defaults to overall survival.
    """
    data = MultimodalDataset(
        modalities={key: Tabular(value) if isinstance(value, pd.DataFrame) else value for key, value in modalities.items()},
        target=target or _overall_survival(),
        required_modalities=[],
    )
    train, test = official_split(data, split)
    pipeline = _pipeline(modalities).fit(train)
    predictions = pipeline.predict(test)
    truth = test.target.frame.loc[predictions.index]
    context = EvalContext(train_target=pipeline.train_target_, classes=None)
    interval = bootstrap_ci(HarrellC(), predictions, truth, context)
    results.append({"experiment": name, "split": split, "test patients": len(predictions),
                    "C-index": interval.estimate, "lower": interval.lower, "upper": interval.upper})
    print(f"{name} ({split} split): C-index {interval.estimate:.3f} (95% CI {interval.lower:.2f} to {interval.upper:.2f})")
    return {"pipeline": pipeline, "data": data, "train": train, "test": test, "predictions": predictions,
            "truth": truth, "context": context}


def compare(new: dict, old: dict) -> None:
    """Print the bootstrap 95% CI of the C-index gained by ``new`` over ``old`` on the same test patients."""
    shared = new["predictions"].index.intersection(old["predictions"].index)
    gain = bootstrap_ci(HarrellC(), new["predictions"].loc[shared], new["truth"].loc[shared], new["context"],
                        baseline=old["predictions"].loc[shared], baseline_context=old["context"])
    verdict = "a clear gain" if gain.lower > 0 else "a clear loss" if gain.upper < 0 else "no clear difference"
    print(f"Gain: {gain.estimate:+.3f} (95% CI {gain.lower:+.2f} to {gain.upper:+.2f}): {verdict}")


# Plots

def plot_results() -> None:
    """Show every experiment run so far, best first, as a table and a plot of C-index with 95% CI."""
    board = (pd.DataFrame(results).drop_duplicates(["experiment", "split"], keep="last")
             .sort_values("C-index", ascending=False).reset_index(drop=True))
    display(board.round(3))
    fig, ax = plt.subplots(figsize=(7, 0.35 * len(board) + 1))
    rows = list(range(len(board)))[::-1]
    ax.errorbar(board["C-index"], rows, xerr=[board["C-index"] - board["lower"], board["upper"] - board["C-index"]],
                fmt="o", color=MODEL_COLOUR, ecolor="#b8b6ae", capsize=3)
    ax.set_yticks(rows, [f"{name} ({split})" for name, split in zip(board["experiment"], board["split"])])
    ax.axvline(0.5, color="#8a8880", linestyle="--", linewidth=1)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set(title="Test C-index with 95% CI", xlabel="C-index")
    plt.show()
