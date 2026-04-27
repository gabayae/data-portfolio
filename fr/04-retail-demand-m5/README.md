<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/fr/) · [Carnet](https://gabayae.github.io/data-portfolio/04-retail-demand-m5/notebook.ipynb)

---

# Prévision hiérarchique de la demande retail — M5

## Question métier

Produire des prévisions cohérentes SKU × magasin × semaine — la prévision d'une catégorie doit égaler la somme de ses SKU — pour planifier le réapprovisionnement en rayon et les achats de département à partir des mêmes chiffres.

## Données et EDA

- **Source :** [M5 Forecasting Accuracy (Kaggle)](https://www.kaggle.com/competitions/m5-forecasting-accuracy) — ventes journalières Walmart pour ~30 000 SKU dans 10 magasins de 3 États, avec calendrier, prix et événements SNAP.
- **Cibles d'EDA :**
  - Forte intermittence (beaucoup de jours à zéro vente par SKU)
  - Sensibilité prix/promotion
  - Effets jours fériés (Super Bowl, Noël, Pâques)
  - Pics de demande pilotés par les événements SNAP
  - Hiérarchie : SKU → catégorie → département → magasin → État

## Modélisation

| Niveau | Approche |
|---|---|
| Agrégat (État, département) | SARIMA / Prophet / ETS |
| Base (SKU × magasin) | LightGBM avec features riches lag, rolling, prix, calendrier |
| Réconciliation | MinT (trace minimale) — combinaison optimale à travers la hiérarchie |

## Validation

- RMSSE pondéré à origine glissante selon le protocole M5
- Évaluation par niveau : État, magasin, département, catégorie, SKU
- Les prévisions réconciliées doivent satisfaire les contraintes d'agrégation

## Déploiement

- Pipeline batch Python/PySpark produisant un drop hebdomadaire de prévisions
- Prévisions consommées par les workflows de réapprovisionnement et d'achat
- Chiffres cohérents partagés entre les équipes merchandising et planification

## Résultat métier

- Prévisions multi-niveaux qui alignent les attentes SKU bottom-up avec les plans de catégorie top-down
- Moins de travail de réconciliation entre les équipes merchandising et planification
