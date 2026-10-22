# Multimodal Data Analysis Session (MDAS)

## Cancer & Cardiac Research

The Multimodal Data Analysis Session (MDAS), hosted by the PyKale organization, introduces practical workflows for combining biomedical data using KaleCancer and KaleCardiac, two domain-focused libraries built on PyKale. Participants will explore synthetic examples and discuss how these workflows could support cancer and cardiac research questions.

This repository contains participant documentation for the November 2026 session and is organized for AI-assisted indexing by DeepWiki.

## Audience and learning objectives

The session is for AI/ML researchers, data scientists, research software engineers, clinicians, clinical researchers and PhD students working with, or planning to work with, cancer or cardiac data. Some Python experience and a laptop are recommended in the draft invitation. Clinicians can focus on inputs, outcomes, interpretation and limitations; technical participants can also inspect configuration and code.

Participants should become better able to identify relevant modalities and a research endpoint, follow an example end to end, distinguish synthetic pipeline checks from clinically meaningful evaluation, explain fusion strategies and metrics, and identify constraints for applying a workflow to their own data.

## Proposed date and location

**Draft, subject to organizer confirmation:** Wednesday 18 November 2026, 1–5 PM, Regent Court. The draft proposes an application deadline of 6 November, notification by 10 November, and an optional pre-session briefing on 11 November. See the [agenda and proposed logistics](docs/agenda.md).

## Navigation

| Section | What you will find |
| --- | --- |
| [Quick Start](docs/quick-start.md) | The source cardiac installation and synthetic example commands |
| [Overview](docs/overview.md) | What to explore and where to begin |
| [About the session](docs/about.md) | What MDAS is, its purpose and proposed format |
| [Participation](docs/participation.md) | Suggested activity loop and research discussion prompts |
| [Agenda](docs/agenda.md) | Exact proposed timetable, learning goals and draft logistics |
| [Prerequisites](docs/prerequisites.md) | Preparation, software requirements and data permissions |
| [Tutorials overview](tutorials/README.md) | Choose a domain track |
| [KaleCancer](tutorials/kalecancer/README.md) | Setup, synthetic survival exercise and interpretation |
| [KaleCardiac](tutorials/kalecardiac/README.md) | Setup, CardioVAE, LS-EMVAE and interpretation |
| [Notebooks](notebooks/README.md) | Where real notebooks will be added and how to access them |
| [Resources](docs/resources.md) | Project repositories, snapshot references and support |
| [Migration checklist](MIGRATION_CHECKLIST.md) | Verification, missing materials and organizer review items |

## Two tutorial tracks

**KaleCancer:** Combine clinical variables and pathology patch features through intermediate fusion in a Cox time-to-event model. The starter exercise generates a synthetic cohort with censored survival times. Real-data HANCOCK extensions require separate dataset access and setup.

**KaleCardiac:** Explore CardioVAE for chest X-ray + ECG multimodal representation learning, or LS-EMVAE for lead-specific ECG representations and fine-tuning with a subset of leads. Both starter workflows can generate synthetic cohorts.

> [!IMPORTANT]
> Examples using synthetic data demonstrate software workflows; they are not evidence of clinical predictive performance or clinically validated results. Do not upload identifiable patient data, confidential material or private datasets to this repository or public services.

## Software snapshots and repositories

The documentation preserves commands from the **KaleCancer `cancer-refactor` snapshot** and **KaleCardiac `cardiac-main` snapshot** described in the source PDF. They have different setup procedures. Commands have not been execution-tested during migration and must not be assumed valid on current public default branches. The source archives and notebooks are not included here.

Verified project repositories: [PyKale](https://github.com/pykale/pykale), [KaleCancer](https://github.com/pykale/cancer), and [KaleCardiac](https://github.com/pykale/cardiac). These public links do not identify the exact development revisions used by the PDF.

## Documentation source and status

The documentation was migrated from all 30 pages of the local GitBook PDF export. Draft status, technical paths, commands, warnings and scientific distinctions are preserved; print artifacts and empty navigation divider pages are omitted. The source PDF remains local in the Git-ignored `source-material/` directory. DeepWiki can index the Markdown after organizer review and publication; no website deployment is required.
