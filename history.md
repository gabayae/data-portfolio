# Build history — `gabayae/data-portfolio`

A complete log of how this portfolio was built. Two intensive sessions, 27 commits, 13 end-to-end data-science projects, 5 long-form bilingual case studies. Sessions ran 2026-04-25 → 2026-04-26.

---

## At a glance

| | |
|---|---|
| Total commits on `main` | **27** |
| End-to-end projects | **13** (each: real public data, executable notebook, README, requirements) |
| Long-form case studies | **5**, fully bilingual EN/FR (10 case-study pages) |
| HTML pages | 15 (EN + FR home, EN + FR case-studies index, 5 EN + 5 FR case studies, bilingual 404) |
| Notebooks | 14 (one per project + 1 sample) |
| Languages | English + French (full mirror) |
| Structured data | 12 JSON-LD blocks: 2 home pages (Person + WebSite + ItemList) + 10 case-study Article schemas |
| OG cards | 6 (1 site-level + 5 per-case-study, each 1200×630, rendered via Playwright Chromium) |
| Streamlit twin | `portfolio_app.py` reads from `portfolio_config.py` (single source of truth) |

---

## Origin: the brief

The user (Yaé Gaba, PhD) had a Microsoft AI Data Scientist position to apply for. The original ask was a CV refresh; it grew into a complete portfolio.

The portfolio's editorial design follows the [PasserellAI](https://passerellai.com/) palette — warm cream `#fafaf7`, navy `#0f2a4a`, terracotta accent `#c85c3c`, Iowan Old Style serif headlines over Inter sans body — chosen as a deliberately editorial alternative to the typical "dashboard / dark-mode" portfolio aesthetic.

---

## The 13 projects

Every project lives in its own folder with a README, an executable Jupyter notebook, a `download_data.py` script, and a pinned `requirements.txt`. All 13 were executed end-to-end on **real public data** — no toy datasets, no synthetic pipelines.

| # | Project | Methods | Headline metric | Data source |
|---|---|---|---|---|
| 01 | Health Supply-Chain Demand Forecasting | SARIMA, GBM | MAPE 12.4% | USAID PEPFAR SCMS (Kaggle) |
| 02 | Hourly Electricity Load — PJM East | SARIMA, UC state-space, GBM | GBM **6.2% MAPE**; UC PI 99% | PJM Hourly Consumption (Kaggle) |
| 03 | Insurance Claims Frequency & Severity | Poisson + Gamma GLM, Tweedie, XGBoost | Tweedie Gini **0.310**; Poisson+Gamma top-decile lift 2.66 | freMTPL2 (Kaggle) |
| 04 | Hierarchical Retail Demand — M5 | MinT-OLS reconciliation, ETS, GBM | MASE **0.91** at level-3 | Walmart M5 sample (Kaggle) |
| 05 | Stochastic Optimization — Kenya | Q-learning, capped LP, MDP | Q-learning **+122%**; LP-capped **+39%** with explicit equity | KMPDC + SHA Kenya |
| 06 | River Flow Forecasting — Lake Kariba | SARIMA, UC state-space, GBM with exog | GBM **RMSE 7 cm**; SARIMA PI 100% | Zambezi River Authority |
| 07 | Solar Energy Forecasting — Nairobi | SARIMA, UC + Fourier annual, GBM with weather exog | GBM **9.4% MAPE**; climatology 12.3% beats SARIMA 13.8% | NASA POWER API |
| 08 | Customer Survival — MTN Nigeria | Kaplan-Meier, Cox PH, Weibull AFT, log-rank | Cox concordance **0.71** | MTN Nigeria customer tenure (Kaggle) |
| 09 | Flight Demand & Price — Southern Africa | XGBoost, quantile regression | RMSE **$28** on price | Southern Africa flights (Kaggle) |
| 10 | Property Valuation — Lagos | RandomForest, SHAP, geospatial features | R² **0.78** | Lagos housing (Kaggle) |
| 11 | Geospatial Farm-Output Forecasting | GBM with raster features | R² **0.66** | African Farm Households (Kaggle) |
| 12 | Churn Classification — MTN Nigeria | LogReg, RF, XGBoost, ROC/PR sweep | XGBoost **AUC 0.71** | MTN Nigeria (Kaggle) |
| 13 | A/B Test Framework — Marketing | ANOVA, Welch t, Bonferroni, Bayesian A/B | F=21.95, **p<1e-9** | Fast-food A/B (Kaggle) |

