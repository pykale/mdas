# Showcase Colab integration ? 9 November 2026

This section supersedes the historical validation below for the website's selected Cancer notebooks.

- Classification displays `classification_showcase.ipynb` and opens `classification_showcase_colab.ipynb` in Colab.
- Survival Analysis displays `survival_showcase.ipynb` and opens `survival_showcase_colab.ipynb` in Colab.
- The Survival source and matching `synthetic_showcase_data.py` were copied byte-for-byte from MDAS revision `ff4a8ddd7fed5bba229392505b98aa160fbbeda8` after fetching origin. Existing local edits were retained and HEAD was not advanced. The four original notebooks, existing Classification showcase and Cardiac notebooks were not rewritten.
- Both generated showcase copies prepend setup only. All source scientific cell dictionaries, metadata and outputs are preserved. The generator also refreshes the setup hashes in the retained legacy Colab copies.
- KaleCancer is pinned to `f8dff11372587c4ae97ce86b7d869ace511a6a17`, which provides the interpretation, survival calibration, risk-group and patient-report APIs used by the showcases. `jsonargparse==4.52.0` satisfies this revision's exact requirement; Matplotlib 3.11.2 and its plotting dependencies are included. Existing Hub 1.33.0 and the remaining scientific pins are retained.
- Bootstrap downloads the setup, requirements and both synthetic helpers from public MDAS main, verifies embedded SHA-256 values with LF normalization, and prepares the active Python 3.12 kernel. Helpers are importable from the Cancer working directory; scientific cells generate data at their authored relative paths. Restart and rerun setup when requested for already loaded packages. A final `pip check` and API imports must pass before readiness.

## Local validation

Windows / Python 3.12.10, a newly created isolated environment, ordinary pip resolution (no dependency overrides), and a separate fresh notebook kernel for each execution:

| Check | Result |
| --- | --- |
| Final Classification showcase Colab copy | All 25 code cells passed, including setup and the final cell; 88.91 seconds; source unchanged |
| Final Survival showcase Colab copy | All 29 code cells passed, including setup and the final cell; 98.62 seconds; source unchanged |
| Existing Survival Colab copy on the new dependency pin | All 29 code cells passed; 19.36 seconds |
| Dependencies | Full installation resolved; `pip check` passed |
| Colab regression tests | All 10 passed: preserved cells, both generated page targets, runtime guards, provenance, Hub compatibility, mocked fresh helper/support downloads, checksums and cache reuse |
| Generator | `python site/sync_colab.py --check` passed for all four generated copies |
| Upstream integration | New Survival source and updated helper match origin/main bytes exactly |

Scientific training, cross-validation, bootstrap, interpretation, patient reports and pipeline reconstruction cells were not reduced or skipped. Environment packages were installed before notebook execution; setup reused and checked those exact pins. Fresh network bootstrap is covered by mocks, not a real Colab service test. Final execution reports and rendered notebook outputs are in ignored `outputs/showcase-validation-final/`. An earlier Survival run was invalidated when setup was regenerated during execution; only final unchanged-source runs are reported above.

## Remaining service checks

The browser runtime failed to start, so authenticated Google Colab execution, Colab's preinstalled-package interactions and visual website checks remain unverified. Google's runtime FAQ was checked on 9 November 2026 and lists 2026.07 / Python 3.12.13. Select that runtime before setup; installing another interpreter does not change the kernel. If it is unavailable, use a local Python 3.12 environment for these showcases. If `pip check` reports a Colab-specific conflict, setup stops rather than reporting readiness; retain that output for investigation.

Binder has subsequently been updated to the compatible KaleCancer revision with its own NumPy 2.5.4 lock, and both Cancer Binder buttons are restored. Full local Linux execution of both Cancer showcases and both Cardiac tutorials passed; see `.binder/README.md` for current results and hosted limitations. Cardiac setup and the Binder controller are unchanged.

