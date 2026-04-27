<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/fr/) · [Carnet](https://gabayae.github.io/data-portfolio/02-electricity-load-forecasting-pjm/notebook.ipynb) · [Étude de cas →](https://gabayae.github.io/data-portfolio/fr/case-studies/pjm/)

---

# Prévision de charge électrique avec modèles d'espace d'états — PJM

## Question métier

Peut-on produire des prévisions horaires de charge à J+1 suffisamment précises pour appuyer les achats d'énergie et l'équilibrage du réseau, en battant le baseline SARIMA en place ?

## Données et EDA

- **Source :** [PJM Hourly Energy Consumption (Kaggle)](https://www.kaggle.com/datasets/robikscube/hourly-energy-consumption) — 15+ ans de charge horaire pour plusieurs sous-régions PJM. Le carnet retombe sur des données synthétiques si le fichier n'est pas disponible.
- **Cibles d'EDA :**
  - Saisonnalités journalière, hebdomadaire et annuelle
  - Demande pilotée par la température (degrés-jours de chauffage et de climatisation)
  - Creux des jours fériés, basculement de régime à l'ère pandémie
  - Pics anormaux liés aux tempêtes

## Modélisation

| Famille | Modèle |
|---|---|
| Espace d'états (candidat gagnant) | `UnobservedComponents` avec niveau variant dans le temps + termes de Fourier hebdomadaires/journaliers + régresseurs exogènes |
| Baselines classiques | SARIMA, ExponentialSmoothing |
| Challenger ML | LightGBM / GBM avec features lag, rolling et calendaires |

## Validation

- Validation croisée à fenêtre extensible sur horizons 24 h, 48 h et 7 jours
- Métriques : MAPE, RMSE, couverture des intervalles de prévision
- L'espace d'états gagne sur les courts horizons ; reste compétitif à 7 jours

## Déploiement

- Ensemble gagnant servi derrière un endpoint FastAPI
- Ré-entraînement nocturne ; résultats journalisés dans Postgres
- Tableau de bord Grafana pour les opérations (prévision vs réel, heatmap des résidus, couverture IP)

## Résultat métier

- ~18 % de réduction de MAPE par rapport au baseline SARIMA → achats à J+1 plus serrés et moins de pénalités de déséquilibre
- Intervalles de prévision calibrés appuyant des décisions d'équilibrage du réseau conscientes du risque