---

## The 5 case studies

Each case study is a long-form deep-dive that draws plots from its executed notebook. Same template across all five: hero with hero-meta, sticky table-of-contents, prose sections (Summary → Why this matters → Business question → Data → EDA → Modelling approach → Results → Trade-offs → Deployment → Lessons), one results table, multiple figures, callout box. Every case study lives at both `case-studies/<name>/` (EN) and `fr/case-studies/<name>/` (FR), with a 1200×630 OG card and Article JSON-LD schema.

| Case study | Domain | Methodology family | The honest finding |
|---|---|---|---|
| `case-studies/pjm/` | Energy | Time-series | UC state-space actually performs **worse** than SARIMA for point forecasts (19.3% vs 14.5%); GBM with weather covariates wins point error, but UC's 99% PI coverage is the operationally useful number for procurement. |
| `case-studies/kariba/` | Hydropower | Time-series with exog | A 7 cm RMSE on a 7 m operational band turns "are we going to breach turbine safety in 30 days?" from a guess into a calibrated probability. Turbine discharge as exog is a 2× point-error improvement. |
| `case-studies/solar/` | Solar | Time-series | **Monthly climatology (12.3% MAPE) beats SARIMA (13.8%)**. At Nairobi's latitude the seasonal envelope is most of the predictable signal; same-day cloud + humidity covariates are what move point accuracy. |
| `case-studies/fremtpl2/` | Insurance | GLMs (actuarial pricing) | Tweedie wins on segmentation power (Gini); Poisson + Gamma wins on top-decile lift. The choice is an actuarial decision, not a modelling one. |
| `case-studies/kenya/` | Health Ops | Stochastic optimization / RL | Q-learning beats manual round-robin by 122% on patients-served, but the *constraint formulation* matters more than the algorithm — a capped LP with explicit equity at +39% is more defensible than the unconstrained Q-learning maximum. |

---

## The 27 commits in order

```
1.  803d52c  2026-04-25  Initial commit (auto from github.com create)
2.  807f120  2026-04-25  Initial portfolio: 13 data-science projects on real public data
3.  aa91d8e  2026-04-25  SEO polish: Open Graph + favicon + sitemap + robots
4.  846c4ec  2026-04-25  Add PJM case-study page + wire up case-study link
5.  25ebfbb  2026-04-25  Wire profile photo path with monogram fallback + restore full README
6.  c02f75f  2026-04-25  Add Streamlit twin (portfolio_app.py + portfolio_config.py)
7.  caefd14  2026-04-25  Add EN/FR bilingual toggle (mirror PasserellAI pattern)
8.  349d3b1  2026-04-25  Add Lake Kariba case-study page
9.  8717190  2026-04-25  Add nav header to every project README
10. c3375bc  2026-04-25  Add case-studies index page + custom 404
11. 9bb4ce1  2026-04-25  Link integrity sweep + JSON-LD structured data + theme-color
12. c4e8a1e  2026-04-25  Add freMTPL2 case study (third deep-dive)
13. 1440393  2026-04-25  Add Kenya MDP / Q-learning case study (fourth deep-dive)
14. 50cf9ef  2026-04-25  Sync Streamlit config with all 4 case studies + refresh parent docs
15. e827d19  2026-04-25  Add CHANGELOG.md (v0.1.0 release notes)
16. f66de2b  2026-04-25  Per-case-study OG cards
17. 037ec22  2026-04-25  FR translation of PJM case study
18. 2e092b9  2026-04-25  FR translation of Kariba case study
19. 9afecb8  2026-04-26  FR translation of freMTPL2 case study
20. ee83c7a  2026-04-26  FR translation of Kenya case study (last of the four)
21. 77c1bdd  2026-04-26  FR case-studies index page
22. abb7e51  2026-04-26  Bilingual 404 page
23. a906fb8  2026-04-26  Fifth case study — Solar Nairobi (NASA POWER)
24. 65dc9a9  2026-04-26  FR translation of Solar case study
25. 851e634  2026-04-26  Per-case-study OG card for Solar Nairobi
26. 448fd90  2026-04-26  Article JSON-LD on all 10 case-study pages
27. 5eaa9c7  2026-04-26  JSON-LD on FR home — Person + WebSite + ItemList graph
```

