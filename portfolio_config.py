"""Portfolio configuration — single source of truth for the Streamlit app.

Mirrors the project metadata shown on the static index.html so both surfaces stay in sync.
Edit this file and the Streamlit app picks up the changes automatically.
"""

from __future__ import annotations
from dataclasses import dataclass, field

# ── Identity ──────────────────────────────────────────────────────────────────
NAME = "Yaé Gaba, PhD"
TAGLINE = (
    "End-to-end data-science and machine-learning projects on real public data — "
    "predictive modeling, statistical inference, forecasting, optimization, and "
    "experimentation across healthcare, energy, finance, retail, and beyond."
)
EMAIL = "yaeulrich.gaba@gmail.com"
LINKEDIN = "https://linkedin.com/in/gabayae"
GITHUB = "https://github.com/gabayae"
SITE = "https://gabayae.github.io"
SCHOLAR = "https://scholar.google.com/citations?user=UTszjV4AAAAJ"
BOOK = "https://nostarch.com/shapeofdata"
LOCATION = "Cotonou, Benin"

# Absolute base for the published static site. Used by the Streamlit app so
# project / case-study / notebook links keep resolving when the app is served
# from <name>.streamlit.app (a different origin than GitHub Pages).
STATIC_BASE = "https://gabayae.github.io/data-portfolio/"

# ── Visual tokens (PasserellAI editorial palette) ─────────────────────────────
COLOR_BG = "#fafaf7"
COLOR_SURFACE = "#ffffff"
COLOR_INK = "#171717"
COLOR_MUTED = "#555555"
COLOR_BORDER = "#e4e1d8"
COLOR_PRIMARY = "#0f2a4a"
COLOR_ACCENT = "#c85c3c"
COLOR_ACCENT_SOFT = "#f4e4dd"

CATEGORY_COLORS = {
    "time-series":    ("#f4e4dd", "#b04b2e"),
    "regression":     ("#e3e8ef", "#0f2a4a"),
    "classification": ("#ece2ec", "#6e3a6e"),
    "survival":       ("#e6e0ec", "#594080"),
    "spatial":        ("#d8e9eb", "#2a6b78"),
    "optimization":   ("#d9e8df", "#2b6e4f"),
    "experimentation":("#f0e6c8", "#8a6f1a"),
}

# ── Headline stats ────────────────────────────────────────────────────────────
STATS = [
    ("6.2%",  "MAPE — PJM hourly load (GBM, vs SARIMA 14.5%)"),
    ("7 cm",  "RMSE — Lake Kariba lake-level (30 days)"),
    ("0.71",  "AUC — MTN Nigeria churn (XGBoost)"),
    ("+122%", "Coverage lift — Kenya mobile clinics (Q-learning vs manual)"),
]

# ── Project records ───────────────────────────────────────────────────────────
@dataclass
class Project:
    number: int
    title: str
    tagline: str
    metric: str
    categories: list[str]
    tech: list[str]
    dataset: str
    folder: str
    case_study: str | None = None  # relative URL of long-form case study, if any

