# Cancer: hands-on activity

> [!NOTE]
> This is a proposed session activity using the synthetic survival example.

## 1. Run and observe

From the Cancer repository root:

```sh
uv run python examples/synthetic/synthetic_survival.py
```

Record:

- Which data types are combined
- Which outcome is predicted
- Which evaluation metric is reported

## 2. Follow the pipeline

Open `examples/synthetic/synthetic_survival.py` and find:

1. Creation of the synthetic clinical table and patch features.
2. Generation of survival times and censoring indicators.
3. Construction of the model/pipeline.
4. Training and evaluation.

## 3. Discuss the research question

- Why is censoring important for time-to-event outcomes?
- Why should records from one patient remain in the same data split?
- What information might pathology patches add to clinical covariates?

## Optional advanced reading

The [Cancer quickstart](https://github.com/pykale/cancer/blob/main/docs/quickstart.md) documents HANCOCK examples, including `examples/hancock/survival_intermediate.py`, `from_config.py`, `cross_validation.py` and `classification_late.py`. These require a **local HANCOCK dataset** and are **not part of the no-data starter exercise**.

[Getting started](getting-started.md) · [Results and interpretation](results.md) · [Participation guide](../../docs/participation.md).
