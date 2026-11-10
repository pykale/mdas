# Overview

[KaleCardiac](https://github.com/pykale/cardiac) is a Python library for multimodal cardiovascular machine learning, built on [PyKale](https://github.com/pykale/pykale). It supports multiple data modalities, including cardiac imaging, physiological signals, and clinical data. Its API follows a modular pipeline architecture, with each module named according to its functionality:

```text
loaddata  →  prepdata  →  model  →  pipeline  →  evaluate  →  interpret
(access)    (transform)  (learn)     (train)    (metrics)     (explain)
```

The library is organised around two features of cardiac data. Data are easy to collect but labels are expensive, so a model first learns from unlabelled datas and is then fine-tuned on a labelled cohort. Modalities also go missing in practice, so models keep working when an input is absent.

## The tutorial notebooks

Each notebook builds a published model from raw DICOM files using the [KaleCardiac API](https://github.com/pykale/cardiac/blob/main/API_overview.md). You will find both under **Cardiac Overview** in the sidebar.

| | Chest X-ray and ECG | 12-lead ECG |
| --- | --- | --- |
| **Input data (Modality)** | Chest X-ray and 12-lead ECG | 12-lead ECG, with each lead as separate modality |
| **Model** | An encoder and a decoder for each modality; the two encodings are fused by a product of experts (PoE) into one shared latent representation | An encoder for each of the 12 leads and one decoder shared by all of them; the 12 encodings are fused by hierarchical modality experts (HiME) into one shared latent representation |
| **Pretrained on** | Paired 12-lead ECGs and chest X-rays | 12-lead ECGs |
| **Fine-tuned on** | Both modalities, or 12-lead ECG or chest X-rays  | Six limb lead ECG, or 12-lead ECG |
| **Missing modalities** | 12-lead ECG or chest X-rays | Any ECG leads |
| **Notebook** | [Open Chest X-ray and ECG](../../notebooks/MDAS/cardiac/tutorial-CardioVAE.ipynb) | [Open 12-lead ECG](../../notebooks/MDAS/cardiac/tutorial-LSEMVAE.ipynb) |

## What you will do

Both tutorials follow the same five steps:

1. **Set up:** install KaleCardiac and download the tutorial data.
2. **Pretrain:** the model learns from the data without any labels.
3. **Fine-tune:** a classifier is trained on top of the model using labelled data.
4. **Evaluate:** the model is tested on subjects it has not seen.
5. **Interpret:** you see which inputs, and which parts of them, the predictions relied on.

Each tutorial runs in Google Colab, which provides the GPU it uses for training.