PROJECTS: list[Project] = [
    Project(1,
        "Health Supply-Chain Demand Forecasting",
        "12-month horizon on real PEPFAR shipment records — Rwanda focus.",
        "SARIMA WAPE 0.94",
        ["time-series"],
        ["SARIMA", "UC state-space", "Holt-Winters", "GBM"],
        "USAID PEPFAR SCMS · 10,324 shipments",
        "01-demand-forecasting-rwanda",
    ),
    Project(2,
        "Hourly Load Forecasting — PJM",
        "State-space + Fourier exog vs SARIMA on 145k hours of PJME load.",
        "GBM MAPE 6.2% · UC PI 99%",
        ["time-series"],
        ["SARIMA", "UnobservedComponents", "Fourier exog", "GBM"],
        "PJM Hourly Consumption · 145k records",
        "02-electricity-load-forecasting-pjm",
        case_study="case-studies/pjm/",
    ),
    Project(3,
        "Insurance Claims Frequency & Severity",
        "Poisson / Gamma / Tweedie GLMs on freMTPL2 with GBM challenger.",
        "Tweedie Gini 0.310 · Lift 2.52",
        ["regression"],
        ["Poisson GLM", "Gamma GLM", "Tweedie", "XGBoost"],
        "freMTPL2 freq + sev · 678k policies",
        "03-insurance-claims-fremtpl2",
    ),
    Project(4,
        "Hierarchical Retail Demand — M5",
        "SARIMA + GBM with MinT-OLS to make item × store × week forecasts coherent.",
        "MinT-OLS reconciliation",
        ["time-series"],
        ["SARIMA", "GBM", "MinT-OLS", "RMSSE"],
        "M5 sample · 13 items × 10 stores × 275 weeks",
        "04-retail-demand-m5",
    ),
    Project(5,
        "Mobile-Clinic Scheduling — Kenya",
        "MDP + Q-learning vs capped LP baseline on real KMPDC + SHA data.",
        "Q-learning +122% vs manual",
        ["optimization"],
        ["MDP", "Q-learning", "Linear programming", "scipy.linprog"],
        "Kenya KMPDC + SHA · 7,876 facilities",
        "05-resource-allocation-kenya",
    ),
    Project(6,
        "River Flow Forecasting — Lake Kariba",
        "Daily lake level on real Zambezi reservoir data; turbine discharge as exog.",
        "GBM RMSE 7 cm · SARIMA PI 100%",
        ["time-series"],
        ["SARIMA", "State-space", "GBM exog"],
        "Lake Kariba reservoir · 1,155 daily obs",
        "06-river-flow-forecasting-kariba",
    ),
    Project(7,
        "Solar Forecasting — Nairobi",
        "Daily irradiance with weather covariates from NASA POWER API.",
        "GBM MAPE 9.4% · 10-yr daily",
        ["time-series"],
        ["SARIMA", "UnobservedComponents", "Fourier annual", "GBM weather exog"],
        "NASA POWER · 3,652 days, 6 vars",
        "07-solar-forecasting-nairobi",
    ),
    Project(8,
        "Customer Survival — MTN Nigeria",
        "Tenure-as-time, churn-as-event; KM, Cox PH, Weibull AFT, log-rank stratification.",
        "Cox PH + Weibull AFT",
        ["survival"],
        ["Kaplan-Meier", "Cox PH", "Weibull AFT", "Log-rank"],
        "MTN Nigeria · 974 customers",
        "08-customer-survival-mtn-tenure",
    ),
    Project(9,
        "Flight Demand & Price — Southern Africa",
        "Daily volume forecast on top route + GBM price predictor across all routes.",
        "SARIMA MAPE 2.0% · price MAE 410 ZAR",
        ["time-series"],
        ["SARIMA", "GBM", "Dynamic pricing"],
        "SA Flight Prices · 15,393 flights",
        "09-flight-demand-southern-africa",
    ),
    Project(10,
        "Property Valuation — Lagos",
        "Bedroom + property-type + neighborhood features on 9,607 Lagos sale listings.",
        "GBM R² 0.57 · OLS 0.51",
        ["regression"],
        ["OLS", "GBM", "Log target", "Feature engineering"],
        "Lagos Housing · 9,607 listings",
        "10-property-valuation-lagos",
    ),
    Project(11,
        "Geospatial Farm-Output Forecasting",
        "Predict farm sales from lat/lon + farm + climate features across multiple African countries.",
        "GBM R² 0.66 (vs OLS 0.31)",
        ["spatial", "regression"],
        ["Spatial features", "OLS", "GBM", "Multi-country"],
        "African Farm Households · 9,597 surveyed",
        "11-geospatial-farm-households",
    ),
    Project(12,
        "Churn Classification — MTN Nigeria",
        "XGBoost vs RF vs LogReg with calibration plot and retention-queue ranking.",
        "XGBoost AUC 0.71",
        ["classification"],
        ["Logistic", "Random Forest", "XGBoost", "Calibration"],
        "MTN Nigeria · 974 customers",
        "12-churn-prediction-mtn",
    ),
    Project(13,
        "A/B Test Framework — Marketing",
        "Welch t-tests + ANOVA + OLS adjustment + Bayesian posterior on a real 3-arm trial.",
        "ANOVA p < 1e-9 · Cohen's d 0.68",
        ["experimentation"],
        ["ANOVA", "Welch t-test", "Bonferroni", "Bayesian A/B"],
        "Fast-food A/B · 548 weekly obs · 3 arms",
        "13-ab-test-marketing",
    ),
]

CATEGORY_LABELS = {
    "all": "All",
    "time-series": "Time Series",
    "regression": "Regression / GLM",
    "classification": "Classification",
    "survival": "Survival",
    "spatial": "Spatial",
    "optimization": "Optimization",
    "experimentation": "Experimentation",
}

# ── Skills ────────────────────────────────────────────────────────────────────
TECHNIQUES = {
    "Time-series & forecasting": [
        ("SARIMA / ARIMA", [1, 2, 4, 6, 7, 9]),
        ("UnobservedComponents (state-space)", [1, 2, 6, 7]),
        ("Holt-Winters / ETS", [1]),
        ("Hierarchical reconciliation (MinT)", [4]),
        ("Rolling-origin backtest · PI calibration", [1, 2, 6, 7]),
    ],
    "GLMs & statistical modeling": [
        ("Poisson / Gamma / Tweedie GLM", [3]),
        ("Cox PH · Weibull AFT", [8]),
        ("OLS · log-target regression", [10, 11]),
        ("Logistic regression · L2", [12]),
        ("Gini · Lorenz · top-decile lift", [3]),
    ],
    "Machine learning": [
        ("Gradient-boosted trees", [2, 3, 6, 7, 10, 11, 12]),
        ("Random Forest", [12]),
        ("Lag · rolling · calendar feature engineering", [2, 6, 7]),
        ("Calibration · ROC / PR curves", [12]),
    ],
    "Optimization & experimentation": [
        ("Markov decision processes · Q-learning", [5]),
        ("Linear programming (scipy.linprog)", [5]),
        ("ANOVA · Welch t · Bonferroni", [13]),
        ("Bayesian A/B (posterior simulation)", [13]),
        ("Stratified analysis (Simpson guard)", [13]),
    ],
}

TOOLS = {
    "Languages & data": ["Python", "SQL", "pandas", "NumPy", "SciPy", "PostgreSQL"],
    "Modeling libraries": ["statsmodels", "scikit-learn", "XGBoost", "LightGBM", "lifelines"],
    "Engineering & viz": ["FastAPI", "Streamlit", "Docker", "Git", "Jupyter", "matplotlib", "seaborn", "LaTeX"],
}

# ── Process ───────────────────────────────────────────────────────────────────
PROCESS_STEPS = [
    "Business question",
    "Data & EDA",
    "Modeling",
    "Validation",
    "Deployment",
    "Business outcome",
]
