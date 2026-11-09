# Cardiac

<span id="overview"></span>

[KaleCardiac](https://github.com/pykale/cardiac) explores complementary cardiac measurements. Its examples learn representations from unlabelled investigations, then use labelled subjects to train and evaluate a classifier.

<span id="choose-a-tutorial"></span>

## Choose an example

| Example | What it demonstrates |
| --- | --- |
| [KaleCardiac CardioVAE](../../notebooks/MDAS/cardiac/tutorial-CardioVAE.ipynb) | Combine a chest X-ray and a twelve-lead ECG, then inspect how each contributes to a prediction. |
| [KaleCardiac LS-EMVAE](../../notebooks/MDAS/cardiac/tutorial-LSEMVAE.ipynb) | Learn from complementary ECG leads and examine predictions as leads are withheld. |

<span id="the-workflow"></span>
<span id="the-tutorial-dataset"></span>

The notebooks follow preparation, pretraining, fine-tuning, evaluation and interpretation. They use the public tutorial dataset of paired ECGs and chest X-rays stored as DICOM files: an unlabelled pretraining cohort and a labelled fine-tuning cohort. A cell downloads the dataset as a ZIP archive of about **400 MB**. LS-EMVAE uses the ECGs only.

<span id="run-a-tutorial"></span>

## Run an example

Each example page offers **Run with Binder** and **Run in Google Colab**. Start with its Step 0 installation and download cells; see [Cardiac setup](../../docs/notebook-execution.md#cardiac-setup). For **Run locally**, follow [Quick Start](../../docs/quick-start.md#cardiac).

<span id="configuration-files"></span>

Each notebook works independently. In a shared working folder, CardioVAE can download the dataset first and LS-EMVAE can reuse it. Checkpoints and logs go into separate output folders. The notebook configuration cells expose settings you can explore; the matching files are in the [KaleCardiac tutorial folder](https://github.com/pykale/cardiac/tree/main/tutorials/mdas_tutorial).

## As you work

Compare performance and explanations when inputs are available or withheld. An attribution describes what this model uses; it does not establish a causal or clinically reliable finding. The no-data command-line examples in Quick Start use generated cohorts; they are a separate entry point from these DICOM notebooks.

<span id="beyond-the-notebooks"></span>

Use only the tutorial data on public services. Keep identifiable patient data in approved, secure environments, and plan independent evaluation before making clinical claims. For further work, see the [KaleCardiac quickstart](https://github.com/pykale/cardiac/blob/main/docs/quickstart.md) and [examples overview](https://github.com/pykale/cardiac/blob/main/examples/README.md).
