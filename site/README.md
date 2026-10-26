# MDAS website build

This directory contains the Sphinx + MyST Parser + Sphinx Book Theme configuration. Participant content remains authoritative in the root `README.md`, `docs/`, `tutorials/` and `notebooks/README.md`. Edit those pages, then rebuild; do not edit generated copies.

## Build from Windows PowerShell

From the repository root:

```powershell
python .\site\build.py
```

Python and uv must be installed. The script finds uv on `PATH` or in its standard WinGet package directory. If necessary, set `$env:UV_EXECUTABLE` to the full path of your installed `uv.exe` and repeat the command.

The build uses an isolated uv tool environment with the exact documentation tool versions in `site/requirements.txt`: Sphinx 9.2.0, MyST Parser 5.1.0, Sphinx Book Theme 1.4.0, MyST-NB 1.4.0, sphinxcontrib-mermaid 2.1.1 and sphinx-thebe 0.3.1. It does not install the research project's dependencies or modify `pyproject.toml` or `uv.lock`. The first build may need Internet access to download the documentation tools. On later builds uv reuses its cache.

The script stages the content, performs a fresh Sphinx HTML build with warnings treated as errors, and checks generated local links, anchors and assets. The output is:

```text
site/_build/html/index.html
```

For staging without building, use `python .\site\build.py --stage-only`. To repeat just the generated HTML link check, use `python .\site\check_links.py`.

## Preview locally

From the repository root:

```powershell
python -m http.server 8000 --bind 127.0.0.1 --directory site/_build/html
```

Open <http://127.0.0.1:8000/>. Use HTTP for search and other browser scripts rather than opening HTML through `file://`. Stop the server with Ctrl+C. If port 8000 is already occupied, choose another port and use its corresponding URL.

After changing documentation or configuration, rerun `python .\site\build.py` and refresh the browser. The build always restages the current content.

## Content and navigation

Original Markdown remains the source of truth. The home page is concise; `docs/about.md` contains the merged background, audience and learning goals. The current programme and venue are in `docs/agenda.md` and agree with Home, About and Participation.

The sidebar order is **Getting Started**, **About the Session**, **Tutorials**. Tutorials contains the overview plus expandable Cancer and Cardiac groups. Each track has one combined Getting Started page. Home is the first entry and is linked from the logo. There are no separate Introduction, Overview, Resources or notebook-overview sidebar pages.

- `conf.py`: theme, notebook parser, execution prohibition, existing lexer alias, notebook access header and redirects.
- `navigation.json`: ordered top-level sidebar sections.
- `_static/mdas-logo.png` and `_static/mdas.css`: the supplied logo and existing styling, unchanged.
- `_templates/redirect.html`: redirects old Overview, Resources, notebook overview and tutorial Introduction URLs to their current destinations.
- `build.py`: stages sources, updates links and appends navigation without manually maintained content copies.
- `check_links.py`: checks generated local HTML links, fragment identifiers and assets; it does not test remote execution services.

The ignored `site/_staged/` directory is regenerated on every build. It preserves source directory structure, maps the root README to `index.md`, and adds two small track navigation landing pages. Obsolete source pages remain in the repository but are excluded from Sphinx's document tree and search index. Internal links are mapped to consolidated pages, with HTML redirects for old URLs. Previous/next links follow the current toctree order.

### Notebook rendering

The original `notebooks/MDAS/cancer/cancer_live_coding.ipynb` is copied byte-for-byte into the staged tree and parsed by MyST-NB. **Execution is disabled** with `nb_execution_mode = "off"` and an all-notebook exclusion pattern. Saved code and outputs are shown; no research environment or dataset is loaded.

A source-read hook adds the page title, GitHub and prominent Colab links, setup guidance and privacy warnings in memory. Existing notebook headings are nested beneath the page title for navigation. It leaves code, outputs and safety text unchanged. The original notebook and associated Python helper are never written or executed. Its existing Mermaid diagram is rendered using the Mermaid extension. A legacy `ipython2` display-lexer alias is registered without changing notebook metadata on disk.

The Colab button opens the original notebook from GitHub. A compatible Colab environment and companion-module setup remain follow-up work; the current interactive option is Thebe/Binder. No Cardiac notebook is staged because none is currently present.

## Optional Thebe and Binder execution

`sphinx-thebe 0.3.1` is the Sphinx/MyST-NB integration selected for this stack. Its dependency resolution and the actual Sphinx 9.2 build succeeded without upgrading the existing documentation tools. It uses the versioned Thebe 0.8.2 browser bundle from the upstream extension. This verifies build compatibility, not a working remote research environment.

`conf.py` enables the extension and supplies the repository, revision, selectors and backend settings. `_ext/mdas_interactive.py` scopes its assets/configuration to the Cancer notebook and replaces the staged URL-based kernel directory with the real repository directory, `notebooks/MDAS/cancer/`. Inputs use `.cell_input pre` within `.cell`, and saved outputs use `.cell_output`. Other documentation pages keep their original navigation and do not load these scripts.

