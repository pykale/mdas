# What is MDAS?

The **Multimodal Data Analysis Session (MDAS)** is organised by the **CMI** AIRE team with the support of **UKOMAIN**. It introduces practical research workflows through two PyKale domain packages: KaleCancer and KaleCardiac.

## One question, complementary measurements

A clinical table, pathology features, an ECG and a chest X-ray describe different aspects of a person. Multimodal research asks whether combining appropriate measurements helps answer a defined question, and how to test that claim without leakage or overinterpreting a small experiment.

| Fusion approach | When inputs are combined |
| --- | --- |
| Early fusion | Put the input measurements together before learning a shared representation. |
| Intermediate fusion | Learn a representation of each input, then combine those representations before making a prediction. |
| Late fusion | Make a prediction from each input first, then combine the predictions. |

| Analysis | Question it answers | Cancer example |
| --- | --- | --- |
| Classification | Which category does a person belong to? | [KaleCancer Classification](../notebooks/MDAS/cancer/classification_showcase.ipynb) |
| Survival analysis | How does event risk vary when follow-up is incomplete? | [KaleCancer Survival Analysis](../notebooks/MDAS/cancer/survival_showcase.ipynb) |

## Research in practice

The examples help you identify a research endpoint, follow an analysis from inputs to predictions, explain its metrics, and distinguish a synthetic demonstration from clinically meaningful evaluation. You can read the saved notebook outputs before choosing an execution environment. Synthetic demonstrations teach the software workflow; they do not establish clinical performance or replace external clinical evaluation.

(workshop-and-independent-learning)=

## Session and independent learning

**Wednesday, 18 November 2026, 13:00–17:00**.

**Venue:** Ada Lovelace Room (108), Level 1, Regent Court, University of Sheffield. See the [Session Agenda](agenda.md) for the programme.

The live session has two blocks: **Learn the Pipeline**, then **Apply the Pipeline** with the AIRE team available to help. The materials also support self-paced study after the session. Specific organiser-provided problems and final exercise selection remain to be confirmed.

The [Participation Guide](participation.md) covers preparation for the session or independent study.
