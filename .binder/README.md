# Temporary Cancer notebook environment

`runtime.txt` selects Python 3.12. `requirements.in` describes the deliberately CPU-only environment; `requirements.txt` pins the resolved Linux x86-64 dependency graph, including the Cancer commit already recorded in the research `uv.lock`. No imaging, pathology, TabICL or interpretation extras are requested. Torchvision is a transitive PyKale dependency and is also resolved to a CPU wheel. There are no CUDA/NVIDIA runtime packages.

These files use the standard repo2docker `.binder/` layout and do not install or change the MDAS research project itself. No postBuild/start hooks, credentials, private data or Windows paths are needed. Binder supplies its own Jupyter server; the environment includes the Python kernel. The full repository checkout supplies the companion helper.

Thebe requests a Python kernel with working directory `notebooks/MDAS/cancer/`. Thus `from synthetic_data_generation import make_cohort` works as a same-directory import, and `../../../data/synthetic_data` resolves to repository-local synthetic data. The helper creates this directory at the participant's request; neither the Binder build nor the website build trains a model or generates data.

## Regenerate dependency pins

From the repository root, using uv:

```powershell
uv pip compile .binder/requirements.in --python-version 3.12 --python-platform x86_64-unknown-linux-gnu --index-strategy unsafe-best-match --emit-index-url --output-file .binder/requirements.txt
```

Review any changed packages before publishing. Both the PyPI registry and official PyTorch CPU registry are used. The Cancer code is pinned to commit `1f476fdba87f515286f732cd7eaa92ffeeffdbc2`. The requirements pin the Python dependency graph, not the Binder base image or every OS library, so the entire image is not a bit-for-bit lock. Do not add large optional extras just to make an import error disappear.

## Validation status

- A direct public Binder launch cloned `main` at `ed163a322186055c8c5b79885288ad9a051f89c4`, then returned `No environment specification found` followed by `phase: failed`. This is an environment-discovery failure, before dependency installation or kernel connection. That public revision has neither `.binder/runtime.txt` nor `.binder/requirements.txt`; the notebook and helper are already public.
- The local runtime definitions are ready for review but cannot repair the public launch while they remain local. The minimum remote change is to add `.binder/runtime.txt` and `.binder/requirements.txt` on the configured ref. Publish `requirements.in` and this README with them for maintainability. No notebook/helper replacement is needed for this failure, and no patient data or generated HTML is needed in the Binder environment.
- The complete CPU dependency graph resolved successfully for Python 3.12/Linux x86-64.
- The helper was smoke-tested locally with its pinned NumPy, pandas and h5py versions: it generated 100 synthetic clinical rows and 100 valid patch files, totalling about 1.76 MB. Temporary test data were removed; no training ran.
- The final Binder image, full ML import stack and notebook training have **not** been tested. Docker was not running locally. Public Binder cannot see these local files until the reviewed changes are pushed to the configured revision.
- The original notebook is unchanged, including saved outputs. Training is 40 epochs; the optional baseline and bootstrap comparisons can add CPU time. Public Binder has limited, temporary resources. The complete run needs a timed memory/CPU smoke test before participants rely on it.
- Colab requires the separate setup procedure in `docs/notebook-execution.md`. No claim of a verified Colab session is made.

See `site/README.md` for end-to-end tests, disabling Thebe, or choosing another BinderHub. The Binder configuration can also be used with a local repo2docker installation or another compatible service; the static documentation remains independently buildable.

References: [repo2docker configuration](https://repo2docker.readthedocs.io/en/latest/configuration/), [Python runtime selection](https://repo2docker.readthedocs.io/en/latest/configuration/system/), and [public Binder resource limits](https://mybinder.readthedocs.io/en/latest/about/user-guidelines.html).
