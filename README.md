# Multimodal Data Analysis Session (MDAS)

## Cancer & Cardiac Research

## Welcome and Introduction

Welcome to the Multimodal Data Analysis Session (MDAS), hosted by the PyKale organisation. This hands-on session introduces multimodal biomedical data analysis through KaleCancer and KaleCardiac, two domain-focused libraries built on PyKale.

Explore how different types of biomedical data can be combined, follow practical examples, and discuss how these workflows could support your cancer or cardiac research.

## Session Information

**Provisional — subject to confirmation by the organisers.**

- **Date:** Wednesday, 18 November 2026
- **Time:** 1:00–5:00 PM
- **Location:** Regent Court, University of Sheffield

See the [session agenda](docs/agenda.md) for the proposed timetable and other provisional arrangements.

## Who Should Attend

MDAS is for AI/ML researchers, data scientists, research software engineers, clinicians, clinical researchers and PhD students working with, or planning to work with, cancer or cardiac data.

Some Python experience and a laptop are recommended. Clinicians can focus on the data, predicted outcomes, interpretation and limitations; technical participants can also explore configurations and code.

## What You Will Learn

- Recognise early, intermediate and late multimodal fusion strategies.
- Follow a practical workflow from data preparation and encoding through fusion, prediction, evaluation and interpretation.
- Explore synthetic-data examples without needing patient datasets.
- Interpret model evaluation measures and distinguish software pipeline checks from clinically meaningful evaluation.
- Identify relevant modalities, research endpoints and practical constraints for cancer and cardiac applications.

## Getting Started

| Section | What you will find |
| --- | --- |
| [Quick Start](docs/quick-start.md) | Cardiac setup and synthetic example commands |
| [Overview](docs/overview.md) | What to explore and where to begin |
| [About MDAS](docs/about.md) | Purpose and proposed session format |
| [Session Agenda](docs/agenda.md) | Proposed timetable, learning goals and logistics |
| [Prerequisites](docs/prerequisites.md) | Software requirements and preparation |
| [Participation Guide](docs/participation.md) | Suggested activities and discussion prompts |
| [Tutorials Overview](tutorials/README.md) | Choose a domain track |
| [KaleCancer](tutorials/kalecancer/README.md) | Synthetic survival analysis and interpretation |
| [KaleCardiac](tutorials/kalecardiac/README.md) | CardioVAE and LS-EMVAE workflows |
| [Jupyter Notebooks](notebooks/README.md) | Notebook availability and access information |
| [Resources](docs/resources.md) | Official repositories, technical references and support |

## Tutorial Tracks

**KaleCancer:** Combine clinical variables and pathology patch features through intermediate fusion in a Cox time-to-event model. Generate a synthetic cohort with censored survival times, follow the training pipeline, and discuss survival evaluation. Real-data HANCOCK extensions require separate dataset access and setup.

**KaleCardiac:** Explore CardioVAE for chest X-ray + ECG multimodal representation learning, or LS-EMVAE for lead-specific ECG representations and fine-tuning with a subset of leads. Use synthetic cohorts to examine configuration, saved outputs, missing modalities and interpretation.

## Hands-on Jupyter Notebooks

Notebook tutorials will be available in the dedicated `notebooks/kalecancer/` and `notebooks/kalecardiac/` folders. **No session notebooks are available in this repository yet.** See [Jupyter Notebooks](notebooks/README.md) for access and setup information. GitHub and compatible Google Colab execution links will be added when the notebooks are available.

## Resources

- [PyKale](https://github.com/pykale/pykale)
- [KaleCancer](https://github.com/pykale/cancer)
- [KaleCardiac](https://github.com/pykale/cardiac)

See [Resources](docs/resources.md) for technical references and library support.

## Important Notes

- Synthetic examples demonstrate software workflows; their results are not evidence of clinical predictive performance or clinically validated findings.
- The tutorials use the KaleCancer `cancer-refactor` and KaleCardiac `cardiac-main` development snapshots. Their setup procedures differ, and compatibility with current public default branches is not guaranteed. Confirm the session revisions with the organisers.
- Use clinical data only with appropriate permissions and secure infrastructure. Do not upload identifiable patient data, confidential material or private datasets to this repository or public services.
