# Flight Demand & Price Forecasting — Southern Africa

## Business question

Can we forecast flight prices and demand on Southern African routes 7–30 days out so:
- Airlines (FlySafair, LIFT, SAA) can dynamically tune prices
- Travel agencies can advise customers on optimal booking windows
- Tourism boards can anticipate seasonal demand pressure on Cape Town, Durban, Johannesburg routes

This is the African analog of the Calgary transit ridership project — same time-series and demand-modelling toolkit, applied to inter-city air-transport demand.

## Data

- **Source:** [Southern Africa Flight Prices (Kaggle)](https://www.kaggle.com/datasets/mazano/southern-africa-flight-prices) — 15,393 flights, departure/arrival timestamps, airline, route, price.

Run `python download_data.py` (Kaggle CLI required).

## EDA targets

- Price distribution by airline and route
- Day-of-week and hour-of-day effects
- Lead-time-to-departure pricing patterns
- Top routes by volume (CPT–JNB, JNB–DUR, etc.)

## Modeling

| Family | Model |
|---|---|
| Classical time-series | SARIMA on daily flight volume per route |
| ML for forecasting | Gradient-boosted price predictor (route, airline, day-of-week, lead time) |
| Demand + price joint | LightGBM with price elasticity features |

## Validation

- Held-out 20% of flights for price prediction (MAE, RMSE, MAPE)
- Time-aware split for daily volume forecasting

## Deployment

- API `GET /forecast?route=CPT-JNB&horizon=30` returning daily expected volume + 95% PI
- Dynamic-price endpoint for airlines

## Business outcome

- Daily volume forecasts feed crew/aircraft scheduling
- Price-elasticity insight informs revenue-management decisions
- Same pipeline trivially scales to West/East African route networks