The visible launch control calls the upstream lazy loader only on a participant click. `bootstrap: false` prevents automatic activation, no `thebe-init` tags are added, and no notebook cells are executed automatically. `_static/mdas-interactive.js` displays genuine connection statuses and CDN/connection failures in a live region. The underlying Thebe editors/run buttons handle cell editing and execution. Saved output is retained using `predefinedOutput: true`; it is replaced when a participant executes the associated cell. Session-credential caching is disabled.

The original static page, GitHub link and Colab link remain available if an online service fails. The new [execution guide](../docs/notebook-execution.md) provides the participant setup steps. The original notebook, helper and scientific logic remain unchanged.

### Binder configuration and constraints

The standard `.binder/runtime.txt` and `.binder/requirements.txt` select Python 3.12 and a pinned Linux x86-64 CPU-only dependency graph. `.binder/requirements.in` is its editable input. The Cancer library uses the commit already present in the research lockfile; CPU Torch/Torchvision avoid downloading CUDA runtimes. Only core dependencies are installed, without optional research extras. See [.binder/README.md](../.binder/README.md) for the regeneration command and validation status.

The default backend is `https://mybinder.org`, repository `pykale/mmai-mdas`, revision `main`. Binder obtains code from that GitHub revision, **not the local checkout**. These local environment files cannot be used by the public backend until reviewed and pushed; this task does not push or deploy them. Do not tell participants this environment is verified before that remote test.

### Diagnosed failed launch and local repair

The failure was reproduced using the public BinderHub event-stream API, independently of the browser. The public repository exists, is public, and `main` resolved to `ed163a322186055c8c5b79885288ad9a051f89c4`. The service redirected to `2i2c.mybinder.org`, cloned that revision, then logged **No environment specification found** and emitted `phase: failed`. Package installation, Jupyter server launch and kernel connection were not reached. This is not evidence of a PyTorch installation failure, a wrong kernel directory or a WebSocket/CORS error.

The public tree contains the original notebook/helper and the root `pyproject.toml`, `uv.lock` and `.python-version`, but **no Binder runtime definitions**. The serving Binder builder did not find a usable environment specification there. The local `.binder/` files are not part of that public revision. Changing a local Python environment or rebuilding the HTML cannot publish them to Binder.

The repaired launch control performs a click-time, unauthenticated public GitHub tree check for the two runtime definitions and the notebook/helper. Missing files stop the known-bad launch with an actionable message. API/network/rate-limit errors are reported separately. When files exist, the client replaces the moving ref with the exact checked commit before invoking Thebe. Later backend status messages are retained in the page status, and a direct Binder build-log link is available. No credentials are requested or stored, and no launch happens just by reading the page. Browser end-to-end verification remains outstanding; the new controller behaviour has automated tests.

For a repeatable diagnosis from the repository root:

```powershell
python site/diagnose_binder.py
```

This compares local/public files without starting Binder. To explicitly observe one bounded public launch, add `--launch`. Use `--ref <branch-tag-or-commit>` or the existing `MDAS_BINDER_REF` environment setting to check another reviewed revision. The report is saved to ignored `site/_build/binder-diagnostic.json`; server URLs/tokens from ready events are not recorded. The public launch endpoint performs a real build/launch request, so use that option deliberately.

**Files needed on the public Binder revision, after organiser approval:**

1. `.binder/runtime.txt`: tells Binder to use Python 3.12.
2. `.binder/requirements.txt`: installs the pinned CPU-only ML/kernel environment and pinned Cancer code.
3. `.binder/requirements.in` and `.binder/README.md`: preserve the reviewed dependency inputs and regeneration/validation instructions (recommended alongside the two runtime files).

The notebook and `synthetic_data_generation.py` already exist publicly and are unchanged. Neither generated HTML nor synthetic/private datasets must be published to fix environment discovery. The Sphinx configuration/scripts must eventually be included when publishing the website, but they are not required for Binder to recognise its runtime definitions.

After those files are present on the selected ref, repeat the launch diagnostics. Only then can image build, actual imports, working directory, synthetic-data generation and kernel execution be validated. Dependency resolution succeeded locally, but that does not prove that Binder can build the full environment or that training fits its resource limits. No publication or remote-settings changes were performed by this repair.

The kernel starts next to `synthetic_data_generation.py`. The original relative data path resolves to repository-local `data/synthetic_data`; the helper generates synthetic data only when its cell is run. The default cohort generated approximately 1.76 MB of files in a local smoke test. Model imports, 40-epoch training, a second baseline fit and bootstrap intervals add memory and CPU cost. The complete notebook has not been benchmarked on Binder.

