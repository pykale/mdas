# Prerequisites

## Before attending

- Bring a laptop and be comfortable running basic Python commands.
- Choose whether to explore cancer survival modelling, cardiac ECG leads, or ECG + chest X-ray fusion.
- Start with synthetic data: no patient dataset is required for the introductory examples.

## Software requirements

| Track | Software | Setup |
| --- | --- | --- |
| Cancer | Python 3.11 or 3.12, [uv](https://docs.astral.sh/uv/), and the [KaleCancer repository](https://github.com/pykale/cancer) | [Cancer Quick Start](quick-start.md#cancer-quick-start) |
| Cardiac | Python 3.10, 3.11 or 3.12, compatible PyTorch, PyKale, and the [KaleCardiac repository](https://github.com/pykale/cardiac) | [Cardiac Quick Start](quick-start.md#cardiac-quick-start) |

The two repositories have different setup procedures. Do not assume one environment works for both. Confirm the supported session environment with the organisers; the linked repository instructions describe the current public code, but a successful installation on your machine still needs checking.

## Safe use of research data

Synthetic examples demonstrate the software workflow and do not establish clinical usefulness. If planning to use your own data, discuss permissions, privacy, expected data layout and compute requirements with the organisers first.

> [!CAUTION]
> Do not upload identifiable patient data, confidential material or private datasets to public services or this repository. Use clinical data only with appropriate permissions and secure infrastructure.

[Quick Start](quick-start.md) · [Tutorials](../tutorials/README.md).
