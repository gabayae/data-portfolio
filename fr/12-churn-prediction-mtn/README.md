<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/fr/) · [Carnet](https://github.com/gabayae/data-portfolio/blob/main/12-churn-prediction-mtn/notebook.ipynb)

---

# Prédiction de churn — Télécoms MTN Nigeria

> **Note sur les données.** Ce snapshot Kaggle (974 lignes clients MTN Nigeria) est approximativement uniforme aléatoire sur les covariables testées — voir le carnet jumeau `08-customer-survival-mtn-tenure/README.md` pour les détails. L'AUC de la logistique et le F1 du RF s'effondrent ; l'AUC XGBoost = 0,71 reflète des interactions non linéaires dans des one-hots à grande cardinalité, pas un signal interprétable substantivement. **Ce carnet est une démonstration pédagogique de la classification binaire du churn** — régression logistique, random forest, XGBoost, diagnostics ROC / PR / calibration, file de rétention. Pour un vrai benchmark : IBM Watson Telco Customer Churn (7 043 clients).

## Question métier

Quels clients ont le plus de chance de churner au prochain trimestre, et quelles features pilotent leur risque ? Un classifieur binaire ordonne les clients par probabilité de churn pour que les campagnes de rétention ciblent le segment à plus haut risque.

(Compagnon du projet 08, qui modélise les mêmes données comme un problème de survie — mêmes données, deux angles analytiques, tous deux utiles.)

## Données

- **Source :** [MTN Nigeria Customer Churn (Kaggle)](https://www.kaggle.com/datasets/oluwademiladeadeniyi/mtn-nigeria-customer-churn) — 974 clients, 17 features (âge, État, forfait, satisfaction, ancienneté, revenu, usage data, label de churn).

Lancer `python download_data.py`.

## Cibles d'EDA

- Équilibre des classes (~29 % de churn)
- Signaux de hasard univariés : faible satisfaction, faible ancienneté, type de forfait
- Différences au niveau État

## Modélisation

| Famille | Modèle |
|---|---|
| Linéaire | Régression logistique avec pénalité L2 (baseline interprétable) |
| Arbres | Random Forest, Gradient Boosting (XGBoost) |

## Validation

- Découpage stratifié 80/20
- Métriques : ROC-AUC, PR-AUC, F1, exactitude équilibrée
- Tracé de calibration pour le meilleur modèle

## Déploiement

- API `POST /churn-score` retournant probabilité + bande de décile + top contributions de features style SHAP
- File de rétention priorisée par probabilité de churn × revenu

## Résultat métier

- Dépenses de rétention allouées là où le ROI est le plus élevé (clients à forte probabilité de churn × fort revenu)
- Les drivers (par ex. note de satisfaction, type de forfait) alimentent la roadmap produit/tarification
- Le même pipeline s'applique à toute activité par abonnement
