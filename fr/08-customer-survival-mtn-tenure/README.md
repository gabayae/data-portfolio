<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/fr/) · [Carnet](https://gabayae.github.io/data-portfolio/08-customer-survival-mtn-tenure/notebook.ipynb)

---

# Analyse de survie client — Télécoms MTN Nigeria

## Question métier

Au-delà d'un binaire « va-t-il churner ? », comment le risque de churn *évolue-t-il avec l'ancienneté* ? L'analyse de survie permet :
- D'estimer la fonction de survie S(t) — probabilité qu'un client soit toujours actif au mois t
- D'identifier les fenêtres d'ancienneté à fort risque (par ex. mois 1–6 après l'onboarding) pour de la rétention ciblée
- De quantifier comment des covariables (forfait, âge, satisfaction) déplacent le hasard

## Données

- **Source :** [MTN Nigeria Customer Churn (Kaggle)](https://www.kaggle.com/datasets/oluwademiladeadeniyi/mtn-nigeria-customer-churn) — 974 clients, 17 attributs dont l'ancienneté (mois), le forfait, la satisfaction, l'issue de churn.
- **Cadrage de survie :**
  - `duration` = `Customer Tenure in months`
  - `event` = 1 si `Customer Churn Status == 'Yes'`, sinon 0 (censuré à droite, toujours actif)

Lancer `python download_data.py` pour récupérer les données (Kaggle CLI requis).

## Cibles d'EDA

- Médiane du time-to-churn vs censure
- Différences de hasard par forfait, tranche d'âge, satisfaction
- Raisons du churn (catégorisation de texte libre)

## Modélisation

- **Kaplan–Meier** : courbes de survie stratifiées par forfait et satisfaction
- **Cox à hasards proportionnels** avec rapports de hasard ajustés sur covariables
- **Weibull AFT** pour une interprétabilité directe de la durée de vie attendue

## Validation

- Indice de concordance (C-index) sur un test mis de côté à 20 %
- Tests log-rank entre strates

## Déploiement

- API `POST /customer-survival` retournant la durée résiduelle attendue + bande de risque de churn pour les attributs d'un client
- Tableau de bord de rétention classant les clients par probabilité de churn à 90 jours

## Résultat métier

- Le ciblage de rétention conscient de l'ancienneté bat le « tout ce qui est classé risqué »
- Les rapports de hasard pilotent les décisions produit/tarification (par ex. le forfait X retient-il plus longtemps que Y, à âge contrôlé ?)
- Le même pipeline s'applique à toute activité par abonnement avec signal ancienneté + churn
