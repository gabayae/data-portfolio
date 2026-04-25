<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/) · [Notebook](./notebook.ipynb)

---

# Geospatial Farm-Output Forecasting — African Farm Households

## Business question

Given a farm's location (lat/lon, district) and basic attributes, can we predict its annual farm sales value? This is the African analog of the Calgary geospatial demand forecasting project — same spatial-regression toolkit applied to agricultural output across multiple African countries.

Use cases:
- Microfinance institutions sizing crop loans
- Input suppliers (fertilizer, seed) targeting underserved zones
- Agricultural extension agencies prioritizing district visits

## Data

- **Source:** [Agricultural Survey of African Farm Households (Kaggle)](https://www.kaggle.com/datasets/crawford/agricultural-survey-of-african-farm-households) — 9,597 farm households surveyed across multiple African countries with 1,754 attributes including lat/lon, district, household composition, farm size, climate exposure, and farm sales value.

Run `python download_data.py`.

## EDA targets

- Geographic spread of surveyed households
- District-level distribution of `farmsalev` (annual farm sales)
- Land-area distribution and tenure patterns
- Climate-exposure features (long-term temperature/rainfall shifts)

## Modeling

| Family | Model |
|---|---|
| Linear baseline | OLS on log-sales with district + farm-size features |
| Spatial GBM | GradientBoostingRegressor with lat/lon + farm features |
| Geographic GBM | LightGBM/GBM with district one-hot + spatial features |

## Validation

- 80/20 random split; hold-out district sanity check
- Metrics: R² on log-sales, MAPE on raw sales

## Deployment

- API `POST /farm-output-prediction` returning expected sales + interval given farm attributes + coordinates
- Spatial dashboard for microfinance loan-officer triage

## Business outcome

- Underwriting and field-targeting decisions backed by data, not vibes
- Spatial heatmap surfaces under-served districts for input suppliers
- Scales to any survey-based agricultural data with geo + outcome columns
