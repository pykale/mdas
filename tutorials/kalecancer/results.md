# KaleCancer: results and interpretation

## Reading a synthetic survival run

The example illustrates a **Cox time-to-event workflow** using synthetic clinical and patch data. The refactor documentation identifies **Harrell's C** as a survival evaluation measure used in its examples; real-data HANCOCK examples also document **Uno's C**.

A concordance measure summarizes how well risk ordering agrees with observed event-time information. It is not a probability of survival for an individual patient.

## Questions for participants

- Which input modalities were available?
- How are events and censored observations represented?
- What is the difference between risk ranking and clinical calibration?
- Why must a synthetic-data score not be reported as clinical predictive performance?

## Next steps

The real-data HANCOCK examples require access to the dataset, the expected local directory structure, and further compute. Consult `docs/quickstart.md` in the supplied refactor snapshot before attempting them.

**Source:** `cancer-refactor/docs/quickstart.md` and `examples/synthetic/synthetic_survival.py`, as cited on PDF page 20. No experimental scores were supplied in the PDF.

[About KaleCancer](README.md) · [Getting started](getting-started.md) · [Hands-on activity](hands-on.md) · [Resources](../../docs/resources.md).
