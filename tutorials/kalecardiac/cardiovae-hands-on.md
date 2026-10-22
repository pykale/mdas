# CardioVAE hands-on

## Combining ECG and chest X-ray information

The `cardiovae_multimodal` example pairs ECG and chest X-ray modalities. Its repository README describes **product-of-experts multimodal variational representation learning**, followed by fine-tuning on a **haemodynamic endpoint**.

## Run the quick configuration

From the `cardiac-main` checkout:

```sh
python -m examples.cardiovae_multimodal.main --cfg examples/cardiovae_multimodal/configs/quick.yaml
```

> [!WARNING]
> With no dataset path, the example uses generated cohorts. Any resulting metric is a synthetic pipeline check, not a clinical result.

## Proposed participant prompts

1. **Identify the input modalities.** Identify the two input modalities.
2. **Find the configuration file.** Find the configuration file `examples/cardiovae_multimodal/configs/quick.yaml`.
3. **Identify the endpoint and saved results.** Identify the endpoint and locate the saved results.
4. **Discuss missing modalities.** Discuss what could happen when one modality is missing.

For experiment-specific data requirements and output file names, see `examples/cardiovae_multimodal/README.md` in the `cardiac-main` development snapshot.

> [!NOTE]
> These activities are provisional; the final session exercises are still to be confirmed.

[Getting started](getting-started.md) · [LS-EMVAE hands-on](lsemvae-hands-on.md) · [Results and interpretation](results.md).
