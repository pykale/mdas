# Prerequisites

## Before attending

- Bring a laptop and be comfortable running basic Python commands.
- Choose whether you want to explore **cancer survival modelling**, **cardiac ECG leads**, or **ECG + chest X-ray fusion**.
- The demonstrations use **synthetic data**, so no patient dataset is required for initial exploration.
- If planning to use your own data, discuss permissions, privacy and compute requirements with the organisers first.

> [!CAUTION]
> Do not upload identifiable patient data to public services or this documentation repository.

## Software paths

**KaleCancer (`cancer-refactor` development snapshot):** Python **3.11 or 3.12**, [uv](https://docs.astral.sh/uv/), and a checkout of the corresponding source. See [KaleCancer setup](../tutorials/kalecancer/getting-started.md).

**KaleCardiac (`cardiac-main` development snapshot):** Python **3.10–3.12**, PyTorch appropriate to the machine, PyKale and a checkout of KaleCardiac. See [KaleCardiac setup](../tutorials/kalecardiac/getting-started.md).

> [!WARNING]
> The two repositories have different setup procedures. Do not assume one environment works for both. Use the exact revision intended for your tutorial; confirm the supported environment with the organisers before the session.

[Quick Start](quick-start.md) · [Tutorials overview](../tutorials/README.md).
