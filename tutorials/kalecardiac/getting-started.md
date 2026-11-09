# Cardiac: Getting Started

## Overview

The two Cardiac tutorials show how [KaleCardiac](https://github.com/pykale/cardiac) learns representations from multiple cardiac modalities. **CardioVAE** fuses a **chest X-ray (CXR)** with a **twelve-lead electrocardiogram (ECG)**; **LS-EMVAE** treats each of the twelve ECG leads as a modality of its own.

Each tutorial pretrains a multimodal variational autoencoder (VAE) without labels, then fine-tunes a classifier for a binary endpoint: **0**, healthy, or **1**, cardiothoracic abnormality. Both start from raw DICOM files, the format in which hospitals export these investigations.

## Choose a tutorial

| | CardioVAE | LS-EMVAE |
| --- | --- | --- |
| **Modalities** | Chest X-ray + twelve-lead ECG | The twelve ECG leads, each a modality of its own |
| **Model** | An encoder and a decoder per modality, fused by a product of experts | An encoder per lead, hierarchical modality experts (HiME) fusion and one decoder shared by every lead |
| **Pretraining objective** | Tri-stream ELBO: both modalities together, and each alone, so each encoder stays useful when the other modality is missing | ELBO over every lead, plus a latent alignment term that keeps each lead's representation usable when other leads are absent |
| **Fine-tuning input** | Both modalities | The six limb leads by default; all twelve with `USE_12_LEADS = True` |
| **Notebook** | [Open CardioVAE](../../notebooks/MDAS/cardiac/tutorial-CardioVAE.ipynb) | [Open LS-EMVAE](../../notebooks/MDAS/cardiac/tutorial-LSEMVAE.ipynb) |

Each notebook runs on its own. If you plan to run both in the same folder, start with CardioVAE: LS-EMVAE then reuses the dataset CardioVAE has already downloaded.

## The tutorial dataset

The tutorial dataset contains paired twelve-lead ECGs and chest X-rays stored as DICOM, in two folders: an unlabelled cohort for pretraining and a labelled cohort for fine-tuning.

```text
data/
├── kalecardiac_pretraining/   ECG/ and CXR/: one folder per subject, holding its DICOM file
└── kalecardiac_finetuning/    the same layout, plus labels.csv (subject_id,label)
```

A notebook cell downloads it as one ZIP archive of about **400 MB**, without sign-in, and unpacks it into `data/` beside the notebook. LS-EMVAE reads only the ECGs.

## The workflow

Both notebooks follow the same five steps, each a few calls to the KaleCardiac API:

| Step | What you do |
| --- | --- |
| **0. Environment preparation** | Install KaleCardiac, download the tutorial dataset and load the two configuration files. |
| **1. Multimodal pretraining** | Load the unlabelled DICOM files, prepare them to the shape the model reads, and pretrain the VAE. Pretraining is a reconstruction task, so it needs no labels. |
| **2. Multimodal fine-tuning** | Load the labelled cohort, divide its subjects into training, validation and test sets, and train a classification head on the frozen pretrained encoders. |
| **3. Evaluation** | Score the held-out test subjects with accuracy, AUROC, MCC, sensitivity and specificity. LS-EMVAE also scores them again as leads are withheld, down to lead I alone. |
| **4. Interpretation** | Use integrated gradients to find which modalities or leads the predictions rested on, and where in each signal or image. Withhold each modality or lead in turn and score again. |

Each subject's ECG is prepared as ten seconds recorded at 500 Hz, which gives 5,000 time points per lead. CardioVAE interleaves the twelve leads into one strip of 60,000 values (12 leads × 5,000 time points) and resizes the CXR to 224 × 224; LS-EMVAE keeps each lead as a separate signal of 5,000 time points.

## Configuration files

Each tutorial reads two [YACS](https://github.com/rbgirshick/yacs) configuration files from its `configs/` folder, each merged onto KaleCardiac's defaults. Fine-tuning starts from the pretrained model, so the fine-tuning file is merged onto the pretraining configuration.

| Tutorial | Pretraining | Fine-tuning |
| --- | --- | --- |
| **CardioVAE** | `config_cardiovae_pretrain.yaml`: ECG and CXR shape, latent width, tri-stream objective and a 10-epoch schedule | `config_cardiovae_finetune.yaml`: labelled cohort, endpoint, train/validation/test split and a 20-epoch schedule |
| **LS-EMVAE** | `config_lsemvae_pretrain.yaml`: the twelve leads, lead encoders, HiME fusion, alignment term and a 10-epoch schedule | `config_lsemvae_finetune.yaml`: the six limb leads, endpoint, split and a 20-epoch schedule |

The same files are in the [tutorial folder of the KaleCardiac repository](https://github.com/pykale/cardiac/tree/main/tutorials/mdas_tutorial). Change a setting in a file, or override it in the notebook's **Hyperparameters to play with** cells.

## Run a tutorial

Open the [Live-Coding Notebook](../../notebooks/MDAS/cardiac/tutorial-CardioVAE.ipynb) and choose a tutorial, then run it in one of three ways.

### On this website (Binder)

1. Select **Run with Binder** and wait for **Kernel connected**. Starting a session can take several minutes.
2. Run the cells in order, starting with the package installation cell in Step 0. It installs KaleCardiac into the session and fetches the configuration files; the dataset cell then downloads the data.
3. Binder runs on a CPU, so training takes longer than on a GPU. Sessions are temporary: copy any code edits or results you want to keep.

### In Google Colab

1. Select **Run in Google Colab**.
2. Choose **Runtime > Change runtime type > T4 GPU**. The tutorials also run on a CPU, more slowly.
3. Run the cells in order, starting with the package installation cell. Expect about **10 minutes** on a T4 GPU, installation included.

### On your own computer

Use Python **3.10, 3.11 or 3.12** and install a [PyTorch build compatible with your hardware](https://pytorch.org/get-started/locally/). Then install KaleCardiac with the two extras the tutorials need:

```sh
git clone https://github.com/pykale/cardiac.git
cd cardiac
pip install -e ".[imaging,interpret]"
```

The `imaging` extra adds pydicom and scikit-image for reading DICOM files; `interpret` adds Captum for integrated gradients. Open `tutorial-CardioVAE.ipynb` or `tutorial-LSEMVAE.ipynb` from `tutorials/mdas_tutorial` in Jupyter or VS Code, **skip the package installation cell**, and run the remaining cells in order.

Each tutorial writes its checkpoints and training logs under `outputs/` beside the notebook, in separate folders, so both tutorials can run in the same folder.

## As you work

- **CardioVAE:** check the shape each modality is prepared to. Compare each modality's attribution ratio with the test AUROC when that modality is withheld. Ask what happens to a subject whose chest X-ray or ECG is missing.
- **LS-EMVAE:** find where the fine-tuning leads are set, and compare pretraining without labels with fine-tuning on the endpoint. Watch the test AUROC as leads are withheld. Ask why a lead can be strongly attributed yet redundant when other leads carry the same information.
- **Both:** AUROC does not depend on a decision threshold, whereas accuracy, MCC, sensitivity and specificity are computed at 0.5. Compare them to separate how well the model ranks subjects from how it classifies them.

## Beyond the notebooks

The KaleCardiac repository runs both models from the command line, with cross-validation, ablations and a written report. Without a dataset path, these examples generate synthetic cohorts:

```sh
python -m examples.cardiovae_multimodal.main --cfg examples/cardiovae_multimodal/configs/quick.yaml
python -m examples.lsemvae_ecg.main --cfg examples/lsemvae_ecg/configs/quick.yaml
```

For details, see the [KaleCardiac quickstart](https://github.com/pykale/cardiac/blob/main/docs/quickstart.md), the [examples overview](https://github.com/pykale/cardiac/blob/main/examples/README.md), the [CardioVAE](https://github.com/pykale/cardiac/blob/main/examples/cardiovae_multimodal/README.md) and [LS-EMVAE](https://github.com/pykale/cardiac/blob/main/examples/lsemvae_ecg/README.md) example READMEs, and the [API overview](https://github.com/pykale/cardiac/blob/main/API_overview.md).

> [!NOTE]
> Use only the tutorial dataset on public services such as Binder and Colab, and keep identifiable patient data in approved, secure environments. See the [Participation Guide](../../docs/participation.md). The software continues to evolve; confirm the supported session environment with the organisers.

**Next:** [Open the Live-Coding Notebook](../../notebooks/MDAS/cardiac/tutorial-CardioVAE.ipynb).