---

## Detailed timeline

### Day 1 (2026-04-25): foundation, 16 commits

**1. CV → portfolio scope expansion.** The original CV brief mentioned three sample projects. The user asked for the full pipeline — folder per project, real data, executable notebook — and grew the count from 5 to 13 to mirror an existing inspiration repo (`portfolio-with-calgary-data/`). Real data sourcing: Kaggle for 11 projects, NASA POWER API for solar, USAID PEPFAR SCMS for the supply-chain project.

**2. Editorial design.** The user shared the [PasserellAI](https://passerellai.com/) site as a reference and asked for a similar feel rather than a dashboard aesthetic. The palette (cream + navy + terracotta) and typography (Iowan Old Style serif + Inter sans) were lifted from there. The first version had the colors swapped (terracotta primary, navy accent) and the user said "swap the colors" — the navy-primary / terracotta-accent version stuck.

**3. Folder structure.** `01-…/` through `13-…/`, each with README.md + notebook.ipynb + download_data.py + requirements.txt + gitignored `data/`. Single shared `pyproject.toml`, `Makefile`, `CONTRIBUTING.md`, `LICENSE` (MIT) at the root.

**4. Initial push to `gabayae/data-portfolio`.** SSH alias setup: `git@github-gabayae:gabayae/...` because the local `gh` CLI is authed as `guydev42`, not `gabayae`. This gating remained for the whole session — anything requiring a GitHub API token call against `gabayae/...` (enabling Pages, setting repo description) had to fall to the user.

**5. Six bonus tasks materialised after the initial ship:** Streamlit twin, profile-photo wiring, case-study page, SEO polish, EN/FR bilingual, README nav chips. Each became its own commit. The session went well past those six.

**6. Surprises hit during day 1:**
- USAID SCMS data had `"Date Not Captured"` strings; the median delay computed to 0. Pivoted that section to use MTN customer-tenure survival instead.
- Kenya facilities CSV was actually XLSX disguised as `.csv` — switched to the SHA Kenya licensed-facilities dataset.
- PJM real-data finding: GBM hit 6.2% MAPE; UC state-space hit 19.3%, **worse than SARIMA at 14.5%**. The CV initially claimed an "18% MAPE reduction from UC" — corrected to remove the unsupported claim.
- freMTPL2 first run produced a negative Gini (-0.40). Root cause: `predict()` was called with `offset=offset_te` which scaled predictions by exposure; switched to `offset=zeros_like(offset_te)` to get per-exposure rates.
- ImageMagick rendered the OG card SVG with ugly fallback fonts. Switched to **Playwright Chromium headless** for clean Inter / Iowan Old Style rendering. This pattern was reused for all 5 per-case-study OG cards on day 2.

**7. Identity divergence.** The CV uses `yaegaba@gmail.com` and Rocky Mountain House, AB Canada. The portfolio site uses `yaeulrich.gaba@gmail.com` and Cotonou, Benin. This is **intentional** — the two surfaces target different audiences.

### Day 2 (2026-04-26): bilingual completion + structured data, 11 commits

**1. FR translations of all 4 day-1 case studies.** Pattern: read EN file, build a Python translation map (~120 strings), one-shot script writes the FR file with site-absolute paths (`/data-portfolio/case-studies/.../plot-NN.png`) so the plots are shared, not duplicated. Each FR file declares `og:locale fr_FR`, `og:locale:alternate en_US`, and reciprocal hreflang. Scripts had to be `Write`-tooled rather than heredoc'd because heredoc choked on French apostrophes.

**2. FR case-studies index page** mirroring the EN index, links updated to `./pjm/`, `./kariba/`, `./fremtpl2/`, `./kenya/`.

**3. Bilingual 404 page**: single file with EN+FR inline content, JS detects `/data-portfolio/fr/...` URL prefix and toggles which div shows. Both halves include a "you might be looking for" suggested-links card and a language switcher.

**4. Fifth case study — Solar Nairobi.** New territory: NASA POWER API as a free, programmatic, no-auth weather data source. The notebook covers SARIMA, UnobservedComponents with Fourier annual exog, and GBM with same-day weather covariates. Three baselines added: naive-last, naive-seasonal, **and monthly climatology** — climatology came in at 12.3% MAPE, beating SARIMA at 13.8%. This became the case study's headline finding: at this latitude the seasonal envelope dominates predictability; same-day cloud + humidity is what moves point accuracy.

**5. FR translation of Solar** brought all 5 case studies to bilingual parity.

**6. Per-case-study OG card for Solar** brought it to parity with the other 4 (each 1200×630, rendered via Playwright Chromium).

**7. Article JSON-LD** added to all 10 case-study pages (5 EN + 5 FR). Each page declares `@type: Article` with headline, description, OG image, canonical URL, `inLanguage`, dates, and Person author/publisher with `sameAs` to LinkedIn / GitHub / Scholar.

**8. JSON-LD on FR home page**: mirrored the EN home's `Person + WebSite + ItemList` graph with French project names. Both home pages share the same Person `@id` so search engines treat them as one identity rather than two.

---

## Architecture decisions

**Static HTML, not Jekyll/Hugo/Astro.** Every page is a single self-contained HTML file with inlined CSS in `<style>` tags. The cost: no shared templates, so changes to the case-study chrome require touching 10 files. The benefit: GitHub Pages serves it with zero build step, and a recruiter inspecting the source sees readable, hand-crafted HTML rather than minified bundles.

**Site-absolute paths for cross-language assets.** FR pages reference `/data-portfolio/case-studies/.../plot-NN.png` rather than relative paths. This means the four plot files per case study live in the EN folder only; the FR pages link to them. Saves ~5 MB of repo size and ensures EN and FR can never diverge on plot content.

**`portfolio_config.py` as the single source of truth.** Both the static `index.html` (manually curated) and the Streamlit twin (programmatically generated) read project metadata from `portfolio_config.py`. When Solar got its case-study link, only `portfolio_config.py` and `index.html` needed updating; the Streamlit app picked it up automatically.

**SSH alias multi-account.** `git@github-gabayae:gabayae/data-portfolio.git` — the `github-gabayae` host alias in `~/.ssh/config` points the auth at the gabayae key while the system `gh` CLI stays authed as `guydev42`. Standard pattern from `al-folio` setup.

**Bilingual via mirrored folders, not URL params.** `/fr/...` is a real folder mirror, not `?lang=fr`. Trades disk space for SEO simplicity and per-page hreflang declarations.

---

## Still requires the user's hands (gating reason: `gh` CLI is authed as `guydev42`, not `gabayae`)

1. **Enable GitHub Pages** — repo Settings → Pages → Deploy from branch → `main` / `/ (root)`. Live URLs come up ~1–2 min after that:
   - English home: https://gabayae.github.io/data-portfolio/
   - French home: https://gabayae.github.io/data-portfolio/fr/
   - Case-studies index (EN + FR): `/case-studies/` and `/fr/case-studies/`
   - Five individual case studies (each at `/case-studies/<name>/` and `/fr/case-studies/<name>/`)
2. **Set repo description + homepage** on the GitHub page — `gh` PATCH returns 404 because the token belongs to `guydev42`.
3. **Drop `profile.jpg` at the repo root** → hero avatar swaps from "YG" monogram to the real photo automatically.
4. **Optional — deploy Streamlit twin** at https://share.streamlit.io: pick `gabayae/data-portfolio`, branch `main`, file `portfolio_app.py`, requirements file `requirements-app.txt`. Free, ~1 min.

---

## What's next (parked)

- **Live link validation against deployed Pages**: the local link checker validates the local filesystem; once Pages is enabled, sweep `https://gabayae.github.io/data-portfolio/...` for any drift.
- **Google Rich Results Test API check**: confirm the 12 JSON-LD blocks all parse cleanly under Google's validator.
- **Per-project Article schema** for the 8 projects without case studies — currently their READMEs render as folder indices but carry no schema.
- **Reading time + previous/next navigation** between case studies — UX polish, finite scope.
- **Optional: French translations of the 13 project READMEs**: currently FR home cards link back to the EN folder READMEs.

---

*Authored 2026-04-26 as a complete record of the build sessions. The CHANGELOG.md tracks substantive changes going forward; this file is the origin story.*
