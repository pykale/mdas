---
orphan: true
---

# Execution Help

This guide opens in a new tab so your notebook page and active kernel can stay in place. Choose the notebook first, then one execution route. Reading the saved cells alone does not run code.

## Binder: run on this website

1. Choose **Run with Binder**. The page first checks that the public GitHub revision contains the notebook and Binder files, then requests a temporary kernel. It does not run notebook cells automatically.
2. Wait for **Kernel connected**. A first build or busy public service can take several minutes. Keep the page open and read the connection status; repeated clicks do not speed up startup.
3. Edit and run cells individually, from the first cell onwards. Later cells depend on earlier variables. Run training and advanced comparisons deliberately; they add CPU time.

The kernel starts in `notebooks/MDAS/cancer/`, making `synthetic_data_generation.py` and the Classification companion `synthetic_showcase_data.py` importable and the original data path valid. Binder uses the public repository revision, not files from your local checkout.

### Switching, saving and temporary sessions

The Classification/Survival dropdown loads a separate page. Variables, edits and results are not transferred. After launch, the site asks before switching and the browser also protects reloads, links and closing the tab. **Cancel** to stay and copy code edits and important results into local files first. A warning does not save work for you.

Binder sessions can disconnect or expire. The website has no edited-notebook export or general generated-file download interface. If you need to retain generated files, choose Colab and use its Files pane, or work locally. Save before leaving rather than relying on a temporary kernel.

### Connection failure and recovery

- **Missing environment or notebook files:** the public revision is not ready. Local package changes cannot repair files missing on GitHub. Record the message and ask the organiser to check the published revision.
- **GitHub timeout or rate limit:** wait and retry later. This is different from a failed package installation.
- **Failed or disconnected kernel:** copy any work still visible, then reload and launch a new session. Run cells from the beginning; old variables cannot be assumed to survive. If the Binder service provides build logs, use them to distinguish build, server startup and kernel errors.

An eventual kernel connection does not guarantee every research cell will finish within the service's resource limits. Colab or a local environment is an alternative when public Binder is unavailable.

## Colab: run the dedicated copy

**Run in Google Colab** opens `survival_colab.ipynb` for Survival Analysis, preserving its scientific cells and adding an initial **Google Colab Environment Setup** section. Classification now displays `classification_showcase.ipynb`. Its Colab action is disabled because the current KaleCancer pin lacks required showcase interpretation APIs; full Binder execution has the same blocker. It never launches the old Classification example as a substitute. See the [Colab guide](colab.md) for details.

1. Select a compatible **Python 3.12** runtime as explained at the top of that notebook. Runtime selection is a participant action; installing another Python executable does not change the active kernel.
2. Run the initial setup cell. It retrieves support files and installs compatible research packages in the active environment. The first installation may take several minutes.
3. If requested, choose **Runtime > Restart session**, then rerun setup. Continue only when **MDAS ready** appears. After the corrected Hub setup, that message should include **Hub 1.33.0**; an already imported old Hub or Transformers stack needs a restart.
4. Run scientific cells individually in order, including their data generation, training and evaluation steps.
5. Save a notebook copy and download needed data/results using Colab's File menu and Files pane before disconnecting. A new Colab session does not automatically retain an earlier runtime's files or variables.

For runtime selection, a setup failure or a checksum/version message, follow the [Colab troubleshooting guide](colab.md). A failed setup is not permission to skip ahead to the scientific cells.

## Privacy and interpretation

Use synthetic data only on public execution services. Do not upload identifiable patient data, confidential research, private datasets or credentials. Synthetic metrics demonstrate a workflow, not clinical usefulness.
