# KaleCardiac: results and interpretation

## What the examples save

The `cardiac-main` quickstart describes synthetic example outputs under `outputs/`, including configurations, predictions, and metrics. The individual example READMEs describe more detailed artefacts such as `results.csv`, `metrics.json`, and interpretation reports. The LS-EMVAE example also documents `lead_importance.csv`.

## Interpret carefully

> [!WARNING]
> **Synthetic performance:** Confirms that the demonstration pipeline executes; it is not evidence of clinical usefulness.

- **Classification metrics:** Interpret ROC-AUC, sensitivity, and specificity in the context of the endpoint and the study population.
- **Lead importance:** Attribution and modality ablation ask different questions. A lead can have high attribution yet provide little unique information when other leads are present.
- **Missing modalities:** Consider whether performance and interpretation change when ECG leads or an imaging modality are unavailable.

## Reflection questions

1. What clinical endpoint is being predicted?
2. Which modalities are present and which might be missing in practice?
3. What would be required before drawing conclusions on real patient cohorts?

[About KaleCardiac](README.md) · [CardioVAE hands-on](cardiovae-hands-on.md) · [LS-EMVAE hands-on](lsemvae-hands-on.md) · [Resources](../../docs/resources.md).
