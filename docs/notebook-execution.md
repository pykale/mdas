---
orphan: true
---

# Execution Help

This guide opens in a new tab so your notebook page and active kernel can stay in place. Choose the notebook first, then one execution route. Reading the saved cells alone does not run code.

## Binder: run on this website

Binder runs the selected Cancer notebook on this website using a temporary kernel. Google Colab opens a dedicated copy in a separate runtime.

1. Choose **Run with Binder**. The page first checks that the public GitHub revision contains the notebook and Binder files, then requests a temporary kernel. It does not run notebook cells automatically.
2. Wait for **Kernel connected**. A first build or busy public service can take several minutes. Keep the page open and read the connection status; repeated clicks do not speed up startup.
3. Edit and run cells individually, from the first cell onwards. Later cells depend on earlier variables. Run training and advanced comparisons deliberately; they add CPU time.

For Cancer, the kernel starts in `notebooks/MDAS/cancer/`, making `synthetic_data_generation.py` and the showcase companion `synthetic_showcase_data.py` importable and the original data path valid. Binder uses the public repository revision, not files from your local checkout.

### Switching, saving and temporary sessions

Each example has its own page, linked from the sidebar and tutorial overview. Variables, edits and results are not transferred. After launch, the browser asks before leaving via links, reloads or closing the tab. **Cancel** to stay and copy code edits and important results into local files first. A warning does not save work for you.

Binder sessions can disconnect or expire. The website has no edited-notebook export or general generated-file download interface. If you need to retain generated files, choose Colab and use its Files pane, or work locally. Save before leaving rather than relying on a temporary kernel.

### Connection failure and recovery

- **Missing environment or notebook files:** the public revision is not ready. Local package changes cannot repair files missing on GitHub. Record the message and ask the organiser to check the published revision.
- **GitHub timeout or rate limit:** wait and retry later. This is different from a failed package installation.
- **Failed or disconnected kernel:** copy any work still visible, then reload and launch a new session. Run cells from the beginning; old variables cannot be assumed to survive. If the Binder service provides build logs, use them to distinguish build, server startup and kernel errors.

An eventual kernel connection does not guarantee every research cell will finish within the service's resource limits. Colab or a local environment is an alternative when public Binder is unavailable.

## Colab: run the dedicated copy

**Run in Google Colab** opens `classification_showcase_colab.ipynb` for Classification and `survival_showcase_colab.ipynb` for Survival Analysis. Each copy preserves the selected source notebook's scientific cells and adds an initial setup section. Both **Run with Binder** and **Run in Google Colab** are available for either Cancer showcase; each route has its own compatible environment. See the [Colab guide](colab.md) for details.

1. Select a compatible **Python 3.12** runtime as explained at the top of that notebook. Runtime selection is a participant action; installing another Python executable does not change the active kernel.
2. Run the initial setup cell. It retrieves support files and installs compatible research packages in the active environment. The first installation may take several minutes.
3. If requested, choose **Runtime > Restart session**, then rerun setup. Continue only when **MDAS ready** appears. After the corrected Hub setup, that message should include **Hub 1.33.0**; an already imported old Hub or Transformers stack needs a restart.
4. Run scientific cells individually in order, including their data generation, training and evaluation steps.
5. Save a notebook copy and download needed data/results using Colab's File menu and Files pane before disconnecting. A new Colab session does not automatically retain an earlier runtime's files or variables.

For runtime selection, a setup failure or a checksum/version message, follow the [Colab troubleshooting guide](colab.md). A failed setup is not permission to skip ahead to the scientific cells.

## Cardiac setup

Open [KaleCardiac CardioVAE](../notebooks/MDAS/cardiac/tutorial-CardioVAE.ipynb) or [KaleCardiac LS-EMVAE](../notebooks/MDAS/cardiac/tutorial-LSEMVAE.ipynb). **Run in Google Colab** opens that authored notebook in Colab; its own Step 0 prepares the environment.

1. Run the package installation cell. It installs `kalecardiac[imaging,interpret]` from its repository, fetches the tutorial configurations and changes into the tutorial folder.
2. Run the dataset cell. It downloads and extracts about **400 MB** of public tutorial DICOM data. The unlabelled cohort is for pretraining; the labelled cohort is for fine-tuning. Both examples can reuse this data in a shared folder.
3. Run the remaining cells in order. Each tutorial loads separate pretraining and fine-tuning configuration files; its notebook cells expose settings to explore. Checkpoints and training logs are written in separate output folders.
4. For Cardiac Colab, use a compatible Python 3.12 runtime where offered; that is the Python version used in the local shared-environment checks. A T4 GPU can accelerate training, while CPU execution also works. The current default Colab runtime has not been verified here. If a compatible runtime is unavailable, use Run locally; installing another interpreter does not change the kernel. Resolve any installation error before proceeding.

For **Run locally**, use [Quick Start](quick-start.md#cardiac). Do not mix a local checkout and an older installed copy. Public services must use only the tutorial data; save work before leaving a temporary session.

## Privacy and interpretation

Use synthetic data only on public execution services. Do not upload identifiable patient data, confidential research, private datasets or credentials. Synthetic metrics demonstrate a workflow, not clinical usefulness.
