# MDAS 1.0 website review

Prepared locally on 3 November 2026. No commit, push, publication or remote configuration change was performed.

## Learning journey

The site now frames this edition as **MDAS 1.0**, organised by PyKale for Cancer and Cardiac research, with materials usable both during the workshop and independently afterwards.

**Discover > Prepare > Explore > Run > Interpret > Continue** is a reusable, non-interactive stage indicator. It identifies the current stage without adding another menu or client-side state. The homepage gives two balanced track entry cards. Participation explains preparation/privacy; Quick Start keeps the executable commands; Cancer Getting Started explains both tasks; the notebook has one interpretation next step; Results distinguishes the metrics and provides one responsible research continuation.

Cancer explanations were derived from the current original notebooks, not inferred from a generic survival tutorial. Classification predicts early/late labels using age, gender and patch features; it reports AUROC for the late class and balanced accuracy. Survival uses age, stage and gender with patches, predicts log hazard and reports Harrell's C and Uno's C at `tau=1825.0`. The baseline bootstrap comparison uses AUROC for Classification and Harrell's C for Survival. No numerical performance claims are added.

The Regent Court / possible Diamond Workroom 3 (Room 205) venue information, event date and 13:00-17:00 programme are preserved. Agenda activity rows and its pending final-30-minute note are unchanged; only its redundant footer navigation is simplified.

## Navigation before and after

Before:

```text
Getting Started
  Prerequisites
  Quick Start
About the Session
  What is MDAS?
  Session Agenda
  Participation Guide
Tutorials
  Tutorials Overview
  Cancer
    Getting Started
    Hands-on Tutorial
    Live-Coding Notebook
    Results and Interpretation
  Cardiac
    Getting Started
    CardioVAE Hands-on
    LS-EMVAE Hands-on
    Results and Interpretation
```

After:

```text
Getting Started
  Quick Start
About the Session
  What is MDAS?
  Session Agenda
  Participation Guide
Tutorials
  Cancer
    Getting Started
    Live-Coding Notebook
    Results and Interpretation
  Cardiac
    Getting Started
    CardioVAE Hands-on
    LS-EMVAE Hands-on
    Results and Interpretation
```

`navigation.json` supplies the main groups and `build.py` supplies track toctrees; both are updated. Existing Previous/Next navigation remains, including the Survival page's canonical Cancer relations.

## Consolidated pages and redirects

| Previous public URL | New destination | Preserved content |
| --- | --- | --- |
| `docs/prerequisites.html` | `docs/participation.html` | Audience, Python background, laptop/environment choice, separate track environments and privacy |
| `tutorials/README.html` | `index.html#choose-a-research-track` | The two research-track entry points and synthetic-data context |
| `tutorials/kalecancer/hands-on.html` | `tutorials/kalecancer/live-coding.html` | Observe modalities/endpoint/metrics, follow the pipeline, subject-level separation and censoring questions; advanced HANCOCK scope moves into Cancer Results |

The original Markdown files remain in the repository. They are excluded from the Sphinx source/search tree; their HTML URLs become lightweight noindex redirects. Internal links are rewritten directly to consolidated destinations. Cardiac Hands-on pages and source content remain untouched.

## Notebook controls and saving

The page retains its Classification/Survival selector and exactly two blue/white primary execution actions. Binder still uses the original selected notebook, real kernel directory and existing controller; Colab still opens the selected `_colab.ipynb`. Scientific cells and saved output rendering are retained.

The edited-notebook download button, embedded export payload, export function, blank exercise link and repeated help/runtime/source action links are removed from the injected interface. The blank files themselves remain unchanged. A secondary **Execution Help** control sits above the title at the article's upper right, with a help icon, keyboard focus style, touch-sized target and explicit new-tab label. It opens the existing execution guide in another tab so the current DOM/kernel can stay in place. It is not hidden by presentation CSS.

The selector confirmation, same-page no-op, history restoration and `beforeunload` protection remain. Warnings now instruct users to copy code edits/results rather than refer to the removed export function. Execution Help explains that warnings do not save work, that website Binder has no general file-download interface, and that Colab's File menu/Files pane or a local environment can retain work and files.