Public Binder is temporary, has limited capacity and no availability guarantee. Its published memory allowance is at least 1 GB and at most 2 GB, with idle-session culling and CPU/session limits. Download edits/results you need to retain. The CPU-only environment may still take several minutes to build or import. Never use confidential or patient data. See the [Binder usage guidelines](https://mybinder.readthedocs.io/en/latest/about/user-guidelines.html) for current limits.

### Test locally and record the layers separately

Build and serve using the commands above, then open the Cancer Live-Coding Notebook page:

1. Before clicking, confirm the static cells and saved outputs are visible and that no Binder connection is started.
2. Click **Run interactively on this website**. Confirm loading/status text, editable cells and eventual kernel connection. A connected kernel does not prove that research imports work.
3. Edit a code cell temporarily to `print(1 + 1)` and execute it. Restore/reload afterwards; do not change the source notebook.
4. In the first cell, test `import torch` and the companion import. Check the working directory with `from pathlib import Path; print(Path.cwd())`.
5. Run only the synthetic-data setup initially. Check the expected CSV and patch files; avoid launching training until basic tests pass.
6. Test training and advanced cells separately while measuring time and memory before approving the participant environment.

The dependency resolution, helper smoke test, static builds, HTML links and controller behaviour have been checked locally. `node --test site/tests/interactive.test.cjs` exercises launch/error handling using mocks; it **does not** establish browser or remote-kernel success. Docker was unavailable locally, and the new Binder files are not yet on the configured remote revision. Browser-to-Binder execution and the full ML environment are therefore unverified.

The organiser has confirmed Binder server launch and Thebe kernel connection after publishing revision `090f1ff`. The earlier failure analysis above records the pre-publication state. Full research-training validation remains separate.

The Colab button targets the original `notebooks/MDAS/cancer/cancer_live_coding.ipynb`. Colab environment preparation is deferred; no separate Colab-ready notebook or setup instructions are included in this version. The original notebook remains the only rendered notebook/sidebar entry.

### Disable or replace the backend

To build entirely without Thebe controls or assets in PowerShell:

```powershell
$env:MDAS_ENABLE_THEBE = "0"
python site/build.py
Remove-Item Env:MDAS_ENABLE_THEBE
```

The notebook, saved outputs, Colab and GitHub links still render. To re-enable Thebe, rebuild after removing that environment variable. Disabling Thebe does not require a live Binder service or any changes to the notebook.

To select another compatible BinderHub or a reviewed repository revision, set `MDAS_BINDER_URL` and/or `MDAS_BINDER_REF` before building. For an independently managed Jupyter server, adapt the supported Thebe `kernelOptions.serverSettings` in `_ext/mdas_interactive.py` and remove `binderOptions`; configure CORS/WebSocket access for the documentation origin. Do not embed persistent tokens or credentials in version-controlled configuration or generated public HTML. A self-hosted authenticated backend needs its own reviewed authentication design.

All content remains ordinary Markdown and notebook files; environment specifications are standard repo2docker/pip files. The generated website stays static and can be hosted independently. Thebe is optional; Binder is an initial backend, not a requirement for reading or building the documentation. References: [sphinx-thebe configuration](https://sphinx-thebe.readthedocs.io/en/latest/configure.html), [Thebe options](https://thebe.readthedocs.io/en/stable/config_reference.html), and [repo2docker configuration](https://repo2docker.readthedocs.io/en/latest/configuration/).

### Repository compatibility

The Cancer and Cardiac public `main` trees were inspected on 26 October 2026. Both contain the documented quickstarts and example paths, including the optional lead comparison. The current Cancer quickstart documents `uv sync --all-extras`; the Cardiac quickstart documents the editable install and both quick configurations. These checks support linking to the public code, but are not execution tests of the research environments. No command currently requires a documented non-default revision.

## GitHub Pages preparation

The configured destination is <https://pykale.github.io/mmai-mdas/>. No publication is performed by the build script. Generated HTML contains relative links suitable for that project subpath, and Sphinx's GitHub Pages extension creates `.nojekyll` so underscore-prefixed theme assets can be served.

`github-pages.yml.example` is an **inactive template outside `.github/workflows/`**. It cannot run in its current location. It uses only a manual `workflow_dispatch` trigger. After review, a repository maintainer could:

1. Add the template as `.github/workflows/docs-pages.yml`, then commit and push the approved source changes.
2. In repository **Settings → Pages → Build and deployment**, select **GitHub Actions** as the publishing source. Administrative or maintainer access is required to configure the source; organisation policy must permit Pages and the referenced Actions.
3. Permit the workflow token to read repository contents, write Pages deployments (`pages: write`) and request an OpenID Connect token (`id-token: write`). Review any protection rules for the `github-pages` environment.
4. Manually run the workflow on the intended branch. The upload step includes only `site/_build/html`, not notebooks, source material, datasets or the repository checkout.

The workflow and repository settings have not been activated, changed or run. The site is not published by this local work.

For publishing details, see GitHub's [custom Pages workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) and [publishing-source settings](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).
