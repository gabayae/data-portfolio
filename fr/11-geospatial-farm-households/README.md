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
| GBM spatial | `GradientBoostingRegressor` avec lat/lon + features d'exploitation |

## Validation

- **Limitation connue (carnet actuel) :** un découpage aléatoire 80/20 est utilisé, mais les observations d'un même village partagent des `(lat, lon)` identiques et se retrouvent dispersées entre train et test — le GBM mémorise des tables de correspondance lat/lon. Le R²=0,66 reporté sous ce découpage surévalue la généralisation ; la comparaison honnête exige un `GroupKFold` sur lat/lon quantifiées ou un identifiant de grappe. Correctif en attente.
- Métriques : R² sur log-chiffre-d'affaires, MAPE sur chiffre brut

## Esquisse de déploiement

- Un service de triage microfinance nécessiterait une résolution par grappe plutôt que par ménage, et devrait être ré-entraîné à chaque nouvelle vague d'enquête.
- Pas un système de production — le carnet s'arrête à la modélisation hors-ligne.

## Résultat métier

- Esquisse méthodologique de régression géospatiale sur données d'enquête ; les mises en garde ci-dessus (taille d'échantillon, fuite spatiale) doivent être respectées avant tout usage en souscription.
