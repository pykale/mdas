# Participant navigation and presentation review

## Final tutorial sidebar

```text
Cancer
  KaleCancer Classification
  KaleCancer Survival Analysis
Cardiac
  KaleCardiac CardioVAE
  KaleCardiac LS-EMVAE
```

Both parent entries open authored overview pages. All four example URLs retain their existing `live-coding` paths, but visible headings, sidebar labels and help copy use example titles. Each notebook is in its own track's toctree: no orphan/secondary navigation override or picker remains. Normal Sphinx relations supply previous/next navigation. Binder remains lazy; the existing active-session flag protects all leave paths even without a selector. Present mode code is unchanged.

## Content and compatibility

- Home presents KaleCancer and KaleCardiac in parallel and points to online notebook actions or Quick Start for Run locally.
- Quick Start uses Run online / Run locally for both tracks, direct links to all four pages, repository-specific commands and shared local Python 3.11/3.12 guidance. Current upstream KaleCancer and KaleCardiac project metadata were checked. Cancer's Colab runtime selection stays separate from local guidance.
- About has two compact tables for fusion timing and analysis questions; learning goals, organiser credit and session details remain.
- Participation has one Quick Start link in place of duplicated setup guidance, while audience, participation and privacy guidance remain.
- Cancer overview avoids architecture dimensions and detailed metrics. Cardiac overview consolidates the useful tutorial introduction, data, setup and workflow context; its authored source can accept a future diagram without changing the builder, and displays no empty placeholder.
- Concise interpretation/safety guidance accompanies each example. The retired Cancer Results page no longer repeats outdated notebook details.
- Cardiac Getting Started redirects to its overview. Cancer and Cardiac Results URLs redirect to interpretation guidance on an example. Old Cardiac section anchors are retained where useful. Cancer Results survival fragments select the Survival example. Redirects have static links/meta refresh and a fragment-preserving JavaScript enhancement.
- Heading permalink icons remain disabled; no shared Sphinx label is added. The old page-local `#live-coding-notebook` anchors remain for external links, without visible old headings.

## Workflow figure

`assets/kalecancer-fusion-workflow.svg` derives from the supplied `kalecancer-fusion-workflow.drawio 2.svg`. Only root accessibility attributes, title/description, scoped CSS and six decorative paths following the existing arrow geometry are added. Removing those additions produces the original SVG element tree exactly, including labels, images, styles and geometry. No image-generation tool or raster transformation was used. Motion follows data input, training and evaluation in phases. Original arrows always remain. Unsupported animation leaves the overlay invisible; reduced-motion settings disable it. The overview supplies descriptive alt text.

## Validation performed without a site build

- Four source/staging regression tests pass. Staging is exercised only in an isolated temporary directory; the user's `site/_staged` and built HTML are not replaced.
- Ten Colab preservation/bootstrap/runtime tests pass, including the selected notebook's generated Colab path. No generated notebook is rewritten.
- Fourteen JavaScript tests pass, covering Binder lazy launch/failures, picker-independent active-session leave protection and Present mode.
- All 14 redirect templates render with Jinja, including fragment-preserving targets.
- Python source compilation passes. Original SVG structure preservation was checked against the supplied file.
- Checksums confirm all 21 protected files (notebooks, Binder configuration, Colab setup/requirements/generator and agenda) are unchanged. Home session details/acknowledgement and About session details remain exactly as written. No scientific execution, dependency installation, commit or push was performed for this restructure.

The generated-HTML navigation, ToC, title, redirect and action tests were updated for the new structure but require the user's fresh Sphinx build; they were not run against stale HTML. No Sphinx build or browser preview was run.

## Manual review and execution limits

After building, inspect both overview pages and all four notebook pages, desktop/mobile and light/dark modes. Check sidebar highlights, previous/next links, On this page targets, Present mode, legacy bookmarks and the SVG with reduced motion on/off. In an active Binder session, verify a leave prompt before following a sidebar link or reloading.

All four mappings still offer Binder and Colab using their existing sources/configurations. Cancer Colab uses matching showcase copies and the documented Python 3.12 setup; Cardiac uses its own installation/download cells. Cardiac needs about 400 MB of tutorial data and follows upstream main. Prior local Linux execution checks do not establish hosted service availability, current account runtime choices, resource limits or visual animation behaviour. No hosted Binder or authenticated Colab test was repeated for this navigation-only change.
