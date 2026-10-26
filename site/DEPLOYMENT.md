# First GitHub Pages deployment

Destination: https://pykale.github.io/mmai-mdas/ (repository `pykale/mmai-mdas`, branch `main`).

## What the workflow does

`.github/workflows/deploy-docs.yml` runs on pushes to `main` and manual dispatch. Checkout, Python 3.12 and pinned uv 0.13.5 precede the existing `python site/build.py` process. That process installs the exact documentation packages from `site/requirements.txt` in an isolated uv tool environment, builds Sphinx with warnings as errors and checks generated links. It does not install `pyproject.toml`, `uv.lock`, `.binder/requirements.txt`, Torch or Cancer. MyST-NB execution stays disabled; no training, Binder launch or patient-data access happens during build.

The build uploads only `site/_build/html` using `actions/upload-pages-artifact@v4`. The dependent deploy job uses `actions/deploy-pages@v4`, with `pages: write`, `id-token: write` and the `github-pages` environment. The build job has `contents: read` and `pages: read` so `configure-pages` can read the Pages site metadata. The deploy job has the write/OIDC permissions above. One Pages concurrency group serializes runs without cancelling a deployment in progress. Only `main` can deploy, including manually dispatched runs.

**Pushing this workflow to main can deploy automatically once Pages is configured.** Preparation itself does not publish anything. Keep review complete before running the commit/push commands below.

## Source inventory

All existing documentation, original notebook/helper, static branding, navigation, Sphinx configuration and Binder files are already tracked in the current checkout. This is the complete relevant source inventory to retain on `main`; the runtime Binder files are independent of the website build:

```text
.binder/README.md
.binder/requirements.in
.binder/requirements.txt
.binder/runtime.txt
.github/workflows/deploy-docs.yml
.gitignore
README.md
assets/.gitkeep
docs/about.md
docs/agenda.md
docs/notebook-execution.md
docs/overview.md
docs/participation.md
docs/prerequisites.md
docs/quick-start.md
docs/resources.md
notebooks/MDAS/cancer/cancer_live_coding.ipynb
notebooks/MDAS/cancer/synthetic_data_generation.py
notebooks/MDAS/cardiac/.gitkeep
notebooks/README.md
site/DEPLOYMENT.md
site/README.md
site/_ext/mdas_interactive.py
site/_static/mdas-interactive.css
site/_static/mdas-interactive.js
site/_static/mdas-logo.png
site/_static/mdas.css
site/_templates/redirect.html
site/build.py
site/check_links.py
site/conf.py
site/diagnose_binder.py
site/github-pages.yml.example
site/navigation.json
site/requirements.txt
site/tests/interactive.test.cjs
tutorials/README.md
tutorials/kalecancer/README.md
tutorials/kalecancer/getting-started.md
tutorials/kalecancer/hands-on.md
tutorials/kalecancer/results.md
tutorials/kalecardiac/README.md
tutorials/kalecardiac/cardiovae-hands-on.md
tutorials/kalecardiac/getting-started.md
tutorials/kalecardiac/lsemvae-hands-on.md
tutorials/kalecardiac/results.md
```

Do not add generated `site/_build/`, `site/_staged/`, `data/`, caches, virtual environments, `.env`, credentials, `tmp/` or `source-material/`. The ignore rules already exclude these, and none were found in the tracked-file inventory. Only generated HTML is uploaded as the Pages artifact, not the repository checkout. The PDF stays local.

## Review and publish from PowerShell

These commands are provided for the organiser; they were not executed during preparation. At the end of this task the original website sources were already tracked and unchanged. Stage only the five deployment-related paths:

```powershell
cd "C:\Users\Mohammad Javad\Downloads\mmai-mdas"
git branch --show-current
git status --short
python site/build.py
node --test site/tests/interactive.test.cjs
git diff --check
git add -- .github/workflows/deploy-docs.yml site/check_links.py site/README.md site/DEPLOYMENT.md site/github-pages.yml.example
git diff --cached --name-status
git diff --cached --stat
git diff --cached --check
git diff --cached
```

Confirm the branch is `main`, the staged list contains only the five paths above, and no unrelated changes are staged. If anything unexpected is already staged, review it before continuing. Do not use `git add .` or force-add ignored files.

After approving the staged result and configuring Pages:

```powershell
git commit -m "Prepare Sphinx documentation deployment to GitHub Pages"
git push origin main
```

Then monitor **Actions > Publish MDAS documentation**. Alternatively, once the workflow exists remotely, choose **Run workflow**, branch **main**. Do not create a second Pages workflow or a `gh-pages` branch for this approach.

## Manual GitHub settings

1. In repository **Settings > Pages > Build and deployment**, select **Source: GitHub Actions**. Do not select Deploy from a branch. No custom domain is needed.
2. Under **Settings > Actions > General**, ensure the organisation/repository policy permits the referenced GitHub and Astral actions. The workflow declares its required token permissions; a blanket read/write default is not necessary. No personal access token or deployment secret is required.
3. If the `github-pages` environment already has branch restrictions or approval rules, permit `main` and approve deployment if those rules require it. Review any organisation-level Pages restrictions with an administrator.
4. After a successful run, verify the published URL from the deployment job. Test logo/navigation, search, notebook saved outputs and an intentional Thebe connection from the public origin.

Official reference: [GitHub Pages custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

## Validation and remaining issues

- Sphinx build passed with warnings treated as errors: 25 HTML pages, 1,174 local HTML/CSS links/assets, zero errors.
- Link resolution checked under `https://pykale.github.io/mmai-mdas/`; a temporary local HTTP prefix test served 47 page/asset URLs successfully, including search assets. Search runtime behaviour and responsive layout have not been retested in a browser during this deployment preparation.
- Book Theme, CSS, logo, navigation, original notebook, code and saved outputs were preserved. The staged notebook matches the original bytes. Six controller tests passed.
- Thebe remains configured for `pykale/mmai-mdas`, `main`, `https://mybinder.org`, kernel directory `notebooks/MDAS/cancer`. The existing click-time check pins the actual public revision before launch. Working kernel connection was previously confirmed by the organiser; no new remote launch was required for deployment preparation.
- Colab continues to open the original public `cancer_live_coding.ipynb`. At the organiser's explicit clarification, Colab-ready work remains deferred: `cancer_live_coding_colab.ipynb` was previously deleted and is not part of this release. The missing temporary constraints-file issue is therefore not fixed or claimed tested here. The original Colab notebook still needs environment/helper setup for execution.
- The Actions workflow has not run on GitHub, and no public Pages deployment or public-origin Binder connection was tested. Local checks do not establish either. No commit, push, deployment or remote-setting change was performed.

## Configure Pages 404 follow-up

The first remote run failed before Sphinx at the Pages metadata API. The build job initially lacked an explicit `pages: read` permission; this has now been added. A 404 can also mean Pages is not enabled. Confirm Settings > Pages > Source is GitHub Actions before retrying. Commit/push this fix and inspect the new run rather than rerunning an older commit, which retains the old permissions. No remote setting or publication was changed by this local correction.
