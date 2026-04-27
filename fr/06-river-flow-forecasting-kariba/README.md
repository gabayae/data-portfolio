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
| Séries temporelles classiques | SARIMA sur niveau journalier |
| Espace d'états | UnobservedComponents (tendance locale-linéaire + saisonnalité annuelle harmonique) |
| ML pour la prévision | Régresseur gradient-boosté avec features lag/rolling/exogènes (débit turbiné comme covariable) |

## Validation

- Backtest à origine glissante, horizon 30 jours
- Métriques : MAPE, RMSE, couverture des intervalles de prévision
- Baselines : naïf (dernière observation), naïf-saisonnier

## Déploiement

- FastAPI `/forecast` retournant niveau-de-lac moyen + IP 95 % pour les 30 prochains jours
- Tableau de bord Streamlit pour la Zambezi River Authority — rafraîchissement journalier, scénarios pessimistes, panneau d'impact production
- Ré-entraînement hebdomadaire ; alertes si le RMSE glissant dépasse le seuil opérationnel

## Résultat métier

- Visibilité à 30 jours sur le niveau du lac avec intervalles calibrés — éclaire le dispatch des turbines et les accords de stockage entre pays
- Quantifie à l'avance le risque opérationnel des scénarios à faibles apports
