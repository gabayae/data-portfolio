<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/) · [Notebook](https://github.com/gabayae/data-portfolio/blob/main/10-property-valuation-lagos/notebook.ipynb)

---

# Property Valuation — Lagos, Nigeria

## Business question

Can we predict listing prices for Lagos residential properties accurately enough to:
- Help buyers spot under-priced or over-priced listings
- Help estate agents anchor pricing recommendations
- Inform mortgage / valuation models for Nigerian lenders

## Data

- **Source:** [Housing Prices in Lagos, Nigeria (Kaggle)](https://www.kaggle.com/datasets/thedevastator/investigating-housing-prices-in-lagos-nigeria) — 9,784 sale listings, neighborhood, address, free-text property name with bedroom counts and property types embedded.

Run `python download_data.py`.

## EDA targets

- Price distribution by neighborhood (Ikoyi, Lekki, VI command premium; outskirts cheaper)
- Bedroom count and property type extracted from `Property_name`
- Land vs. Apartment vs. House vs. Duplex price differentials

## Modeling

| Family | Model |
|---|---|
| Linear regression | OLS on log-price with neighborhood + property-type + bedrooms |
| GBM | `GradientBoostingRegressor` with one-hot neighborhood + parsed features |

## Validation

- 80/20 random split (random because these are listings at unspecified dates, not a forecast).
- Dual-scale metrics: **R²(log) 0.58, R²(level) implicit lower; raw-NGN MAPE 146%, RMSE 366M NGN** for GBM. OLS: **R²(log) 0.51, raw-NGN MAPE 179%, RMSE 396M NGN**. The log-scale R² is comfortable; the raw-scale MAPE is honest about the limits — on a target with median ~₦50M, routinely being off by more than the true price means this is a ranking tool, not a point-valuation tool.
- `parse_type` priority fixed to most-specific-first so `"semi-detached house"` → `semi-detached` (not `house`), `"detached duplex"` → `detached` (not `duplex`), etc.

## Deployment sketch

- Model output is suitable for *ranking* listings against neighborhood baselines, not for anchoring individual-property valuations (the raw-scale MAPE is too wide for that).
- Point-estimate deployment would require either (a) a quantile-GBM pair (`loss='quantile'`, `alpha=0.1/0.9`) to produce honest intervals, or (b) richer features (floor area, year built, condition) that this scrape does not include.

## Business outcome

- Methodology stub for Lagos residential prices on a free Kaggle extract.
- The honest usage pattern is comparable-sorting at the neighborhood × type × bedrooms level; the raw-scale uncertainty is too wide to anchor individual appraisals.
- Pipeline extends trivially to Abuja, Ibadan, Port Harcourt with the same scrape structure.
