<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/fr/) · [Carnet](https://github.com/gabayae/data-portfolio/blob/main/06-river-flow-forecasting-kariba/notebook.ipynb) · [Étude de cas →](https://gabayae.github.io/data-portfolio/fr/case-studies/kariba/)

---

# Prévision du débit fluvial — lac Kariba (bassin du Zambèze)

## Question métier

Peut-on prévoir le niveau journalier du lac Kariba et le débit total sortant pour que la Zambezi River Authority et les centrales hydroélectriques de Kariba (Kariba Sud, Kariba Nord) puissent planifier les programmes de turbinage et équilibrer le stockage entre la Zambie et le Zimbabwe malgré des apports incertains ?

Le lac Kariba est le plus grand réservoir artificiel au monde par volume ; son niveau pilote ~1 800 MW de production régionale. Une baisse de niveau d'1 m peut coûter des centaines de GWh de production.

## Données

- **Source :** [Lake Kariba Reservoir Data — Kaggle (`marbin/lake-kariba-reservoir-data`)](https://www.kaggle.com/datasets/marbin/lake-kariba-reservoir-data)
- **Période :** 1er janvier 2020 → 28 février 2023 (1 155 observations journalières)
- **Variables :** `lake_level` (m), `usable_storage`, `live_storage`, `turbine_discharge`, `spillage`, `total_outflow` (m³/s)
- **Licence :** données ouvertes déclarées par l'éditeur sur Kaggle

Lancer `python download_data.py` pour télécharger (nécessite Kaggle CLI configuré).

## Cibles d'EDA

- Saisonnalité annuelle (saison des pluies novembre–avril en Afrique australe)
- Cycles de baisse / récupération à long terme du niveau du lac
- Relations multivariées : lake_level vs storage vs outflow
- Événements de déversement (presque toujours nuls — régime extrême de hautes eaux)

## Modélisation

| Famille | Modèle |
|---|---|
| Séries temporelles classiques | SARIMA(1,1,1)(1,1,1)₇ sur niveau journalier |
| Espace d'états | `UnobservedComponents` (tendance locale-linéaire + exog. Fourier annuelles) |
| Challenger ML (équitable) | `GradientBoostingRegressor`, features cible-seules, **récursif 30 pas** |
| Challenger ML (contexte) | GBM avec `turbine_discharge` + `total_outflow` laggés + niveau de la veille révélé, un pas d'avance |

## Validation

- Fenêtre de 30 jours mise de côté, deux variantes GBM comparées côte à côte.
- Métriques : MAPE, RMSE en mètres, couverture IP 95 % avec IC Clopper-Pearson.

**Chiffres en tête :**

| Modèle | MAPE | RMSE (m) | Couverture IP 95 % |
|---|---|---|---|
| **SARIMA (multi-pas)** | **0,027 %** | **0,184** | 30/30 (CP [0,88 ; 1,00]) |
| UC espace d'états (multi-pas) | 0,079 % | 0,418 | 30/30 (CP [0,88 ; 1,00]) |
| GBM récursif 30 pas (équitable) | 0,085 % | 0,508 | — |
| Naïf-dernier | 0,085 % | 0,501 | — |
| GBM à un pas d'avance avec exog (contexte) | 0,013 % | 0,069 | — |

SARIMA gagne la comparaison à armes égales à **18 cm de RMSE** sur l'horizon multi-pas 30 jours, et son IP 95 % tient (demi-largeur moyenne ≈ 56 cm, 30/30 avec IC CP [0,88 ; 1,00]). Faire tourner le GBM en vrai mode récursif le fait chuter à 51 cm de RMSE, essentiellement à égalité avec le naïf-dernier, car `turbine_discharge` et `total_outflow` sont des *décisions* opérateur — pas des covariables prévisibles à 30 jours. Le « RMSE 7 cm du GBM » précédemment en titre était une évaluation à un pas d'avance avec le débit du jour précédent révélé ; il reste dans le tableau comme contexte, pas comme chiffre de planification.

## Esquisse de déploiement

- Pour une planification 30 jours, SARIMA est ce qui part en prod : IP 95 % calibré, et le plus bas RMSE multi-pas de la comparaison.
- Un service temps-réel à un pas d'avance (rafraîchissement J+1 avec débit de la veille connu) pourrait utiliser la variante GBM-avec-exog pour une précision ponctuelle sensiblement plus serrée ; les cas d'usage sont différents.

## Résultat métier

- Visibilité à 30 jours sur le niveau du lac avec IP 95 % calibré de SARIMA — appuie la planification de dispatch de turbines par la Zambezi River Authority lorsque le débit est une variable de *décision*.
- La variante GBM-avec-exog est un outil opérationnel à 1 jour, pas de planification à 30 jours. Le carnet distingue maintenant les deux régimes.

**Prochaines itérations :** prévisions de pluie CHIRPS / NASA POWER comme *apports pluviométriques exogènes* (connus au moment de la prévision, contrairement au débit futur) ; espace d'états à régimes commutés pour sécheresse vs crue ; GBM quantile pour bandes de risque probabilistes autour des seuils de turbinage.
