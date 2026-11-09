---
orphan: true
---

# Run the Cancer notebooks in Google Colab

For **Survival Analysis**, choose it on the Live-Coding Notebook page, then select **Run in Google Colab** to open its self-configuring copy.

**Classification showcase setup is blocked:** the current KaleCancer dependency pin (`1f476fd`) lacks required interpretation APIs, including `modality_shapley`, `feature_shapley` and `attention_heatmap`. Its Colab action is disabled rather than opening the old example or an unprepared copy. The same pin also prevents full showcase execution in Binder. Read the saved showcase on the website while a compatible environment is prepared.

- [Survival Analysis in Google Colab](https://colab.research.google.com/github/pykale/mdas/blob/main/notebooks/MDAS/cancer/survival_colab.ipynb)

## Before running: Python 3.12

In Colab select **Runtime > Change runtime type > Runtime Version > 2026.07**, then reconnect. Google currently lists this Python 3.12 runtime in its [runtime documentation](https://research.google.com/colaboratory/runtime-version-faq.html), checked on 3 November 2026. Runtime availability can change; if it is not offered, use **Run with Binder** on the website.

The default Python 3.13 runtime is outside the published KaleCancer and PyKale requirements. Installing another interpreter does not change the active notebook kernel. The setup checks that kernel's Python version before downloading or installing anything.

## Run cells directly

1. Run the initial **Google Colab Environment Setup** code cell. It installs compatible CPU research packages in this notebook's active Python environment and downloads the companion module. No separate notebook, Drive mount, uploaded files or terminal commands are needed.
2. If setup says a different library version is already loaded, choose **Runtime > Restart session** and rerun setup. This prevents mixing old, loaded libraries with newly installed packages, including Hugging Face Hub and Transformers. After updating an earlier failed setup, wait for **MDAS ready** to print **Hub 1.33.0** before running scientific cells. Continue only after **MDAS ready** appears.
3. Run the scientific cells individually in order. Training and advanced analyses run in full. Rerunning setup reuses compatible dependencies and cached support files.
4. Save a notebook copy through Colab's File menu and download generated files through its Files pane before disconnecting. Colab runtimes are temporary. Use synthetic data only.

The setup arranges `notebooks/MDAS/cancer/` beneath `/content/mdas-cancer/`, adds that directory to the import path and changes the working directory there. Thus the original `from synthetic_data_generation import make_cohort` and `../../../data/synthetic_data` work without editing any scientific cell. Each notebook generates its own appropriate synthetic task with the original deterministic generator.

The four original notebooks, blank exercises, Binder requirements and Binder controller are unchanged. **Run with Binder** uses the selected notebook on the website; the Classification showcase currently has the setup limitation above. Colab copies add only this setup section; all original cell dictionaries, ordering, metadata and saved outputs are preserved.

## If setup does not reach MDAS ready

Keep the error message. An unsupported Python version needs a runtime selection, not another interpreter installed in a cell. A download or checksum error may require reopening the latest Colab copy and rerunning setup with internet access. If a different package version is already imported, restart the session and rerun setup until **MDAS ready** appears; do not continue with a partly configured environment.

For notebook switching, temporary sessions and saving work across both execution routes, see [Execution Help](notebook-execution.md).

## Compatibility and validation

The Colab research stack uses Python 3.12, PyTorch 2.6 CPU, PyKale 0.2.1, the existing pinned KaleCancer Git commit, NumPy 2.0.2, pandas 2.2.2, scikit-learn 1.9.1 and Lightning 2.6.6. NumPy matches the documented Colab 2026.07 base version. Setup installs the required PyTorch version because the preinstalled newer release does not satisfy PyKale's cap. Unrelated kernel/IPython packages are not replaced. No Python-version or dependency constraints are bypassed.

Direct Colab UI execution has not been verified in this development environment. Complete local executions, preservation checks, exact dependency details and the final fresh-session Colab checklist are documented in the [validation report](https://github.com/pykale/mdas/blob/main/notebooks/MDAS/cancer/README-colab.md). Local execution is not a claim that Colab UI/runtime behaviour has been tested. The new notebook copies and their support files must be published together after review before their public links can work.
