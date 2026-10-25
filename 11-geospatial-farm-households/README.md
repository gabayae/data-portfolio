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
| Spatial GBM | `GradientBoostingRegressor` with lat/lon + farm features |

## Validation

- **Known limitation (current notebook):** a random 80/20 split is used, but same-village observations share identical `(lat, lon)` and get spread across train and test — the GBM memorizes lat/lon lookup tables. The R²=0.66 reported under this split overstates generalization; the honest comparison requires `GroupKFold` on quantized lat/lon or a cluster identifier. Fix pending.
- Metrics: R² on log-sales, MAPE on raw sales

## Deployment sketch

- A microfinance-triage service would need per-cluster rather than per-household resolution, and should be re-trained whenever a new survey batch lands.
- Not a production system — the notebook stops at offline modeling.

## Business outcome

- Methodology stub for geospatial regression on survey data; the sample-size and spatial-leakage caveats above must be respected before any underwriting use.
