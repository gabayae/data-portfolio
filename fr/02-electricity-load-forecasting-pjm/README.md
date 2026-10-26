<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/fr/) · [Carnet](https://github.com/gabayae/data-portfolio/blob/main/02-electricity-load-forecasting-pjm/notebook.ipynb) · [Étude de cas →](https://gabayae.github.io/data-portfolio/fr/case-studies/pjm/)

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
| Baseline classique | SARIMA sur la charge agrégée journalière |
| Espace d'états | `UnobservedComponents` avec niveau variant dans le temps + termes de Fourier hebdomadaires/journaliers + régresseurs exogènes |
| Challenger ML | GBM (`GradientBoostingRegressor`) avec features lag, rolling et calendaires |

## Validation

- Backtest à holdout de 60 jours en fin de série.
- Métriques : MAPE, RMSE, couverture des IP 95 % avec IC Clopper-Pearson.

**Prévisions multi-pas 60 jours, à armes égales :**

| Modèle | MAPE | RMSE (MW) | Couverture IP 95 % |
|---|---|---|---|
| **GBM récursif 60 pas** | **9,0 %** | 4 414 | — |
| SARIMA (multi-pas) | 14,5 % | 6 676 | 54/60 (IC CP [0,79 ; 0,96]) |
| UC espace d'états (multi-pas) | 19,3 % | 8 295 | 60/60 (IC CP [0,94 ; 1,00]) |

Le GBM bat SARIMA de 38 % de MAPE une fois les deux évalués comme prévisions multi-pas 60 jours. La variante UC a *perdu* face à SARIMA sur ce run (−33 % de gain). Le GBM à un pas d'avance (MAPE 6,2 %) est rapporté dans le carnet comme contexte, étiqueté comme tel — il suppose la charge de la veille révélée, ce qui n'est pas une prévision 60 jours.

## Esquisse de déploiement

- Le GBM récursif est le choix opérationnel sur ce run ; SARIMA offre le seul IP 95 % bien calibré (54/60 dans la bande).
- Ré-entraînement planifié + artefact picklé ; pas un système de production — le carnet s'arrête à la prévision hors-ligne sur données PJME réelles.

## Résultat métier

- Prévision de charge à J+1 sur données PJME réelles ; le GBM avec évaluation récursive multi-pas est le leader honnête en erreur ponctuelle.
- La couverture IP de SARIMA (54/60 à nominal 95 %, compatible avec toute vraie couverture ≥ 79 %) reste le choix opérationnel pour les décisions achats/hedging où la calibration d'intervalle compte plus que l'erreur ponctuelle.