After review, publish both generated showcase copies and all matching support files together; hash mismatches deliberately stop setup on mixed revisions. Public Colab URLs serving the new copies cannot be verified before publication. No Sphinx build, site preview, commit or push was performed.

---

# Direct Google Colab notebooks: implementation and validation

Validated locally on **3 November 2026**. No commit, push or deployment was performed.

## Hub compatibility correction after a real Colab failure

The user reported a real Colab 2026.07 import failure: Transformers required `huggingface-hub>=1.5.0,<2.0`, but this setup had pinned Hub 2.3.0. The earlier local environments lacked optional Transformers, so they did not exercise the Lightning/TorchMetrics Transformers import path. Those earlier tests did not establish compatibility with Colab's preinstalled stack.

The [official Colab 2026.07 package inventory](https://github.com/googlecolab/backend-info/blob/ec53f93fe44a9cab118dc5451527b18e36e1a643/pip-freeze.txt) lists Transformers **5.13.1**. Its [release metadata](https://pypi.org/pypi/transformers/5.13.1/json) confirms Hub `>=1.5.0,<2.0`. The pinned KaleCancer commit requires Hub `>=0.24`. [Hub 1.33.0 release metadata](https://pypi.org/pypi/huggingface-hub/1.33.0/json) confirms a published Python-3.12-compatible 1.x release within both ranges. It depends on `httpx>=0.23,<1`, so the old Hub-2-only HTTP client pins were replaced as well:

- `huggingface-hub==2.3.0` ? `huggingface-hub==1.33.0`
- `httpx2==2.16.0` ? `httpx==0.28.1`
- `httpcore2==2.16.0` ? `httpcore==1.0.9`

All other research pins, the KaleCancer source commit, training code and scientific cells remain unchanged. Transformers is still optional and is not installed or upgraded by the participant setup. When present, its installed Hub constraint is checked before importing KaleCancer. The local verification environment explicitly includes Transformers 5.13.1, Tokenizers 0.22.2 and Safetensors 0.8.0, reproducing the previously missing import path.

The setup now tracks already imported `huggingface_hub`, `transformers`, `tokenizers`, `httpx` and `httpcore` modules as well as the scientific stack. A real local process imported Hub 2.3.0, ran the corrected setup, installed Hub 1.33.0 on disk, and correctly stopped with **Restart session** rather than reporting readiness while the old module remained in memory. A fresh process then reached **MDAS ready** with Hub 1.33.0. This validates the Python process behaviour; it is not a direct Colab UI restart test.

For the failed Colab session: open the updated Colab copy after the fix is published, run setup, choose **Runtime > Restart session** if requested, and rerun setup. Do not continue until **MDAS ready** prints **Hub 1.33.0**. Reopening a notebook without restarting its existing runtime does not unload old imported modules.

Correction validation:

| Check | Result |
| --- | --- |
| Old full requirements plus Transformers 5.13.1 | Pip reproduced `ResolutionImpossible`: Hub 2.3.0 conflicts with `>=1.5,<2` |
| Corrected full requirements plus Transformers 5.13.1 | Fresh resolution (`--dry-run --ignore-installed`) and actual installation passed without dependency overrides |
| Installed environment | `pip check`: **No broken requirements found**; Transformers, Hub and KaleCancer/Pipeline imports passed |
| Classification with Transformers present | All **26 code cells** passed, including setup, full training, baseline, evaluation and advanced analysis; about **14.9 seconds** |
| Survival with Transformers present | All **29 code cells** passed, including setup, full training, baseline, survival evaluation and bootstrap analysis; about **17.6 seconds** |
| Already-loaded Hub downgrade | Real process blocked until restart; fresh process imported the corrected stack successfully |
| Regressions | `sync_colab.py --check`, all 9 setup/preservation tests, generated notebook HTML/ToC/link checks and all 17 JavaScript tests passed |
| Website rebuild | Strict Sphinx build passed; 27 HTML pages and 1,423 local links/assets checked; zero errors |
| Copy integrity and hashes | Both copies regenerated; `python site/sync_colab.py --check` passed; all four originals byte-identical; all original scientific cells preserved in each copy |

Correction artifacts are ignored under `tmp/hub-*` and `outputs/hub-fix/`. The original local validation table below is retained as history; its environments lacked Transformers. This correction changes only the requirement pins, setup safety/compatibility checks and instructions, setup-cell hashes in the two copies, regression tests and this report. Website design and Binder integration are unchanged. No commit or push was performed. Direct execution of this correction in Colab remains a final manual check.

## Participant workflow

MDAS website → choose **Classification** or **Survival Analysis** → **Run in Google Colab** → select Python 3.12 → run the initial setup cell → run scientific cells directly, individually and in order.

The website offers exactly two primary execution actions:

- **Run with Binder** uses the original notebook and existing in-page Binder controller.
- **Run in Google Colab** opens `classification_colab.ipynb` or `survival_colab.ipynb`.

The direct copies add one initial Markdown cell and one setup code cell. Every original cell dictionary follows unchanged, in its original order: scientific source, explanatory Markdown, IDs, metadata, saved outputs and execution counts. The original notebook files themselves are never written. The optional blank exercises remain unchanged.

## Runtime availability and dependency evidence

[Google's runtime FAQ](https://research.google.com/colaboratory/runtime-version-faq.html) and [official backend information](https://github.com/googlecolab/backend-info) were checked on 3 November 2026. They currently list **2026.07 / Python 3.12.13** as an available runtime and **2026.10 / Python 3.13.18** as the newer runtime. This is verification of Google's published availability list, not an authenticated account/UI test. Availability may change.

At the top of each copy, participants are instructed to choose **Runtime > Change runtime type > Runtime Version > 2026.07**, then reconnect. If that runtime is not offered, use Binder. The actual active kernel must report Python 3.12 before setup proceeds; downloading a different interpreter is not treated as a kernel change.

The current [PyKale 0.2.1 metadata](https://pypi.org/pypi/pykale/0.2.1/json) still requires Python `<3.13`, PyTorch `<=2.6.0`, pandas `<=2.2.2` and NumPy `>=2.0.0`. The existing [KaleCancer source pin](https://github.com/pykale/cancer/blob/1f476fdba87f515286f732cd7eaa92ffeeffdbc2/pyproject.toml) requires Python `>=3.11,<3.13`, PyTorch `>=2.6`, pandas `>=2.2`, and PyKale. Current KaleCancer main also declares Python `<3.13`. No verified constraint-respecting stack was found for the current default Python 3.13 Colab runtime, so these copies explicitly require the documented Python 3.12 runtime.

`colab-requirements.txt` pins the scientific dependency closure based on the existing Binder lock, excluding its kernel/IPython-only packages. NumPy is pinned to **2.0.2**, matching Google's documented 2026.07 base and satisfying both research packages. All dependencies are installed through normal pip resolution; there is no `--no-deps`, `--ignore-requires-python`, editable root-project install, or source patch to bypass compatibility constraints.

Key pins:

| Dependency | Version/source |
| --- | --- |
| KaleCancer | Git commit `1f476fdba87f515286f732cd7eaa92ffeeffdbc2` |
| PyKale | 0.2.1 |
| PyTorch / Torchvision | 2.6.0+cpu / 0.21.0+cpu |
| NumPy / pandas | 2.0.2 / 2.2.2 |
| h5py | 3.16.0 |
| scikit-learn | 1.9.1 |
| Lightning / PyTorch Lightning | 2.6.6 |
| torchsurv | 0.1.6 |
| jsonargparse | 4.53.0 |
| Hugging Face Hub | 1.33.0 |
| HTTPX / HTTPCore | 0.28.1 / 1.0.9 |

The CPU Torch index is official. No imaging, pathology, interpretation, TabICL or development extras are installed. The required PyTorch downgrade is necessary to satisfy PyKale's declared cap. Installation is into the **active interpreter** (`sys.executable -m pip`), so the following scientific cells use the installed packages directly, without a kernel proxy or notebook runner.

## Bootstrap and paths

The two small setup cells share `colab_setup.py` and `colab-requirements.txt`; `site/sync_colab.py` generates the copies and embeds the support-file SHA-256 values. In a fresh Colab runtime, setup downloads only those support files from the MDAS public `main`, verifies their hashes before executing code (normalizing support-file line endings to LF for Windows/GitHub consistency), and caches them under `/content/mdas-cancer/notebooks/MDAS/cancer`. A local checkout can supply the same files during testing.

`main` is used for these new support files because the copies and helper must be published together. The embedded hashes bind a notebook copy to its exact support-file revision. If a later `main` no longer serves the matching version and no verified cached copy exists, setup stops and asks the participant to reopen the latest notebook rather than silently executing different setup code. Regenerate both copies whenever the helper or requirement file changes:

```text
python site/sync_colab.py
python site/sync_colab.py --check
```

The unchanged companion `synthetic_data_generation.py` is retrieved from MDAS commit `5e3eac4145944c38932b8ec2c78cbc08b7af068a`, with its own verified SHA-256. An existing local scientific helper is never overwritten. Setup adds the Cancer directory to `sys.path`, sets it as the working directory, and imports the tutorial APIs before reporting **MDAS ready**. Thus the original import and `../../../data/synthetic_data` path work unchanged. Data is still generated by the original scientific cells, with their original seeds and task choices. Setup does not substitute datasets or run training automatically.

Reruns check the installed scientific pins and KaleCancer VCS provenance. They reuse correct dependencies and cached files. If a scientific library is already loaded at a different version, installation cannot safely replace its live binary state: setup stops with **Runtime > Restart session**, followed by rerunning setup. It never reports readiness while holding a detected stale scientific library. The notebook file and original scientific cells are unaffected by a session restart.

## Preservation checks

Baseline repository revision: `5e3eac4145944c38932b8ec2c78cbc08b7af068a`.

| Protected original | SHA-256 of unchanged file bytes |
| --- | --- |
| `classification.ipynb` | `46519696d7800288112fdc3c2da16a3c65c83ee32086b591743eba933ed5a2d5` |
| `survival.ipynb` | `e21eeb2e9bd4abb28a2606239539984f7dd5f2a7c47e99c2d536df11c767db82` |
| `classification_blank.ipynb` | `a03663a39aad4e0c4f3ba00be90c8573e05e7d40e2c9457de6767260dae68080` |
| `survival_blank.ipynb` | `618e010bc1b0c72951733273fbfe5455c97b3e4281613a3f0a842dfaffa44f90` |

Git diffs and initial-file hashes confirm all four originals are unchanged. There are no changes to `.binder/`, its controller/adapter, the selector JavaScript, presentation code, the scientific helper, root `pyproject.toml`/`uv.lock`, logo, venue, timing or Pages workflow.

## Measured validation

Tests ran on local Windows/Python 3.12.10; these are not Colab measurements.

| Check | Result |
| --- | --- |
| Classification Colab copy, initially empty research environment | All **26 code cells** passed: setup plus all 25 original scientific cells. Setup about **104.6 seconds**; total about **114.4 seconds** |
| Survival Colab copy, fresh kernel reusing installed dependencies | All **29 code cells** passed: setup plus all 28 original scientific cells. Setup about **3.5 seconds**; total about **16.6 seconds** |
| Independent fresh Survival environment | All **29 code cells** passed in a second empty research environment and isolated checkout; setup about **106.3 seconds**; total about **119.9 seconds** |
| Original Classification regression | All 25 code cells passed, about **15.0 seconds**, source unchanged |
| Original Survival regression | All 28 code cells passed, about **17.7 seconds**, source unchanged |
| Research dependency check | `pip check` passed in the fresh direct-copy test environment |
| Setup rerun in the same process | Reused pinned dependencies; no reinstall; repeated readiness check passed |
| Real GitHub companion download | Pinned source and checksum verified |
| Fresh support-download bootstrap | Mocked network verified both support downloads, hash checks, cache reuse and delegation to the active-kernel setup |
| Runtime/provenance safety | Unsupported Python rejected before install/download; wrong KaleCancer commit not reused; mismatched loaded libraries require restart |
| Failure handling | Temporary test notebook stops on first failing cell, preserves source bytes, saves a partial report and removes a stale success HTML report |
| Website | Strict clean-source Sphinx builds passed with Binder enabled and disabled; 27 HTML pages; **1,423 enabled** and **1,415 disabled** local links/assets; zero errors |
| Tests | Seven direct-Colab regression tests, generated notebook HTML/link/ToC/button checks, failure integration check, and all 17 existing JavaScript controller/presentation tests passed |
| Button styling | Scoped blue backgrounds and `#FFFFFF` text in link/visited/hover/focus/active/disabled states; contrast checks above 4.5:1; keyboard outline and mobile rules checked in source |

No training epochs, evaluations, baseline fits, bootstrap intervals or other scientific cells were reduced or skipped. `site/tests/execute_notebooks.py` is a **maintainer validation tool only**, running each tested notebook in its own explicit fresh kernel and saving outputs outside the source directory. Participants execute their Colab cells directly; this script is not part of their workflow.

Validation artifacts are ignored: `outputs/colab-validation/`, `outputs/original-regression/`, and `tmp/` contain executed copies, HTML reports, source checksums, cell timings and logs. The source notebooks and Colab copies are never output destinations.

## Remaining manual checks

Direct Google Colab UI/runtime execution and browser visual validation remain **unverified**. The browser tool reported an unavailable access host/native pipe. Successful local execution does not establish successful Colab execution or actual rendered button colours in a browser.

After review and publication of all new files together:

1. From the MDAS Classification page, select **Run in Google Colab**. Confirm the URL ends in `classification_colab.ipynb`. Choose the listed Python 3.12 runtime and start a fresh CPU session, without Drive or uploaded files.
2. Run setup. If asked, restart the session and rerun setup; wait for **MDAS ready**. Run all original scientific cells individually, including both full 40-epoch training fits and advanced analysis. Check the final table and rerun setup to verify safe reuse.
3. Repeat in a separate fresh session for `survival_colab.ipynb`, including survival metrics, baseline fit and bootstrap intervals. Record actual setup/execution times and any Colab-specific conflicts.
4. In the default Python 3.13 runtime, verify that setup stops before installing and provides the runtime-selection instruction. If Python 3.12 is not actually offered in the account, use Binder and report that limitation.
5. On desktop/mobile and in light/dark mode, inspect both blue execution buttons, white text in normal/visited/hover/focus/active states, and keyboard focus. Check dropdown switching, Binder launch, edited-notebook download and presentation mode. Binder must still display and execute the original selected notebook.

New public URLs cannot be verified until these uncommitted files are reviewed and published. There is no automatic commit, push or deployment in this task.

## Files created, changed and removed

New:

- `notebooks/MDAS/cancer/classification_colab.ipynb`
- `notebooks/MDAS/cancer/survival_colab.ipynb`
- `notebooks/MDAS/cancer/colab_setup.py`
- `notebooks/MDAS/cancer/colab-requirements.txt`
- `notebooks/MDAS/cancer/README-colab.md`
- `site/sync_colab.py`
- `site/tests/test_colab.py`
- `site/tests/execute_notebooks.py`
- `site/tests/check_notebook_worker.py`

Modified: `site/conf.py`, `site/_static/mdas-notebooks.css`, `site/tests/test_notebooks.py`, `site/README.md`, `docs/colab.md`, and `docs/notebook-execution.md`.

Removed obsolete files: `colab/prepare_colab.ipynb`, `colab/environment.py`, `colab/run_notebooks.py`, `colab/requirements.txt`, `colab/README.md`, `colab/tests/test_workflow.py`, and `colab/tests/check_worker.py`. Their useful validation behaviour is replaced by the new tests and maintainer execution utility above. No unrelated files were deleted.
