# Participation Guide

Join us on **Wednesday, 18 November 2026, 13:00–17:00**.

**Venue:** Ada Lovelace Room (108), Level 1, Regent Court, University of Sheffield.

## Who this is for

Researchers, clinicians, data scientists, research software engineers and PhD students who want to understand a multimodal analysis workflow. Basic Python helps: you should be comfortable with imports, functions and reading a table. Clinicians can follow the research question, predictions and interpretation without writing every line of code.

## What to bring

- A laptop, charger and a modern browser with internet access for online execution.
- A question about your research: what is the outcome, and which measurements are available for each person?
- No patient dataset is needed. Start with the supplied synthetic examples.

## Choose an execution route

| Route | Preparation |
| --- | --- |
| Binder on this website | Open the [Cancer notebook page](../notebooks/MDAS/cancer/classification.ipynb) or [Cardiac notebook page](../notebooks/MDAS/cardiac/tutorial-CardioVAE.ipynb), choose a tutorial, and select **Run with Binder**. Binder starts a temporary kernel on the site; first startup may take several minutes. Follow that notebook's documented setup and run cells in order. |
| Google Colab | Open the [Cancer notebook page](../notebooks/MDAS/cancer/classification.ipynb) or [Cardiac notebook page](../notebooks/MDAS/cardiac/tutorial-CardioVAE.ipynb) and select **Run in Google Colab** to open the notebook for your chosen track. Follow its documented runtime and setup instructions, including any requested session restart. |
| Optional local setup | Cancer and Cardiac use separate repositories and environments. Follow Quick Start for the commands; a successful install still needs a test run. |

**Cancer and Cardiac:** Binder runs the selected notebook on this website; Colab opens its dedicated notebook. Follow the selected notebook's setup instructions; see [Execution Help](notebook-execution.md).

Local Cancer examples support Python 3.11 or 3.12. The Cardiac instructions use Python 3.10, 3.11 or 3.12 with compatible PyTorch and PyKale. Do not assume one environment serves both tracks.

## In person or at your own pace

At the session, use the first block to learn the pipeline and the second to explore a research question with support from the AIRE team. Specific organiser-provided problems remain to be confirmed. The [Session Agenda](agenda.md) contains the detailed programme.

Learning independently? Choose one track, complete a synthetic run, and record the endpoint, modalities, outputs and one limitation. Return to the interpretation page before changing a configuration. The same materials remain available after the event.

## Synthetic data and privacy

Synthetic results show that a pipeline runs; they do not establish clinical usefulness. Do not upload identifiable patient data, confidential research, credentials or private datasets to public services or this repository. Before using your own data, discuss permissions, secure infrastructure, expected data layout and compute needs with the organisers or your research team.

**Next:** [Choose an execution route in Quick Start](quick-start.md).
