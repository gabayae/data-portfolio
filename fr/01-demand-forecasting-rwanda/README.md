<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/fr/) · [Carnet](https://github.com/gabayae/data-portfolio/blob/main/01-demand-forecasting-rwanda/notebook.ipynb)

---

# Prévision de la demande — chaîne d'approvisionnement en santé du Rwanda

## Question métier

Peut-on prévoir la consommation à 3–6 mois de médicaments essentiels par district pour faire baisser **à la fois** les ruptures de stock et les sur-stocks, et permettre aux responsables logistiques de prendre des décisions de réapprovisionnement et de redistribution inter-districts avec des intervalles de prévision calibrés ?

## Données et EDA

- **Source (réelle) :** entrepôt national de la chaîne d'approvisionnement en santé (tables livraisons + dispensations). Aucun jeu de données entièrement public n'existe ; ce carnet génère des données mensuelles synthétiques mais réalistes (12 SKU × 10 districts × 60 mois). Remplacer `load_data()` par la requête SQL réelle au moment du branchement.
- **Cibles d'EDA :**
  - Saisonnalité annuelle (pics de paludisme autour des saisons des pluies)
  - Rupture structurelle pendant la COVID-19 (début 2020)
  - Demande intermittente pour les SKU à faible rotation (régime de Croston)
  - Reporting retardé / manquant des districts ruraux
  - Tendance (croissance démographique, expansions de programmes)

## Modélisation

| Famille | Modèles |
|---|---|
| Séries temporelles classiques | SARIMA, lissage exponentiel (ETS) |
| Espace d'états | UnobservedComponents (tendance + saisonnier + AR) |
| ML pour la prévision | Régresseur gradient-boosté avec features lag/rolling/calendaire |
| Demande intermittente | Méthode de Croston pour les SKU à faible rotation |

## Validation

- Backtest à origine glissante, horizon 12 mois, ré-ajustement mensuel
- Métriques : **MAPE**, **WAPE**, biais, couverture des intervalles de prévision
- Évaluation par niveau : district × catégorie de SKU
- Baselines : naïf-saisonnier, ETS

## Déploiement

- Tableau de bord Streamlit avec backend FastAPI
- Ré-entraînement mensuel via pipeline Python ordonnancé tirant depuis l'entrepôt
- Prévisions + intervalles écrits dans une table Postgres lue par le tableau de bord

## Résultat métier

- Visibilité à 3 mois avec intervalles calibrés pour les responsables logistiques
- Quantités de réapprovisionnement et décisions de redistribution inter-districts éclairées par les prévisions
- Réunion S&OP mensuelle raccourcie (chiffres validés au lieu de chiffres débattus)
