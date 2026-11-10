# KaleCardiac Overview

[KaleCardiac](https://github.com/pykale/cardiac) is a Python library for multimodal cardiovascular machine learning, built on [PyKale](https://github.com/pykale/pykale). It works with ECG, chest X-ray, cardiac imaging and clinical data. Its API is a pipeline of modules, each named for what it does:

```text
loaddata  →  prepdata  →  model  →  pipeline  →  evaluate  →  interpret
 access      transform    learn      train        score        explain
                            │
                            ├─ layers   building blocks
                            ├─ embed    CardioVAE, LS-EMVAE and fusion
                            └─ predict  heads and objectives
```

The `auto` module runs these stages from a single configuration, and the tutorials use it for pretraining and fine-tuning.

The library is organised around two features of cardiac data. Recordings are easy to collect but labels are expensive, so a model first learns from unlabelled recordings and is then fine-tuned on a labelled cohort. Modalities also go missing in practice, so models keep working when an input is absent.

## The tutorial notebooks

Each notebook builds a published model from raw DICOM files using the [KaleCardiac API](https://github.com/pykale/cardiac/blob/main/API_overview.md). You will find both under **KaleCardiac API Notebooks** in the sidebar.

| | CardioVAE | LS-EMVAE |
| --- | --- | --- |
| **Input data** | Chest X-ray and twelve-lead ECG | Twelve-lead ECG, with each lead as its own modality |
| **Model** | An encoder and a decoder for each modality, fused by a product of experts | An encoder for each lead, hierarchical fusion and one decoder shared by all leads |
| **Pretrained on** | Paired ECGs and chest X-rays | All twelve leads |
| **Fine-tuned on** | Both modalities | The six limb leads, or all twelve |
| **Missing inputs** | Withholds each modality in turn and scores again | Withholds leads one after another, down to lead I |
| **Notebook** | [Open CardioVAE](../../notebooks/MDAS/cardiac/tutorial-CardioVAE.ipynb) | [Open LS-EMVAE](../../notebooks/MDAS/cardiac/tutorial-LSEMVAE.ipynb) |

## What you will do

Both tutorials follow the same five steps:

1. **Set up:** install KaleCardiac and download the tutorial data.
2. **Pretrain:** the model learns from the data without any labels.
3. **Fine-tune:** a classifier is trained on top of the model using labelled data.
4. **Evaluate:** the model is tested on subjects it has not seen.
5. **Interpret:** you see which inputs, and which parts of them, the predictions relied on.

Each tutorial runs in Google Colab, which provides the GPU it uses for training.
