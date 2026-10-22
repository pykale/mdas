# Migration checklist

Migration source: local `source-material/MDAS_GitBook_pdf_Export.pdf`, 30 pages, exported 22 October 2026. The PDF remains local and is ignored by Git. This checklist records migration status, not confirmation that the software examples execute.

## Successfully migrated content

- [x] Read and extracted all 30 pages; reviewed rendered contact sheets of every page and full-size selected pages for commands, tables and links.
- [x] Preserved substantive explanations, activity prompts, technical references, commands, warnings and scientific meaning.
- [x] Created all 20 expected Markdown pages, the `.gitignore`, and the three `.gitkeep` files in the requested structure.
- [x] Preserved the exact eight agenda rows, their proposed timings and activity wording; kept draft status and organizer-confirmation warnings.
- [x] Kept `cancer-refactor` and `cardiac-main` setup requirements and commands distinct.
- [x] Replaced outdated event references to â€œworkshopâ€ with â€œsessionâ€; retained code identifiers, paths and third-party names.
- [x] Preserved the distinctions between synthetic demonstrations, research datasets and clinically validated results. No results or scores were invented.
- [x] Converted GitBook navigation into relative links to the actual Markdown files. Replaced obsolete PDF-local `/3241678/tutorials/...` links with the appropriate tutorial setup pages.
- [x] Recovered the PyKale, KaleCancer, KaleCardiac, PyKale discussions and uv URLs from PDF annotations. Verified the three public repository pages and discussions page on 22 October 2026. No default-branch compatibility claim is made.
- [x] Added the main README navigation, audience, objectives, draft date/location, track descriptions and DeepWiki context.
- [x] Prepared notebook folders without generating any `.ipynb` files or Colab links.

## Source-to-page coverage

| PDF pages | Source content | Migrated destination |
| --- | --- | --- |
| 1 | Untitled cover, no substantive content | Replaced by the [main README](README.md) entry point |
| 2â€“3 | Quick Start and snapshot warning | [Quick Start](docs/quick-start.md); reused for [KaleCardiac setup](tutorials/kalecardiac/getting-started.md) |
| 4â€“5 | Overview, audience, navigation, synthetic-data warning | [Overview](docs/overview.md) |
| 6â€“7 | What is MDAS divider; purpose and proposed format | [About](docs/about.md) |
| 8â€“9 | Activity loop, own-data guidance and questions | [Participation](docs/participation.md) |
| 10â€“11 | Draft agenda, learning goals and proposed logistics | [Agenda](docs/agenda.md) |
| 12 | Before attending, software paths and warnings | [Prerequisites](docs/prerequisites.md) |
| 13â€“14 | Tutorials divider and overview | [Tutorials overview](tutorials/README.md) |
| 15â€“16 | KaleCancer divider and introduction | [KaleCancer](tutorials/kalecancer/README.md) |
| 17 | Refactor setup, synthetic example and notebook reference | [Cancer getting started](tutorials/kalecancer/getting-started.md) |
| 18â€“19 | Proposed exercise and HANCOCK advanced reading | [Cancer hands-on](tutorials/kalecancer/hands-on.md) |
| 20 | Survival results, concordance and next steps | [Cancer results](tutorials/kalecancer/results.md) |
| 21â€“22 | KaleCardiac divider, examples table and development warning | [KaleCardiac](tutorials/kalecardiac/README.md) |
| 23â€“24 | LS-EMVAE exercise and optional lead-set comparison | [LS-EMVAE hands-on](tutorials/kalecardiac/lsemvae-hands-on.md) |
| 25â€“26 | CardioVAE exercise and proposed prompts | [CardioVAE hands-on](tutorials/kalecardiac/cardiovae-hands-on.md) |
| 27â€“28 | Cardiac output artifacts, interpretation and reflection | [Cardiac results](tutorials/kalecardiac/results.md) |
| 29â€“30 | Resources divider, repositories, references and status | [Resources](docs/resources.md) |

Print headers, timestamps, footers, page numbers and duplicated headings caused by page breaks were removed. Empty section-divider pages were merged into their substantive sections; no scientific content was removed.

## Missing materials, images and uncertain links

- [ ] Obtain the actual KaleCancer and KaleCardiac notebooks. The PDF references `examples/synthetic/synthetic_survival.ipynb` inside the cancer snapshot, but that file was not supplied. No cardiac notebook file path is given. See [notebook availability](notebooks/README.md).
- [ ] Obtain or identify the exact `cancer-refactor` and `cardiac-main` archives/revisions. Only the PDF was supplied; archive content was not independently inspected. The cardiac snapshot is described as having September 2026 metadata, without a commit hash.
- [ ] Confirm participant access to these exact software revisions. Public repository URLs do not identify the original snapshots; no guessed download, archive or branch links were added.
- [x] No embedded raster images were present on any of the 30 pages. Rendered review found no scientific figures or diagrams needing recovery. Tables, numbered steps and warning boxes were converted to Markdown; decorative interface icons were not extracted. `assets/` is ready for future real assets.
- [x] No important visual is known to be missing. No unresolved external URL was substituted with a guessed URL. Installation-guidance URLs absent from the PDF were not invented; uv's URL was recovered directly.
- [ ] Provide working GitHub and, where compatible, Colab links after real notebooks are added and verified.

