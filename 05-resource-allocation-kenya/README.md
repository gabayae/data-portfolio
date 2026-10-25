<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/) · [Notebook](https://github.com/gabayae/data-portfolio/blob/main/05-resource-allocation-kenya/notebook.ipynb) · [Case study →](https://gabayae.github.io/data-portfolio/case-studies/kenya/)

---

# Stochastic Optimization for Resource Allocation — Kenya Health Facilities

## Business question

Can mobile clinics be scheduled across underserved counties to maximize population coverage under uncertain demand, road conditions, and staff availability?

## Data & EDA

- **Source:** facility list, catchment populations, historical visit counts, road network, weather/seasonality. Public proxies: [Kenya Open Data](https://www.opendata.go.ke/). The notebook generates a synthetic 8-facility county scenario by default.
- **EDA targets:**
  - Seasonal demand swings
  - Geographic clusters of under-coverage
  - High variance in daily utilization

## Modeling

| Component | Choice |
|---|---|
| Decision process | Markov Decision Process (state = `(location, day_bucket)`; action = next facility; reward = patients served − travel cost − recent-visit penalty) |
| Solver | Tabular Q-learning (|S|·|A| = 84·12) |
| Static baseline | Linear-programming (LP) max-coverage facility-location, with an equity cap on per-county visits |
| Manual baseline | Round-robin schedule |

## Validation

- Simulated rollouts against the manual schedule and the capped LP baseline
- Metrics: patients served, travel distance (km), coverage of low-demand counties
- Policies are not budget-matched — manual round-robin incurs 87 km/day of mandatory travel; Q-learning is allowed to not travel at all. See the case study for the honest comparison.

## Deployment sketch

- Streamlit interface for district health officers — the capped LP output is the deployable candidate; Q-learning's greedy policy collapsed to a single-county visit pattern on this run and should not be deployed as-is.
- Re-train monthly as visit data accumulates.

## Business outcome

- The honest headline is the capped LP's **+39% coverage** over the manual schedule, achieved with an explicit equity constraint that forces visits to low-demand counties.
- Q-learning's reported **+122%** vs manual comes from a degenerate greedy policy (`total_travel_km = 0`, `low_demand_visits = 0`); see the case-study callout. Reward-shaping is doing most of the work during training and does not carry over to evaluation.
- Headline lesson: *the constraint formulation matters more than the algorithm.* On this problem a capped LP with equity is more defensible than a hard-to-stabilize RL policy.
