<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/fr/) · [Carnet](https://github.com/gabayae/data-portfolio/blob/main/11-geospatial-farm-households/notebook.ipynb)

---

# Prévision géospatiale de la production agricole — exploitations africaines

## Question métier

Étant donné la localisation d'une exploitation (lat/lon, district) et ses attributs de base, peut-on prédire son chiffre d'affaires annuel ? C'est l'analogue africain du projet de prévision géospatiale de Calgary — même boîte à outils de régression spatiale appliquée à la production agricole sur plusieurs pays africains.

Cas d'usage :
- Institutions de microfinance dimensionnant les prêts de campagne
- Fournisseurs d'intrants (engrais, semences) ciblant les zones sous-desservies
- Agences de vulgarisation agricole priorisant les visites de district

## Données

- **Source :** [Agricultural Survey of African Farm Households (Kaggle)](https://www.kaggle.com/datasets/crawford/agricultural-survey-of-african-farm-households) — l'enquête complète comporte 9 597 ménages agricoles sur plusieurs pays africains avec 1 754 attributs.
- **Sous-ensemble modélisé :** **931 lignes** après `dropna` sur `(lat, lon, farmsalev)`. Dans ce sous-ensemble, la colonne `district` se réduit à une seule valeur (« Unknown »), de sorte que l'OHE district du pipeline actuel ne porte aucun signal. Les features climatiques long terme sont majoritairement imputées à une médiane unique et contribuent peu.

Lancer `python download_data.py`.

## Cibles d'EDA

- Distribution géographique des 931 ménages modélisés
- Distribution de `farmsalev` (chiffre d'affaires annuel) sur le sous-ensemble modélisé
- Distribution des superficies et patterns de tenure

## Modélisation

| Famille | Modèle |
|---|---|
| Baseline linéaire | OLS sur log-chiffre-d'affaires avec lat/lon + features de taille |
| Baseline géo non-paramétrique | `KNeighborsRegressor(n_neighbors=10)` |
| Challenger non-linéaire | `GradientBoostingRegressor` avec lat/lon + features d'exploitation |

## Validation

- **Découpage aléatoire 80/20 (fuite) :** OLS R² 0,31 · KNN R² 0,57 · GBM R² 0,66. Les observations d'un même village partagent des `(lat, lon)` identiques ; le découpage aléatoire laisse le GBM mémoriser des tables de correspondance au niveau village. Conservé dans le carnet uniquement pour rendre la fuite visible.
- **`GroupKFold` spatial sur cellules 1° lat/lon, 5 folds (honnête) :** OLS R² **0,22 ± 0,38** · KNN R² **0,14 ± 0,44** · GBM R² **0,12 ± 0,34**. 35 cellules spatiales, médiane 27 obs/cellule. Le R² du GBM s'effondre de 0,66 à 0,12 — les +0,54 du découpage aléatoire étaient de la mémorisation, pas de la généralisation. Toutes les variances inter-fold sont très larges ; le signal honnête sur cellules spatiales inédites est faible.
- Métriques : R² sur log-chiffre-d'affaires (principale), MAE sur log, MAPE sur chiffre brut.

## Esquisse de déploiement

- Un service de triage microfinance nécessiterait une résolution par grappe plutôt que par ménage, et devrait être ré-entraîné à chaque nouvelle vague d'enquête.
- Tout déploiement nécessiterait un join sur l'identifiant de grappe à partir des données brutes d'enquête, pour que le GroupKFold corresponde au vrai plan d'échantillonnage plutôt qu'à une grille lat/lon 1° ad-hoc.

## Résultat métier

- Esquisse méthodologique de régression géospatiale sur données d'enquête ; les mises en garde ci-dessus (taille d'échantillon, fuite spatiale) doivent être respectées avant tout usage en souscription.
