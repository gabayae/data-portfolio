<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/) · [Notebook](https://github.com/gabayae/data-portfolio/blob/main/09-flight-demand-southern-africa/notebook.ipynb)

---

# Flight Demand & Price — Southern Africa

## Scope

Exploratory analysis of a 31-day Kaggle scrape of Southern African flight listings. Volume forecasting on the top route (JNB–CPT) over a 6-day held-out window; price prediction conditional on `(route, airline, dow, hour, day_index)` across the full scrape.

**What this is not.** Not a 7–30 day forward forecast — the dataset only spans 2025-03-14 to 2025-04-13, so the SARIMA holdout is 6 days on a near-constant series (mean ≈ 90 flights/day, CV ≈ 8%). Not a pricing-curve model — the Kaggle scrape carries departure dates only, not booking dates, so there is no lead-time variable; the `day_index` feature is a day-of-window index 0–30, not a lead time.

## Data

- **Source:** [Southern Africa Flight Prices (Kaggle)](https://www.kaggle.com/datasets/mazano/southern-africa-flight-prices) — 15,393 flight listings over 31 days, departure timestamps, airline, route, price.

Run `python download_data.py` (Kaggle CLI required).

## EDA targets

- Price distribution by airline and route
- Day-of-week and hour-of-day effects
- Top routes by volume (CPT–JNB, JNB–DUR, etc.)

## Modeling

| Family | Model |
|---|---|
| Classical time-series | SARIMA on daily flight volume (top route) |
| ML challenger | `GradientBoostingRegressor` on `(route, airline, dow, hour, day_index)` for price prediction |
| Baseline | Naive-mean / naive-last / naive-seasonal (volume); `groupby(route, airline, dow, hour).mean()` lookup (price) |

## Validation

- Volume: 6-day held-out SARIMA MAPE, with bootstrap CI across the 6 test errors (the sample is too small to carry meaningful inference on its own).
- Price: random 80/20 split; GBM MAE compared against a cell-mean lookup baseline to show whether the GBM is learning anything beyond `groupby.mean()`.

## Deployment sketch

- Not a production system — scope is too narrow (31-day window) for a planning service.
- Longer scrapes (6+ months) with booking-date metadata would unlock the lead-time pricing dynamic the current scrape cannot support.

## Business outcome

- Methodology stub for daily volume + conditional price on short route-scrape data.
- The GBM reproduces within-cell means ± noise on this scrape — no evidence of a pricing-curve learned beyond the lookup baseline. The SARIMA 2% MAPE on 6 test points is directional, not evidence of skill.
