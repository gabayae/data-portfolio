<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/fr/) · [Carnet](https://gabayae.github.io/data-portfolio/11-geospatial-farm-households/notebook.ipynb)

---

# Prévision géospatiale de la production agricole — exploitations africaines

## Question métier

Étant donné la localisation d'une exploitation (lat/lon, district) et ses attributs de base, peut-on prédire son chiffre d'affaires annuel ? C'est l'analogue africain du projet de prévision géospatiale de Calgary — même boîte à outils de régression spatiale appliquée à la production agricole sur plusieurs pays africains.

Cas d'usage :
- Institutions de microfinance dimensionnant les prêts de campagne
- Fournisseurs d'intrants (engrais, semences) ciblant les zones sous-desservies
- Agences de vulgarisation agricole priorisant les visites de district

## Données

- **Source :** [Agricultural Survey of African Farm Households (Kaggle)](https://www.kaggle.com/datasets/crawford/agricultural-survey-of-african-farm-households) — 9 597 ménages agricoles enquêtés à travers plusieurs pays africains avec 1 754 attributs dont lat/lon, district, composition du ménage, taille de l'exploitation, exposition climatique et chiffre d'affaires agricole.

Lancer `python download_data.py`.

## Cibles d'EDA

- Distribution géographique des ménages enquêtés
- Distribution au niveau district de `farmsalev` (chiffre d'affaires annuel agricole)
- Distribution des superficies et patterns de tenure
- Features d'exposition climatique (variations long terme de température/pluviométrie)

## Modélisation

| Famille | Modèle |
|---|---|
| Baseline linéaire | OLS sur log-chiffre-d'affaires avec district + features de taille |
| GBM spatial | GradientBoostingRegressor avec lat/lon + features d'exploitation |
| GBM géographique | LightGBM/GBM avec district en one-hot + features spatiales |

## Validation

- Découpage aléatoire 80/20 ; vérification de bon sens sur district mis de côté
- Métriques : R² sur log-chiffre-d'affaires, MAPE sur chiffre brut

## Déploiement

- API `POST /farm-output-prediction` retournant chiffre attendu + intervalle pour des attributs d'exploitation + coordonnées
- Tableau de bord spatial pour le triage des dossiers de prêt en microfinance

## Résultat métier

- Décisions de souscription et de ciblage terrain appuyées par des données, pas par l'intuition
- Une heatmap spatiale fait remonter les districts sous-desservis pour les fournisseurs d'intrants
- S'adapte à toute donnée d'enquête agricole avec colonnes géo + résultat
