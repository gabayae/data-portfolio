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

- Découpage stratifié 80/20 (taux de base test = 29 %).
- Métriques : ROC-AUC, PR-AUC, F1, exactitude équilibrée, **Precision@k et Lift@k** pour le cadrage file-de-rétention.
- Tracé de calibration avec **IC Wilson 95 % par bin** pour rendre visible l'incertitude des ~19 obs/bin plutôt que la lisser.

**Chiffres en tête (test) :**

| Modèle | ROC-AUC | PR-AUC | P@50 | Lift@50 | P@100 | Lift@100 |
|---|---|---|---|---|---|---|
| XGBoost | 0,71 | 0,51 | **0,52** | **1,78×** | 0,40 | 1,37× |
| Random Forest | 0,59 | 0,36 | 0,34 | 1,16× | 0,38 | 1,30× |
| LogReg | 0,48 | 0,27 | 0,20 | 0,68× | 0,30 | 1,03× |

Seule la file top-50 de XGBoost porte un lift significatif (1,78× vs aléatoire). La top-50 de la LogReg est *pire* qu'aléatoire, signe que le scoring linéaire capte de l'anti-signal sur ces données (quasi-aléatoires). Voir la note dataset en haut pour le contexte.

## Esquisse de déploiement

- File de rétention classée par score XGBoost ; auditer Lift@k mensuellement sur le holdout pour détecter la dérive.
- Pas déployable sur le dataset actuel — la note dataset en haut s'applique. Sur un vrai benchmark churn (IBM Watson Telco) le même code produit des features interprétables et un lift top-k défendable.

## Résultat métier

- Dépenses de rétention allouées là où le lift prédit est le plus élevé ; le top-k est la métrique qui correspond au cas d'usage de ciblage de campagne.
- Jumeau du projet 08 (analyse de survie sur les mêmes données) — deux lentilles analytiques, toutes deux contraintes par le même problème de provenance de données.
- Le même pipeline s'applique à toute activité par abonnement
