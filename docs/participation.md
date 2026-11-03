# Participation Guide

Join us on **Wednesday, 18 November 2026, 13:00–17:00**.

**Venue:** Regent Court, University of Sheffield; The Diamond is a possible alternative.

## Who this is for

Researchers, clinicians, data scientists, research software engineers and PhD students who want to understand a multimodal analysis workflow. Basic Python helps: you should be comfortable with imports, functions and reading a table. Clinicians can follow the research question, predictions and interpretation without writing every line of code.

## What to bring

- A laptop, charger and a modern browser with internet access for online execution.
- A question about your research: what is the outcome, and which measurements are available for each person?
- No patient dataset is needed. Start with the supplied synthetic examples.

## Choose an execution route

| Route | Preparation |
| --- | --- |
| Cancer on this website | Use Binder to request a temporary kernel, then run cells in order. First startup may take several minutes. |
| Cancer in Google Colab | Open the dedicated Colab copy, select a compatible Python 3.12 runtime, then run its setup cell. Follow any restart instruction before continuing. |
| Optional local setup | Cancer and Cardiac use separate repositories and environments. Follow Quick Start for the commands; a successful install still needs a test run. |

Local Cancer examples support Python 3.11 or 3.12. The Cardiac instructions use Python 3.10, 3.11 or 3.12 with compatible PyTorch and PyKale. Do not assume one environment serves both tracks.

## In person or at your own pace

At the workshop, use the first block to learn the pipeline and the second to explore a research question with support from the AIRE team. Specific organiser-provided problems remain to be confirmed. The [Session Agenda](agenda.md) contains the detailed programme and venue confirmation arrangements.

Learning independently? Choose one track, complete a synthetic run, and record the endpoint, modalities, outputs and one limitation. Return to the interpretation page before changing a configuration. The same materials remain available after the event.

## Synthetic data and privacy

Synthetic results show that a pipeline runs; they do not establish clinical usefulness. Do not upload identifiable patient data, confidential research, credentials or private datasets to public services or this repository. Before using your own data, discuss permissions, secure infrastructure, expected data layout and compute needs with the organisers or your research team.

**Next:** [Choose an execution route in Quick Start](quick-start.md).
