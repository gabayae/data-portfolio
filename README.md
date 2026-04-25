# Yaé Gaba — Data Science Portfolio

![tests](https://github.com/gabayae/data-portfolio/actions/workflows/test.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Projects](https://img.shields.io/badge/projects-13-orange)

13 end-to-end data-science and machine-learning projects on **real public data** — forecasting, GLMs, survival analysis, hierarchical reconciliation, stochastic optimization, and experimental design.

**Live site:** [gabayae.github.io/data-portfolio](https://gabayae.github.io/data-portfolio/)

Each project follows the same pipeline:
**business question → data & EDA → modeling → validation → deployment → business outcome.**

---

## Projects

| # | Project | Domain | Real data source | Headline result |
|---|---|---|---|---|
| 01 | Health Supply-Chain Demand Forecasting | Health logistics | [USAID PEPFAR SCMS](https://www.kaggle.com/datasets/apoorvwatsky/supply-chain-shipment-pricing-data) | SARIMA WAPE 0.94 |
| 02 | Hourly Load Forecasting — PJM **([case study](./case-studies/pjm/))** | Energy | [PJM Hourly Consumption](https://www.kaggle.com/datasets/robikscube/hourly-energy-consumption) | GBM MAPE 6.2% (UC PI 99%) |
| 03 | Insurance Claims Frequency & Severity | Insurance | [freMTPL2 freq + sev](https://www.kaggle.com/datasets/floser/french-motor-claims-datasets-fremtpl2freq) | Tweedie Gini 0.310 |
| 04 | Hierarchical Retail Demand Forecasting | Retail | [M5 sample](https://www.kaggle.com/datasets/tarique7/m5-small-sample-dataset-whole-series) | MinT-OLS reconciliation |
| 05 | Stochastic Optimization for Resource Allocation | Health / Ops | [Kenya KMPDC + SHA](https://www.kaggle.com/datasets/xen0r0m/sha-kenya-licensed-health-facilities-and-funds) | Q-learning +122% vs manual |
| 06 | River Flow Forecasting — Lake Kariba | Hydropower | [Kariba Reservoir](https://www.kaggle.com/datasets/marbin/lake-kariba-reservoir-data) | GBM RMSE 7 cm |
| 07 | Solar Energy Forecasting — Nairobi | Energy | [NASA POWER API](https://power.larc.nasa.gov/) | GBM MAPE 9.4% |
| 08 | Customer Survival Analysis — MTN Nigeria | Telecom | [MTN Nigeria Churn](https://www.kaggle.com/datasets/oluwademiladeadeniyi/mtn-nigeria-customer-churn) | Cox PH + Weibull AFT |
| 09 | Flight Demand & Price — Southern Africa | Aviation | [SA Flight Prices](https://www.kaggle.com/datasets/mazano/southern-africa-flight-prices) | SARIMA MAPE 2.0% |
| 10 | Property Valuation — Lagos | Real estate | [Lagos Housing](https://www.kaggle.com/datasets/thedevastator/investigating-housing-prices-in-lagos-nigeria) | GBM R² 0.57 |
| 11 | Geospatial Farm-Output Forecasting | Agriculture | [African Farm Households](https://www.kaggle.com/datasets/crawford/agricultural-survey-of-african-farm-households) | GBM R² 0.66 |
| 12 | Churn Classification — MTN Nigeria | Telecom | [MTN Nigeria Churn](https://www.kaggle.com/datasets/oluwademiladeadeniyi/mtn-nigeria-customer-churn) | XGBoost AUC 0.71 |
| 13 | A/B Test Framework | Marketing | [Marketing Campaign A/B](https://www.kaggle.com/datasets/chebotinaa/fast-food-marketing-campaign-ab-test) | ANOVA F=21.95, p < 1e-9 |

---

## Tech stack

- **Languages:** Python, SQL
- **Time-series:** SARIMA, UnobservedComponents (state-space, Kalman filter), Prophet, ETS / Holt-Winters, ARIMA
- **ML:** scikit-learn (GradientBoostingRegressor, RandomForest, LogisticRegression), XGBoost, LightGBM
- **GLM / generalized:** statsmodels (Poisson, Gamma, Tweedie, Cox PH, Weibull AFT, OLS)
- **Survival:** lifelines (KaplanMeier, CoxPHFitter, WeibullAFTFitter)
- **Hierarchical reconciliation:** MinT-OLS
- **Stochastic optimization:** Markov Decision Processes, Q-learning, linear programming (`scipy.optimize.linprog`)
- **Experimentation:** ANOVA, Welch t-tests with Bonferroni correction, Bayesian A/B (posterior simulation)
- **Data engineering:** pandas, NumPy, Kaggle CLI, NASA POWER API
- **Visualization:** matplotlib, seaborn

## Domain coverage

- Energy (2): PJM hourly load, Nairobi solar
- Health logistics & operations (2): USAID supply chain, Kenya facility scheduling
- Telecom (2): MTN customer survival, MTN churn classification
- Time-series & forecasting infrastructure (2): hierarchical reconciliation, river flow
- Insurance (1), Aviation (1), Real estate (1), Agriculture (1), Experimentation (1)

## How to reproduce

```bash
git clone https://github.com/gabayae/data-portfolio.git
cd data-portfolio
make install            # install deps from pyproject.toml
make data               # download all datasets (Kaggle CLI required for some)
make notebooks          # execute every notebook end-to-end
```

For a single project:

```bash
cd <NN-project-name>
pip install -r requirements.txt
python download_data.py
jupyter nbconvert --to notebook --execute notebook.ipynb
```

Each notebook is self-contained — open it on GitHub and the rendered plots and tables are visible without running anything.

## Streamlit twin

`portfolio_app.py` is an interactive twin of `index.html` — same content, same color palette, with project filtering and clickable cards. Run it locally:

```bash
pip install -r requirements-app.txt
streamlit run portfolio_app.py
```

To deploy on Streamlit Community Cloud:
1. [share.streamlit.io](https://share.streamlit.io) → **New app**
2. Repository: `gabayae/data-portfolio` · Branch: `main` · Main file path: `portfolio_app.py`
3. Advanced settings → Python requirements file: `requirements-app.txt`
4. Deploy. Free, public, takes ~1 minute.

`portfolio_config.py` is the single source of truth for project metadata — edit there and both surfaces update.

## Profile photo

Drop a square headshot at `profile.jpg` in the repo root and the hero avatar on `index.html` automatically swaps the "YG" monogram for the photo (no code change — handled by `onerror="this.remove()"` on the `<img>`). Recommended ≥240×240 px; JPG / PNG / WebP all work.

## Contact

- **Email:** yaeulrich.gaba@gmail.com
- **LinkedIn:** [linkedin.com/in/gabayae](https://linkedin.com/in/gabayae)
- **Personal site:** [gabayae.github.io](https://gabayae.github.io)
- **Google Scholar:** [profile](https://scholar.google.com/citations?user=UTszjV4AAAAJ) (h-index 12)
- **Book (No Starch Press, 2024):** [The Shape of Data](https://nostarch.com/shapeofdata)

## License

MIT — see [LICENSE](./LICENSE).
