# External Google Colab execution for MDAS Cancer

The four authored Cancer notebooks are **unchanged**, including code, Markdown, metadata and saved outputs. The Binder environment and controller are unchanged. This directory supplies an external preparation notebook and runner.

## What this workflow can and cannot do

`prepare_colab.ipynb` runs the original Classification and/or Survival notebook from a public MDAS checkout, in separate fresh kernels, without editing the source files. It downloads HTML reports, execution copies and timing/checksum reports. It does not prepare an independent Colab tab that opens an original notebook. Independently opened Colab notebooks do not automatically share packages, files or kernel state.

The website keeps its original Classification and Survival Colab links, and adds a **Prepare Colab Environment** link. Fully automatic interactive execution in an independently opened original Colab tab is not achievable by a separate setup notebook alone. It would require changing the originals or configuring that tab's runtime manually. This implementation instead offers external, complete execution of the originals. Binder remains the direct interactive path.

## Root causes and dependency choice

- Colab's GitHub notebook opener does not clone its repository. `synthetic_data_generation.py` is absent, and Colab's default working directory does not make the original relative data path point into an MDAS checkout.
- The root `pyproject.toml` is a research environment manifest, not a suitable Colab bootstrap. `uv.lock` and `.binder/requirements.txt` pin KaleCancer to Git commit `1f476fdba87f515286f732cd7eaa92ffeeffdbc2`. The registry check found no published `kalecancer` distribution; installation uses the existing VCS pin, not a guessed PyPI package.
- That [KaleCancer metadata](https://github.com/pykale/cancer/blob/1f476fdba87f515286f732cd7eaa92ffeeffdbc2/pyproject.toml) requires Python `>=3.11,<3.13`, PyTorch `>=2.6`, and PyKale `>=0.2.0`. [PyKale 0.2.1 release metadata](https://pypi.org/pypi/pykale/0.2.1/json) requires Python `<3.13`, PyTorch `<=2.6.0`, pandas `<=2.2.2` and NumPy `>=2.0.0`. A dependency-respecting installation therefore uses Python 3.12 and PyTorch 2.6, not the newest Colab stack.
- [Google's runtime documentation](https://research.google.com/colaboratory/runtime-version-faq.html) lists Python 3.13/PyTorch 2.11 for 2026.10 and Python 3.12/PyTorch 2.11 for 2026.07. Select **Runtime > Change runtime type > Runtime Version > 2026.07**, then reconnect. The preparation notebook verifies the actual host-kernel Python. If Python 3.12 is unavailable, use Binder; no dependency metadata override is used.

`requirements.txt` includes the existing, unchanged Binder CPU research lock and adds only `nbclient==0.11.0`, `nbformat==5.11.1`, and `nbconvert==7.17.2` for execution/reporting. Research pins include `pykale==0.2.1`, `torch==2.6.0+cpu`, `torchvision==0.21.0+cpu`, `numpy==2.5.4`, `pandas==2.2.2`, `h5py==3.16.0`, `scikit-learn==1.9.1`, `lightning==2.6.6` and `torchsurv==0.1.6`. No imaging, pathology, TabICL, interpretation or development extras are requested. Research transitive versions come from the existing lock; reporting-tool transitive dependencies are resolved by pip and are not a complete image lock.

`environment.py` creates `.venv/colab` using the actual Python 3.12 interpreter, installs normally through pip, runs `pip check`, and imports the APIs used by both tutorials. It installs only into the isolated environment, with ordinary dependency resolution and no `--ignore-requires-python` or `--no-deps` overrides. It does not install the root project with `pip install -e .`. A checksum of both requirement inputs controls reuse. Failed installations are not marked ready. The virtual environment is created without `ensurepip`; the host pip (22.3 or newer) manages it through the [documented `--python` option](https://pip.pypa.io/en/stable/topics/python-option/). This unseeded-environment bootstrap was tested separately, and it does not install into the host.

`run_notebooks.py` supplies an explicit kernel spec containing the prepared interpreter's `sys.executable`. Creating a virtual environment does not change the Colab notebook's kernel; the worker deliberately launches a separate kernel instead. Each original notebook executes in `notebooks/MDAS/cancer`, preserving both same-directory imports and `../../../data/synthetic_data`. Original data generation is untouched: Classification uses its existing classification default and Survival its explicit survival task. Repeated runs overwrite the same deterministic synthetic files. Run the two tasks sequentially because the originals share their data directory. The blank notebooks remain optional exercises and are not executed as complete tutorials; their paths and missing exercise code are preserved exactly.

## Repository and revision handling

The preparation notebook shallow-clones `https://github.com/pykale/mdas` into `/content/mdas-colab` on its first run. It records the resolved commit. Reruns verify the origin and reuse that checkout without pulling, resetting or overwriting local work. A fresh session follows the then-current `main`; record the printed commit for reproduction. The checkout supplies both notebooks, the helper, requirement files and runner from one revision. No Drive mount, upload, personal path or untracked development file is needed.

These new `colab/` files and the website links are local review changes. They must be published together before the new public preparation link works. Existing links to the original notebooks remain unchanged. No commit, push or deployment is performed here.

## Validation on 3 November 2026

| Check | Actual result |
| --- | --- |
| All four original notebook files | Byte-identical to their initial checkout copies and authored Git payloads |
| Binder configuration and controller | No source changes |
| Fresh public Binder kernels, original Classification | All 25 code cells passed, including full 40-epoch training, baseline, evaluation and bootstrap; about 90.9 seconds |
| Fresh public Binder kernels, original Survival | All 28 code cells passed, including full 40-epoch training, baseline, evaluation and bootstrap; about 52.6 seconds |
| Isolated local Python 3.12 setup | Normal dependency resolution, `pip check` and actual tutorial API imports passed; initial install about 156.7 seconds; cached preparation about 5.0 seconds |
| Local nbclient runner | All 25 Classification cells passed in 13.1 seconds and all 28 Survival cells in 18.1 seconds; source unchanged; HTML reports, execution copies and JSON timings produced |
| Worker failure test | Passed: first failure stops later cells, saves a partial report, and preserves source bytes |
| Workflow regression tests | Four tests passed; setup reuse, unsupported-Python rejection, authored notebook preservation, and setup notebook syntax |
| Website | Clean-source strict Sphinx builds passed with Thebe enabled and disabled; 27 HTML pages, 1,426 enabled-build links/assets and 1,418 disabled-build links/assets checked with zero errors; generated notebook link/ToC checks and 17 JavaScript tests passed |
| Direct Google Colab UI | **Not tested**; no claim of a verified Colab session or cross-tab environment sharing |

Public Binder tested repository revision `bc4399b85b4513b68745a7c3d56f3c9ef2a27d92` using its unchanged Python 3.12 Linux environment. Local isolated-environment tests used Python 3.12.10 on Windows with the exact research dependency versions above. Timings are measurements on those systems, not Colab guarantees. No epochs or scientific analyses were removed, reduced or skipped.

Local execution artifacts are under ignored `outputs/colab/`; installation and execution logs are under ignored `tmp/`. Outputs include the worker interpreter, working directory, source checksum, individual cell timings, completion status and a source-unchanged check. Source notebooks are never execution output destinations. The worker stops on the first failure, saves partial notebook/report results, removes an older HTML success report for that task, and closes its kernel.

Run these checks from the repository root:

```text
python -m unittest discover -s colab/tests
python site/build.py
python site/tests/test_notebooks.py
node --test site/tests/interactive.test.cjs site/tests/presentation.test.cjs site/tests/notebooks.test.cjs
```

For a supported local Python 3.12 installation, run `python colab/environment.py`, then use the interpreter printed/created at `.venv/colab/bin/python` (Linux) or `.venv/colab/Scripts/python.exe` (Windows):

```text
<prepared-python> colab/run_notebooks.py both
<prepared-python> colab/tests/check_worker.py
```

The worker integration check deliberately fails a temporary notebook, confirms later cells do not run, and verifies the source and partial failure report. It does not edit or use the authored notebooks as failure fixtures.

## Final manual Colab test after publication

1. Open `colab/prepare_colab.ipynb` through its Colab link in a fresh session. Select runtime **2026.07 / Python 3.12** and a CPU runtime. Do not mount Drive or reuse a previous session.
2. Run the checkout and preparation cells. Confirm the printed repository commit, successful `pip check`, PyTorch `2.6.0+cpu` in the research environment, and the message that the host kernel is unchanged.
3. Select `classification` and execute. Confirm all 25 code cells pass, including training, baseline evaluation and bootstrap intervals. Download and inspect its HTML and execution report.
4. In a second fresh Colab session, repeat for `survival`; confirm all 28 code cells pass and inspect the survival metrics and bootstrap table.
5. In either preparation session, rerun setup and choose `both`. Confirm no reclone, installation reuse, fresh kernels for each task and unchanged source checksums. Download results before disconnecting.
6. Open each website **Open in Google Colab** button and confirm it still targets the corresponding original notebook. Do not expect that independent tab to inherit preparation. Check both optional blank exercise links. Test Binder separately; its source configuration is unchanged.
7. In a Python 3.13 Colab session confirm preparation stops with the supported-runtime instruction before it installs anything. If 2026.07 is no longer offered, record the limitation and use Binder rather than bypassing upstream constraints.

## Files changed

New: `colab/prepare_colab.ipynb`, `colab/environment.py`, `colab/run_notebooks.py`, `colab/requirements.txt`, `colab/tests/test_workflow.py`, `colab/tests/check_worker.py`, this README, and `docs/colab.md`.

Updated: `site/conf.py` (preparation link/guidance only), `site/tests/test_notebooks.py` (link checks), `site/README.md`, and `docs/notebook-execution.md`.

Unchanged: all four Cancer notebooks, `synthetic_data_generation.py`, `pyproject.toml`, `uv.lock`, `.binder/`, the Binder adapter/controller, selector/presentation assets, logo, venue/programme information, and GitHub Pages deployment workflow.