The guides cover startup delays, connection failures and recovery, cell order, switching, temporary sessions, Python 3.12 selection, setup/restart instructions, and `MDAS ready` with Hub 1.33.0. They do not claim automatic runtime selection or guaranteed execution. The existing local Hub correction in the Colab guide was retained.

## Reusable components

- `site/_ext/mdas_journey.py`: static stage mapping/renderer and source-read adaptation. Cardiac pages receive the indicator in memory without editing their Markdown files.
- `.mdas-track-cards` / `.mdas-track-card`: a two-column homepage grid that becomes one column on smaller screens, using the existing logo, colours and theme.
- `.mdas-notebook-tools` / `.mdas-execution-help`: an article-level secondary help control independent of Binder and presentation scripts.

No new dependencies, animation system, future-edition routes or publishing infrastructure are introduced. The Present/fullscreen JavaScript and existing presentation layout rules are unchanged.

## Changed-file inventory

Content:

- `README.md`
- `docs/about.md`
- `docs/participation.md`
- `docs/quick-start.md`
- `docs/agenda.md` (footer only)
- `docs/notebook-execution.md`
- `docs/colab.md`
- `tutorials/kalecancer/getting-started.md`
- `tutorials/kalecancer/results.md`

Navigation, rendering and styling:

- `site/navigation.json`
- `site/build.py`
- `site/conf.py`
- `site/_ext/mdas_journey.py` (new)
- `site/_static/mdas.css`
- `site/_static/mdas-notebooks.css`
- `site/_static/mdas-notebooks.js`

Tests and maintenance:

- `site/tests/notebooks.test.cjs`
- `site/tests/test_notebooks.py`
- `site/tests/test_learning_journey.py` (new)
- `site/README.md`
- `site/MDAS-1.0-REVIEW.md` (this report, new)

There were pre-existing local changes in `docs/colab.md` and `site/tests/test_colab.py` when work began. The Colab guide changes were retained while adding website help; `site/tests/test_colab.py` was not edited by this redesign. It will still appear in the working-tree diff because of that earlier change.

## Validation

Completed checks:

- Strict fresh Sphinx build (`-n -W -E -a`) passed.
- Generated link checker: **27 HTML pages, 1,178 local links/assets, zero errors**.
- **6 learning-journey tests**, generated notebook HTML/mapping/ToC/help tests, **9 existing Colab setup/preservation tests**, and **17 JavaScript tests** passed.
- JavaScript tests cover both switching directions, cancellation, selecting the current notebook, history restoration, unload warnings, lazy Binder startup/error paths and unchanged fullscreen/presentation behaviour. Export tests were replaced with a regression asserting that the removed export controller is absent while switching guards remain.
- Setup command blocks and Agenda programme/event information match the prior source exactly. Notebook and Colab setup files are not rewritten or regenerated.
- All 21 files in the initial protected-file SHA-256 snapshot were verified unchanged, including all six Cancer notebooks, both Colab support files, Binder configuration/controller, logo, Present JavaScript and all Cardiac tutorial sources.

A clean `git archive HEAD` snapshot with all current review changes overlaid passed the strict Sphinx build and all website tests. The enabled build checked **1,178** links/assets; the disabled build checked **1,170**; both had 27 HTML pages and zero errors. The disabled build retained the selector, Colab route and Execution Help while omitting Binder launch/configuration. `git diff --check` passed. This is a clean source snapshot, not a newly cloned or published repository.

## Limits and manual review

Browser inventory reported no usable browser/native surface: browser access host and native pipe were unavailable. Actual desktop/mobile appearance, keyboard focus traversal, native leave prompts and fullscreen visual placement therefore remain unverified. Generated markup, responsive CSS and behaviour tests are evidence for those implementations, not a claim of a visual browser pass.

No live Binder kernel or Colab session was launched for this content-only redesign. Its runtime code, notebooks and dependency pins are unchanged; static destination checks and controller regressions passed. No scientific execution retest was needed or claimed.

Before publication, inspect the home cards and stage indicator in light/dark modes and mobile width; launch each selected notebook route; open Execution Help with keyboard and in presentation mode; cancel an active-session switch; verify copy/save guidance and Previous/Next links. Review the two task explanations against the unchanged notebooks. Publish only after review.
