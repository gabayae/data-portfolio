# Changelog

Record of substantive changes to this portfolio. Newest entries first.

## Unreleased

### Added

- **Fifth long-form case study** at `case-studies/solar/` — Nairobi solar irradiance forecasting on 10 years of NASA POWER daily data. SARIMA, UnobservedComponents (state-space + Fourier annual), GBM with same-day weather covariates, and three baselines (naive, seasonal-naive, monthly climatology). Headline finding: **monthly climatology (12.3% MAPE) beats SARIMA (13.8%)** — at this latitude the seasonal envelope is most of the signal, and same-day weather is what moves point accuracy. GBM wins point-error at 9.4% MAPE; SARIMA/UC win on calibrated 95% prediction intervals (99% empirical coverage).
- Case-studies index now lists 5 deep-dives; sitemap and JSON-LD on the EN home updated to point project 07 at `case-studies/solar/` instead of the bare folder.
- FR case-studies index card for solar links to the EN case study (FR translation pending).

## v0.1.0 — 2026-04-25

Initial public release. 13 end-to-end data-science projects, 4 long-form case studies, EN/FR bilingual home page, Streamlit twin.

### Added

- **13 self-contained project folders** (`01-…` through `13-…`), each with its own `README.md`, executable `notebook.ipynb`, `download_data.py`, and `requirements.txt`. All notebooks executed end-to-end on real public data sourced from Kaggle, NASA POWER, and USAID PEPFAR SCMS.
- **Static landing page** `index.html` with PasserellAI editorial palette (warm cream `#fafaf7`, navy `#0f2a4a`, terracotta `#c85c3c`, Iowan Old Style serif headlines). Sticky nav, dark-navy gradient hero, headline stats grid, filterable project grid, process flow, capabilities, contact cards, footer.
- **Four long-form case studies** in `case-studies/`:
  - `pjm/` — hourly load forecasting on real PJM East data; SARIMA / state-space / GBM compared (`GBM 6.2% MAPE`).
  - `kariba/` — Lake Kariba river-flow forecasting on real Zambezi reservoir data (`GBM RMSE 7 cm`).
  - `fremtpl2/` — Tweedie compound-Poisson GLM vs Poisson + Gamma vs GBM on French motor TPL data (`Tweedie Gini 0.310; Poisson + Gamma top-decile lift 2.66`).
  - `kenya/` — Mobile-clinic scheduling as MDP on real KMPDC + SHA data; Q-learning vs capped LP vs manual (`Q-learning +122% / LP-capped +39% with equity`).
- **Case-studies index page** at `case-studies/` with cards previewing all four.
- **Custom `404.html`** with the editorial palette and suggested-links card.
- **Streamlit twin** (`portfolio_app.py` + `portfolio_config.py`): interactive version of the static site, deployable for free on Streamlit Community Cloud. `portfolio_config.py` is the single source of truth for project metadata; both surfaces read from it.
- **Bilingual home page**: `fr/index.html` is a full French translation built via a one-shot translation map covering ~120 strings. Language switch in the nav of both pages, `hreflang` alternate tags, `og:locale` + `og:locale:alternate`.
- **SEO scaffold**:
  - `favicon.svg` and `og-card.png` (1200×630, rendered via Chromium for clean fonts) — both YG monogram in navy + terracotta.
  - Full Open Graph and Twitter Card meta tags pointing at the OG card.
  - `<link rel="canonical">` on every page.
  - `theme-color` meta (`#0f2a4a`) for mobile browser chrome tinting.
  - JSON-LD `@graph` with `Person` (sameAs to LinkedIn / GitHub / Scholar, knowsAbout, knowsLanguage), `WebSite` (inLanguage en/fr), and `ItemList` of all 13 projects with positions and URLs.
  - `sitemap.xml` with `xhtml:link` alternate hreflang tags and entries for every page including the four case studies.
  - `robots.txt` allowing all + sitemap pointer.
- **Project README nav chips**: every `01-…/README.md` through `13-…/README.md` starts with `[← Portfolio] · [Notebook] · [Case study →]` (case-study link present where applicable). Marked with an HTML comment so future re-runs of the helper would refresh idempotently.
- **Repo scaffolding**: `pyproject.toml` (package metadata + ruff config), `Makefile` (`install / data / notebooks / test / clean`), `CONTRIBUTING.md`, `LICENSE` (MIT), `.gitignore` excluding `data/` and `artifacts/`, `requirements-app.txt` for the Streamlit deploy.
- **CI workflow** at `.github/workflows/test.yml`: validates every notebook is well-formed JSON, parses `index.html`, and lints `download_data.py` files with ruff. Runs on push and pull_request to `main`. Status: green on every commit so far.
- **Link integrity verification**: a Python crawler over every HTML and Markdown file, parsing `href` / `src` / Markdown link syntax, confirming each internal target resolves. 130+ links checked, all clean.

### Notes

- The `data/` folders inside each project are gitignored. Run `make data` (or `python download_data.py` per project) to fetch the real datasets — Kaggle CLI + auth required for Kaggle sources.
- The hero avatar shows a "YG" monogram by default; dropping a square `profile.jpg` in the repo root automatically swaps it in (handled by `onerror="this.remove()"` on the `<img>`).

### Pending (non-code)

- **GitHub Pages enablement** — needs to be flipped on in the repo settings to make the live URLs resolve.
- **Repo description and homepage** — to be set on github.com (the writer-CLI on this machine doesn't have admin scope here).
- **Streamlit Cloud deploy** — optional, takes ~1 min at `share.streamlit.io` once the repo is public.
