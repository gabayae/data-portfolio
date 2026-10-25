<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/) · [Notebook](https://github.com/gabayae/data-portfolio/blob/main/13-ab-test-marketing/notebook.ipynb)

---

# A/B Test Framework — Multi-arm Marketing Promotion

## Business question

Which of three promotion strategies (Promotion 1 vs. 2 vs. 3) drives the highest sales? A real fast-food chain ran them across stores; we apply a rigorous A/B/n testing framework to draw correct conclusions and recommend the rollout.

The toolkit demonstrated here applies directly to African retail or telecom marketing experiments (e.g., MTN Nigeria push campaigns, Jumia promo strategies).

## Data

- **Source:** [Fast Food Marketing Campaign A/B Test (Kaggle)](https://www.kaggle.com/datasets/chebotinaa/fast-food-marketing-campaign-ab-test) — 548 weekly sales observations across 137 locations × 4 weeks × 3 promotions, with market size (Small/Medium/Large) and store age.

Run `python download_data.py`.

## EDA targets

- Sales distribution per promotion arm
- Market size as a stratifier
- Store age effect

## Statistical analyses

| Test | Use |
|---|---|
| Welch's two-sample t-test with Bonferroni | Pairwise promotion comparisons |
| One-way ANOVA | Joint test across all three promotions |
| OLS with covariate adjustment + cluster-robust SEs on `LocationID` | Honest inference under store-level clustering |
| Formal interaction test `C(Promotion) × C(MarketSize)` | Simpson's-paradox guard with p-value |
| Flat-prior Normal-Normal posterior on each arm's mean | `P(a > b)` as a direct probability (acknowledging the flat improper prior, not a true informative Bayesian analysis) |

## Validation

- 548 observations are **137 locations × 4 weeks** — not independent. Naive OLS SEs are too narrow; the notebook reports both naive and cluster-robust-on-`LocationID` SEs so the inflation is visible.
- Multiple-comparison correction (Bonferroni on 3 pairwise t-tests).
- Effect size: Cohen's d (P1-vs-P2 d = 0.68 moderate-large; P1-vs-P3 d = 0.16 negligible).
- Interaction F = 4.93, p = 0.0007 — the Simpson's-paradox check is statistically real, not just visual.

## Deployment sketch

- Dashboard summarising per-arm sales + 95% CI (clustered) + lift estimate vs. the reference arm.
- Decision rule: launch winning promotion if (a) ANOVA p < 0.01 AND (b) clustered pairwise p < 0.01 vs. all alternatives AND (c) Cohen's d > 0.3 AND (d) winner holds within every market-size stratum.

## Business outcome

- Statistically defensible promotion-rollout decision with clustered inference.
- Formal interaction test confirms the market-size × promotion interaction (visible in the stratified mean table).
- The flat-prior "Bayesian" layer is a convenience read, not a true informative-prior analysis; a proper hierarchical model with store random intercepts would further widen the posteriors.
