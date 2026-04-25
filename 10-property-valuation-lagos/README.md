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
| GBM | LightGBM / GradientBoostingRegressor with one-hot neighborhood + parsed features |

## Validation

- 80/20 random split; metrics: R², MAE on log-price, MAPE
- Compare OLS vs. GBM head-to-head

## Deployment

- API `POST /property-valuation` returning price estimate + 80% interval
- Estate-agent dashboard with neighborhood-level distribution overlays

## Business outcome

- Estate agents and buyers anchor pricing on a model rather than vibes
- Mortgage lenders get an explainable valuation reference
- Same pipeline trivially extends to Abuja, Ibadan, Port Harcourt with neighborhood-tagged data
