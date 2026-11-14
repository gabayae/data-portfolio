<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/) · [Notebook](https://github.com/gabayae/data-portfolio/blob/main/10-property-valuation-lagos/notebook.ipynb) · [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/gabayae/data-portfolio/blob/main/10-property-valuation-lagos/notebook.ipynb)

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
- **Ranking quality:** Overall Spearman ρ = **0.748 [95% CI: 0.722, 0.773]** on log-price (B=1000 bootstrap on the test fold). Per-neighborhood ρ (n ≥ 25 only) spans a wide range:

  | Submarket (n ≥ 25) | n | Spearman ρ |
  |---|---|---|
  | Ajah | 119 | 0.75 |
  | Ogba | 40 | 0.73 |
  | Sangotedo | 73 | 0.72 |
  | Surulere | 47 | 0.72 |
  | Ikoyi | 132 | 0.65 |
  | Ojo | 70 | 0.64 |
  | VI | 57 | 0.59 |
  | Ikeja | 133 | 0.55 |
  | Lekki | 516 | 0.49 |
  | Amuwo-Odofin | 40 | 0.46 |
  | Other | 322 | 0.43 |
  | Ikorodu | 65 | 0.42 |
  | Ibeju-Lekki | 163 | 0.41 |
  | Kosofe | 60 | 0.38 |
  | Ipaja | 41 | 0.28 |
  | Yaba | 44 | 0.22 |

  The ranking claim holds strongly in five submarkets (Ajah, Ogba, Sangotedo, Surulere, Ikoyi — all ρ > 0.6). It is moderate in the largest submarket (Lekki, ρ=0.49 on n=516), and weak in three (Yaba, Ipaja, Kosofe — all ρ < 0.4). A deployment should disclose the per-submarket variance, not just the aggregate ρ.
- `parse_type` priority fixed to most-specific-first so `"semi-detached house"` → `semi-detached` (not `house`), `"detached duplex"` → `detached` (not `duplex`), etc.

## Deployment sketch

- Model output is suitable for *ranking* at aggregate level (Spearman ρ = 0.748 overall) and in the stronger submarkets (Ajah, Ogba, Sangotedo, Surulere, Ikoyi all ρ > 0.6), not for anchoring individual-property valuations (raw-scale MAPE too wide). In the weak-ρ submarkets (Yaba ρ=0.22, Ipaja ρ=0.28, Kosofe ρ=0.38) even the ranking claim doesn't hold cleanly and a dashboard should flag those listings as low-confidence.
- Point-estimate deployment would require either (a) a quantile-GBM pair (`loss='quantile'`, `alpha=0.1/0.9`) to produce honest intervals, or (b) richer features (floor area, year built, condition) that this scrape does not include.

## Business outcome

- A working residential-price model on a free Kaggle Lagos scrape; the pipeline is the point, not the predictions.
- Usable for ranking at aggregate level (Spearman ρ = 0.748 [0.722, 0.773]) and in the five stronger submarkets (all ρ > 0.6). Raw-scale uncertainty remains too wide to anchor individual appraisals; the per-submarket ρ table in Validation is the honest surface the deployment UI should expose.
- The same pipeline would run on Abuja, Ibadan, or Port Harcourt scrapes with the same structure.
