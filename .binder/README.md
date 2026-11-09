# Shared Binder notebook environment

`runtime.txt` selects Python 3.12. `requirements.in` defines Binder's CPU-only environment; `requirements.txt` is its resolved Linux x86-64 lock. Binder supplies its own Jupyter server, while the lock includes the Python kernel. The root research project and Colab bootstrap are not installed or run by Binder. No postBuild/start hooks are required.

## Research dependencies

- KaleCancer: `f8dff11372587c4ae97ce86b7d869ace511a6a17`, including the interpretation and survival APIs used by both showcases.
- CPU PyTorch / Torchvision: 2.6.0+cpu / 0.21.0+cpu; PyKale 0.2.1.
- NumPy 2.5.4 and pandas 2.2.2. Binder retains its original NumPy pin; Colab independently uses 2.0.2. The initial attempt to align Binder to Colab's NumPy allowed Cardiac's existing setup to upgrade it; the final Binder pin matches the version used successfully by both Cardiac tutorials.
- jsonargparse[signatures] 4.52.0 satisfies KaleCancer's exact requirement.
- Matplotlib 3.11.2 and its resolved plotting dependencies; Hugging Face Hub 1.33.0 with HTTPX 0.28.1.

No CUDA packages or optional Cancer imaging/pathology/TabICL extras are added. Cardiac's original setup cell still installs `kalecardiac[imaging,interpret]` and fetches its tutorial configuration. Neither Cardiac notebook nor its setup was changed.

Cancer kernels start in `notebooks/MDAS/cancer/`, next to `synthetic_data_generation.py` and `synthetic_showcase_data.py`. The authored relative data paths resolve within the repository. Participants generate synthetic data by running the notebook's cells. Cardiac kernels start in `notebooks/MDAS/cardiac/`; their setup then changes into the downloaded tutorial folder. A Binder launch starts no scientific cells automatically.

## Regenerate the Linux lock

```sh
uv pip compile .binder/requirements.in --python-version 3.12 --python-platform x86_64-unknown-linux-gnu --index-strategy unsafe-best-match --emit-index-url --output-file .binder/requirements.txt
```

## Validation on 9 November 2026

Local Ubuntu/WSL, Python 3.12.15, CPU, two numerical-library threads. A newly created environment installed the final Binder lock using ordinary pip resolution, with nbclient 0.11.0 and nbconvert 7.17.2 as validation-only tools. Each notebook used a fresh kernel and byte-for-byte source copies in isolated Linux-native input trees. Cancer began with no generated data. Cardiac executed its original install and public Dropbox download cells.

| Original source notebook | Code cells passed | Elapsed |
| --- | ---: | ---: |
| `classification_showcase.ipynb` | 24 | 65.06 s |
| `survival_showcase.ipynb` | 28 | 81.50 s |
| `tutorial-CardioVAE.ipynb` | 21 | 185.01 s |
| `tutorial-LSEMVAE.ipynb` | 21 | 69.86 s |

No scientific cells, epochs, folds, bootstrap intervals or interpretation steps were reduced or skipped. The validation runner explicitly executes Cardiac cells tagged `skip-execution`; source tags and cells are unchanged. All source hashes stayed unchanged.

All 90 locked package versions and KaleCancer VCS provenance matched after installation and after both Cardiac runs. `pip check` passed. Cardiac's validated main revision was `55d1e404026e16cfe5467c44acd91a2971e303ee`; its unchanged install command subsequently proposed zero package changes in a pip dry-run. There is no remaining conflict with the final Binder pins. Cardiac still follows upstream main, so this records the tested revision rather than changing its setup.

Reproduce in a disposable Linux checkout (notebook cells create synthetic data, clones, downloaded data and model outputs):

```sh
python3.12 -m venv /tmp/mdas-binder-check
. /tmp/mdas-binder-check/bin/activate
python -m pip install -r .binder/requirements.txt nbclient==0.11.0 nbconvert==7.17.2
python -m pip check
python site/tests/execute_notebooks.py classification_showcase --variant original --output outputs/binder-cancer
python site/tests/execute_notebooks.py survival_showcase --variant original --output outputs/binder-cancer
python site/tests/execute_notebooks.py tutorial-CardioVAE --variant original --output outputs/binder-cardiac
python site/tests/execute_notebooks.py tutorial-LSEMVAE --variant original --output outputs/binder-cardiac
python -m pip check
```

Final local execution reports and rendered outputs are ignored under `outputs/binder-final-cancer/` and `outputs/binder-linux-native-cardiac/`. Earlier mounted-drive exploratory runs are not the reported results.

## Hosted checks still required

This verifies Linux dependencies and complete notebook execution, not a repo2docker image or hosted Binder launch. Docker was not running. The proposed environment cannot be tested by public Binder before the reviewed files are published on the configured ref. No commit, push, deployment, Sphinx build or browser preview was performed.

After publication, launch both Cancer selections and both Cardiac selections through the website. Check image build, kernel connection, notebook working directories, cell execution, active-session switching guards and downloadable outputs where supported. Public Binder's RAM, CPU, startup latency and session lifetime may differ from the local machine; full training under those limits is unverified. Preserve work before leaving a temporary session.
