<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/) · [Notebook](https://github.com/gabayae/data-portfolio/blob/main/11-geospatial-farm-households/notebook.ipynb)

---

# Geospatial Farm-Output Forecasting — African Farm Households

## Business question

Given a farm's location (lat/lon, district) and basic attributes, can we predict its annual farm sales value? This is the African analog of the Calgary geospatial demand forecasting project — same spatial-regression toolkit applied to agricultural output across multiple African countries.

Use cases:
- Microfinance institutions sizing crop loans
- Input suppliers (fertilizer, seed) targeting underserved zones
- Agricultural extension agencies prioritizing district visits

## Data

- **Source:** [Agricultural Survey of African Farm Households (Kaggle)](https://www.kaggle.com/datasets/crawford/agricultural-survey-of-african-farm-households) — the full survey has 9,597 farm households across multiple African countries with 1,754 attributes.
- **Modeled subset:** **931 rows** after `dropna` on `(lat, lon, farmsalev)`. After the subset, the `district` column collapses to a single value ("Unknown"), so the district OHE in the current pipeline carries no signal. The long-term climate-shift features are mostly imputed to a single median in the subset and contribute little.

Run `python download_data.py`.

## EDA targets

- Geographic spread of the 931 modeled households
- Distribution of `farmsalev` (annual farm sales) on the modeled subset
- Land-area distribution and tenure patterns

## Modeling

| Family | Model |
|---|---|
| Linear baseline | OLS on log-sales with lat/lon + farm-size features |
| Non-parametric geo baseline | `KNeighborsRegressor(n_neighbors=10)` |
| Non-linear challenger | `GradientBoostingRegressor` with lat/lon + farm features |

## Validation

- **Random 80/20 split (leaky):** OLS R² 0.31 · KNN R² 0.57 · GBM R² 0.66. Multiple rows share identical `(lat, lon)` (same-village observations); random splitting lets the GBM memorize village-level lookup tables. Retained in the notebook only to make the leakage visible.
- **Spatial `GroupKFold` on 1-degree lat/lon cells, 5 folds (honest):** OLS R² **0.22 ± 0.38** · KNN R² **0.14 ± 0.44** · GBM R² **0.12 ± 0.34**. 35 spatial cells, median 27 obs/cell. The GBM's R² collapses from 0.66 to 0.12 — the +0.54 under random splitting was memorization, not generalization. All models have very wide fold variance; the honest signal across unseen spatial cells is weak.
- Metrics: R² on log-sales (primary), MAE on log-sales, MAPE on raw sales.

## Deployment sketch

- A microfinance-triage service would need per-cluster rather than per-household resolution, and should be re-trained whenever a new survey batch lands.
- Any deployment would need a cluster-ID join from the survey raw data, so GroupKFold corresponds to the actual sampling design rather than an ad-hoc 1-degree lat/lon grid.

## Business outcome

- Methodology stub for geospatial regression on survey data; the sample-size and spatial-leakage caveats above must be respected before any underwriting use.
