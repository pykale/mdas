# Cancer: Getting Started

## The research question

What can clinical variables and pathology patch features tell us together that a clinical table alone cannot? Cancer research may ask for a **class label** or for **time-to-event risk**. These are different questions, with different targets and evaluation methods.

The MDAS notebooks use small synthetic cohorts so you can learn the workflow without patient data. The patch features are generated numerical vectors, not real pathology images or evidence that an image encoder works clinically.

## Classification: predict a category

The Classification notebook predicts **early** versus **late**, the synthetic labels in the `stage` column. Inputs are clinical **age and gender**, together with bags of **32-dimensional pathology patch features**. The target column is removed from the clinical inputs.

Age is imputed and standardised; gender is encoded categorically. An attention-based multiple-instance encoder (**ABMIL**) pools each subject's patch bag. The clinical and patch representations are concatenated, then a classification head produces class probabilities. This is intermediate fusion: the representations are combined before the prediction head.

You will trace subject identifiers across modalities, keep fitted preprocessing inside the training pipeline, and inspect **AUROC for the late class** and **balanced accuracy**. The advanced section compares the fused model with a clinical-only baseline using AUROC bootstrap intervals.

## Survival Analysis: predict relative event risk

Survival analysis uses both a follow-up **time** and an **event indicator**. An observed event means the event occurred at that time. A censored observation means the event was not observed by the end of that person's follow-up; it does not mean the event can never occur.

The Survival notebook combines clinical **age, stage and gender** with pathology patch features. Its `time` and `event` target columns are excluded from the clinical inputs. Age is imputed and standardised; **stage and gender** are encoded categorically. Stage is an input here, unlike Classification where the synthetic stage label is the target.

The same intermediate-fusion pattern leads to a **Cox head** with Efron handling of tied event times. Its prediction is a **log-hazard score** for relative risk ordering, not a survival probability or an estimated number of days. You will examine **Harrell's C** and **Uno's C at a horizon of 1,825 time units**, then compare a clinical-only baseline using Harrell's C bootstrap intervals.

## What to do and observe

Follow one notebook in order: generate data, load each modality and target, construct the model, fit on the training split, and evaluate on the held-out split. Both notebooks use an 80/20 split and 40 training epochs; the optional baseline adds another fit. First inspect the saved cells if you want to understand the sequence before launching execution.

As you work, record the target, input columns, prediction shape and metric. Ask why records from the same subject must stay in one split, why transformations must be fitted on training data, and what information patches might add beyond clinical variables. The interpretation page will help you separate a runnable workflow from a research claim.

**Next:** [Choose and run the Live-Coding Notebook](../../notebooks/MDAS/cancer/classification.ipynb).