## Commands requiring testing

All commands below are transcribed from the PDF. They were checked against its text and rendered command blocks, but **not executed**. Run them in the appropriate extracted software repository, not this documentation repository.

| Snapshot | Command or check | Status |
| --- | --- | --- |
| `cancer-refactor` | `uv sync --all-extras` | Requires clean-environment testing with Python 3.11 or 3.12 |
| `cancer-refactor` | `uv run python examples/synthetic/synthetic_survival.py` | Verify CPU/no-download behavior, printed metrics and outputs |
| `cardiac-main` | `pip install -e .` | Install compatible PyTorch and PyKale first; test Python 3.10â€“3.12 environments intended for participants |
| `cardiac-main` | `python -c "import kalecardiac, torch, kale; print(kalecardiac.__version__)"` | Verify imports and version against the intended snapshot |
| `cardiac-main` | `python -m examples.cardiovae_multimodal.main --cfg examples/cardiovae_multimodal/configs/quick.yaml` | Verify synthetic generation, endpoint, CPU behavior and saved artifacts |
| `cardiac-main` | `python -m examples.lsemvae_ecg.main --cfg examples/lsemvae_ecg/configs/quick.yaml` | Verify synthetic generation, lead settings, stages and saved artifacts |
| `cardiac-main` | `python -m examples.lsemvae_ecg.main --leads I,I+II,I+II+III` | Optional; requires facilitator validation before session day |

PDF display wraps in the cardiac `--cfg` commands and the Python `-c` command were joined into single logical command lines, without changing tokens or argument values. The split imaging-extra token was restored to `.[imaging]`. No commands, APIs or package installation steps were added beyond the source. Optional extras are documented as source tokens, not expanded into unverified installation recipes.

## Details requiring organizer confirmation

- [ ] Confirm Wednesday 18 November 2026, 1â€“5 PM, Regent Court, and any room/access details absent from the PDF.
- [ ] Confirm the proposed 6 November application deadline, notification by 10 November and optional 11 November briefing; no application URL was supplied.
- [ ] Approve the draft timetable and proposed facilitator exercises.
- [ ] Resolve the planning discrepancy: the agenda says organizer-provided datasets/problems are available, while the participation guide says availability and support are not yet confirmed. The agenda wording is preserved exactly and the uncertainty is highlighted.
- [ ] Confirm AIRE/facilitator support, final cardiac exercise selection and session-day support arrangements.
- [ ] Confirm suitable datasets, permissions, secure infrastructure, compute and expected local directory structure before real-data use, including HANCOCK access.
- [ ] Decide how to distribute the exact source snapshots and notebooks to participants.

## Quality checks

Validation on 22 October 2026: 20 expected Markdown files, 122 working relative links, five structurally consistent tables, seven unique commands matched to source text, and eight agenda rows matched to PDF page 10. All code fences are paired. The source PDF contains 30 pages.

- [x] Expected Markdown pages and marker files exist.
- [x] Relative Markdown links resolve to existing local files or directories.
- [x] Code fences are paired and Markdown tables have consistent column counts.
- [x] Source-to-page audit accounts for every PDF page and all substantive sections.
- [x] Agenda times and activity text match PDF page 10, including both block rows.
- [x] All seven unique source commands are retained, allowing only PDF display-wrap normalization.
- [x] Main README links to every major section and to the migration checklist.
- [x] Notebook directories and `.gitkeep` files exist and are not ignored; the two notebook marker files are staged for Git tracking without a commit.
- [x] `source-material/` and temporary extraction/rendering tools and files are ignored. Legitimate tutorial `.ipynb` files are not ignored; notebook checkpoints, Python caches, local environments, secrets and generated outputs are ignored.
- [x] No identifiable patient data, confidential datasets, invented notebooks, generated scientific results, website configuration or deployment workflow were added.
- [x] No commit, push, deployment or external repository modification was performed.

## Recommended next steps before publishing

1. Review this migration against the PDF and confirm draft logistics and support arrangements.
2. Identify exact software revisions, distribute them through an approved route and test the commands in clean participant environments.
3. Supply and review the real notebooks, confirm dependencies/data requirements, and add working GitHub/Colab links where appropriate.
4. Review permissions for any future assets or datasets; keep identifiable/confidential data and the source PDF out of Git.
5. Review and stage the intended Markdown files locally. After organizer approval, commit and push, then request DeepWiki indexing. No GitHub Pages, MkDocs, Jupyter Book or Docusaurus project is needed.

