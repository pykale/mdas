# LS-EMVAE hands-on

## Different ECG leads as complementary views

The `lsemvae_ecg` example treats individual ECG leads as separate modalities. Its source README describes **representation pretraining on multi-lead recordings** and **fine-tuning using a subset of leads** for a **pulmonary hypertension task**.

## Run the quick configuration

From the `cardiac-main` checkout:

```sh
python -m examples.lsemvae_ecg.main --cfg examples/lsemvae_ecg/configs/quick.yaml
```

Without a dataset path, this generates synthetic cohorts. It does not reproduce the published clinical findings.

## Proposed participant prompts

1. **Identify configuration.** Identify where lead names and fine-tuning lead subsets are configured.
2. **Compare training stages.** Compare the meaning of pretraining without labels and fine-tuning with an endpoint.
3. **Discuss limited lead availability.** Discuss why a model might need to work with fewer available leads.
4. **Examine output descriptions.** Examine the output descriptions in `examples/lsemvae_ecg/README.md`, including lead importance and ablation.

## Optional configuration exploration

The example README documents an optional comparison of lead sets:

```sh
python -m examples.lsemvae_ecg.main --leads I,I+II,I+II+III
```

> [!WARNING]
> Treat configuration experiments as optional, subject to facilitator testing before session day.

Source: PDF pages 23–24. [Getting started](getting-started.md) · [CardioVAE hands-on](cardiovae-hands-on.md) · [Results and interpretation](results.md).
