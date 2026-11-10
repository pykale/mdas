# Cancer: Results and Interpretation

Start with the prediction table, then the held-out metrics, and finally the baseline comparison. The two notebooks answer different questions; a classification score and a survival concordance score are not interchangeable.

## Classification: Results and Interpretation

### What the predictions mean

`pipeline.predict(test)` returns `probability[early]` and `probability[late]` for each held-out subject. These model probabilities refer to the synthetic categories. They are not calibrated estimates of a real patient's disease stage or outcome.

The notebook reports two metrics:

| Metric | What to ask |
| --- | --- |
| **AUROC**, with `late` as the positive class | Does the model tend to rank late-labelled subjects above early-labelled subjects across score thresholds? This measures discrimination, not calibration. |
| **Balanced accuracy** | How well does the resulting class decision recover each class? For these two classes it averages their recalls, so the larger class does not dominate as it would in ordinary accuracy. |

### Compare, then question the result

The advanced section fits a clinical-only baseline and reports bootstrap intervals for **fused AUROC**, **clinical-only AUROC**, and their difference, labelled **gain from the slides**. Examine the difference and its uncertainty rather than just comparing two point estimates. An interval spanning zero does not establish a clear positive gain on this sample; an interval away from zero would still not demonstrate clinical usefulness.

Common mistakes are treating AUROC as a probability of a correct individual prediction, assuming good ranking guarantees calibrated probabilities, or concluding that adding a modality must improve performance. The synthetic generator deliberately creates a relationship between patch features and labels. A small held-out cohort and its bootstrap intervals do not represent an external clinical study.

## Survival Analysis: Results and Interpretation

### Read risk alongside follow-up

`pipeline.predict(test)` returns a `log_hazard` score. Larger scores indicate higher relative event risk under this model. The score is neither an event time nor a survival probability at a chosen horizon.

Interpret risk ordering using both **time and event status**. A censored subject is not a known event-free negative for all future time. Their follow-up is only partially observed, so an ordinary classification comparison would discard important information.

| Metric | What to ask |
| --- | --- |
| **Harrell's C** (`harrell_c`) | Among comparable pairs, how often does predicted risk ordering agree with observed event ordering? Censoring affects which pairs can be compared. |
| **Uno's C** (`uno_c_5y`) | How does risk ranking perform with inverse-probability-of-censoring weighting up to `tau=1825.0`? The name suggests five years if the time unit is days; synthetic time units do not establish a clinical horizon. |

Concordance concerns ranking, not calibration. A useful risk ordering does not prove that individual survival probabilities or clinical decisions would be reliable. The notebook does not evaluate a survival-probability calibration curve.

The advanced section reports **Harrell's C** bootstrap intervals for the fused model, clinical-only baseline and their difference. It does not use Classification's AUROC comparison or an Uno's C bootstrap comparison. Censoring assumptions, follow-up, the small cohort and the synthetic data-generating process all limit interpretation.

## Further research

Before changing a model, write down a testable question: what information should the extra modality add, and how would a subject-level split assess it? The [Cancer research examples](https://github.com/pykale/cancer/tree/main/examples/hancock) include intermediate survival fusion, configuration-driven pipelines, cross-validation and late-fusion classification. These require access to a local HANCOCK dataset, its expected layout and appropriate compute; they are not no-data starter exercises.

## Responsible interpretation

A synthetic run demonstrates data flow, training and evaluation code. It does not establish clinical validity, generalisation to a new cohort or causality of an attributed feature. Use subject-level separation, fit transformations on training data, assess uncertainty and missing modalities, and plan external evaluation before making real-world claims. Real clinical data require permissions and secure infrastructure.
