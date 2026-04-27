# Changelog

Record of substantive changes to this portfolio. Newest entries first.

## Unreleased

### Added

- **Fifth long-form case study** at `case-studies/solar/` — Nairobi solar irradiance forecasting on 10 years of NASA POWER daily data. SARIMA, UnobservedComponents (state-space + Fourier annual), GBM with same-day weather covariates, and three baselines (naive, seasonal-naive, monthly climatology). Headline finding: **monthly climatology (12.3% MAPE) beats SARIMA (13.8%)** — at this latitude the seasonal envelope is most of the signal, and same-day weather is what moves point accuracy. GBM wins point-error at 9.4% MAPE; SARIMA/UC win on calibrated 95% prediction intervals (99% empirical coverage).
- Case-studies index now lists 5 deep-dives; sitemap and JSON-LD on the EN home updated to point project 07 at `case-studies/solar/` instead of the bare folder.
- **FR translation** of the Solar case study at `fr/case-studies/solar/`. EN/FR alternate hreflang on both sides; FR case-studies index now links to the local FR translation; sitemap carries the bilingual pair. All 5 case studies are now bilingual EN/FR.
- **Per-case-study OG card for Solar** (`case-studies/solar/og-card.png`) — brings Solar to parity with the other 4 case studies. Same dark-navy + terracotta gradient, headline metric "GBM 9.4% MAPE", rendered via Playwright Chromium. Solar EN+FR pages now reference it instead of the site-level OG card.
- **Article JSON-LD** on all 10 case-study pages (5 EN + 5 FR). Each page declares `@type: Article` with headline, description, OG image, canonical URL, `inLanguage`, `datePublished`/`dateModified`, and Person author/publisher with `sameAs` to LinkedIn/GitHub/Scholar. Combined with the home-page `Person + WebSite + ItemList`, search engines now have a complete bilingual graph.
- **JSON-LD on FR home**: mirrors the EN home's `Person + WebSite + ItemList` graph with French project names. Both home pages share the same Person `@id` so search engines collapse the EN and FR sides to one identity.
- **Prev/next case-study navigation** at the bottom of every case study (10 pages). Chain order: PJM → Kariba → Solar → freMTPL2 → Kenya. PJM and Kenya only have one direction. Localised labels ("Previous"/"Next" vs "Précédente"/"Suivante").
- **BreadcrumbList JSON-LD** on every case-study page (10 pages). 3-step crumb: portfolio root → case-studies index → current page, with localised names. Pairs with the existing Article schema for richer Google rich-result rendering.
- **history.md** at the repo root — origin story for the build (27 commits, 13 projects, 5 case studies, day-by-day timeline, architecture decisions, what still needs the user's hands).
- **Reading-time badge** at the top of each case study (10 pages) — first item in the hero meta strip, e.g. `Read · 6 min · 1,354 words` (EN) or `Lecture · 8 min · 1,658 mots` (FR). Localised, computed at build time from the article body word count at 230 wpm.
- **Article schema enriched** with `wordCount` and `timeRequired` (ISO 8601 duration, e.g. `PT6M`) on every case-study page — the same numbers Google now exposes as a "X min read" snippet next to the search result.
- **Explicit `width`/`height` on every plot image** across all 10 case studies (34 img tags total). Eliminates Cumulative Layout Shift (CLS) — the browser reserves the right rectangle before the PNG arrives, so the page no longer reflows when plots load. Real Lighthouse / Core Web Vitals win.
- **`<lastmod>` on every sitemap URL** (27 entries — was 2/27 before). Lets crawlers detect changes and re-fetch promptly: home pages and all 10 case studies + indices set to today's date; the 13 project-folder URLs keep their original publish dates.
- **Favicon variants + web app manifest**. Renders the existing SVG favicon at 16, 32, 180 (Apple touch icon), 192 (Android), and 512 (PWA splash) px via Playwright Chromium for clean text rendering. New `site.webmanifest` declares the portfolio as a standalone PWA with theme/background colors matching the editorial palette. All 15 HTML pages now reference the full set via site-absolute paths so the right size loads from any URL depth.
- **Print stylesheet for case studies**: `@media print` block on all 10 case-study pages. Drops nav/TOC/footer/prev-next/CTA chrome, flattens the dark hero gradient to a clean white masthead with a navy underline, expands the article to full A4 width, prevents page breaks inside figures + result tables + callouts, prints external URL after every link via `[href]::after`, sets `orphans: 3` and `widows: 3` on body copy. Recruiter print-to-PDF now produces a clean 6-8 page document instead of a screenshot of the dark editorial layout.
- **`validate_site.py`**: pre-push smoke test for site-wide consistency. Walks every HTML page, sitemap entry, JSON-LD block, hreflang declaration, and manifest icon. Exits 0 on PASS / 1 on FAIL. Current state: 15 pages, 273 internal links, 22 JSON-LD blocks (10 Article + 10 BreadcrumbList + 2 ItemList + 2 Person + 2 WebSite), 27 sitemap URLs all with lastmod, 4 manifest icons.
- **CI now runs `validate_site.py`** on every push and PR (`.github/workflows/test.yml`). Replaces the old one-line "index.html parses" check with the full site-wide validator — link drift, JSON-LD parse errors, missing hreflang reciprocals, missing sitemap entries, or missing manifest icons fail the build automatically.
- **FR translations of all 13 project READMEs** at `fr/<slug>/README.md`. Each README mirrors its EN sibling section-for-section: nav chip → business question → data + EDA → modelling table → validation → deployment → business outcome. Carnet links point at the original `/data-portfolio/<slug>/notebook.ipynb` (notebooks are language-neutral); FR project READMEs carry FR text only. The portfolio is now bilingual end-to-end — every reader-facing surface has a French twin.
- **FR home Projet buttons** swapped from `../<slug>/` (EN folder) to `./<slug>/` (FR folder). Case-study projects keep their "Étude de cas →" buttons (already FR).
- **Sitemap expanded to 40 URLs** (was 27). 13 new FR project URLs added; each EN/FR pair carries reciprocal `xhtml:link` alternate hreflang. `validate_site.py` confirms 100% lastmod coverage and 100% URL → file resolution.

## v0.1.0 — 2026-04-25

Initial public release. 13 end-to-end data-science projects, 4 long-form case studies, EN/FR bilingual home page, Streamlit twin.

### Added

- **13 self-contained project folders** (`01-…` through `13-…`), each with its own `README.md`, executable `notebook.ipynb`, `download_data.py`, and `requirements.txt`. All notebooks executed end-to-end on real public data sourced from Kaggle, NASA POWER, and USAID PEPFAR SCMS.
- **Static landing page** `index.html` with an editorial palette (warm cream `#fafaf7`, navy `#0f2a4a`, terracotta `#c85c3c`, Iowan Old Style serif headlines). Sticky nav, dark-navy gradient hero, headline stats grid, filterable project grid, process flow, capabilities, contact cards, footer.
- **Four long-form case studies** in `case-studies/`:
  - `pjm/`: hourly load forecasting on real PJM East data; SARIMA / state-space / GBM compared (`GBM 6.2% MAPE`).
  - `kariba/`: Lake Kariba river-flow forecasting on real Zambezi reservoir data (`GBM RMSE 7 cm`).
  - `fremtpl2/`: Tweedie compound-Poisson GLM vs Poisson + Gamma vs GBM on French motor TPL data (`Tweedie Gini 0.310; Poisson + Gamma top-decile lift 2.66`).
  - `kenya/`: Mobile-clinic scheduling as MDP on real KMPDC + SHA data; Q-learning vs capped LP vs manual (`Q-learning +122% / LP-capped +39% with equity`).
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

- **GitHub Pages enablement**: needs to be flipped on in the repo settings to make the live URLs resolve.
- **Repo description and homepage**: to be set on github.com (the writer-CLI on this machine doesn't have admin scope here).
- **Streamlit Cloud deploy**: optional, takes ~1 min at `share.streamlit.io` once the repo is public.
