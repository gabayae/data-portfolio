<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/fr/) · [Carnet](https://github.com/gabayae/data-portfolio/blob/main/02-electricity-load-forecasting-pjm/notebook.ipynb) · [Étude de cas →](https://gabayae.github.io/data-portfolio/fr/case-studies/pjm/)

---

# Prévision de charge électrique avec modèles d'espace d'états — PJM

## Question métier

Peut-on produire des prévisions horaires de charge à J+1 suffisamment précises pour appuyer les achats d'énergie et l'équilibrage du réseau, en battant le baseline SARIMA en place ?

## Données et EDA

- **Source :** [PJM Hourly Energy Consumption (Kaggle)](https://www.kaggle.com/datasets/robikscube/hourly-energy-consumption) — 15+ ans de charge horaire pour plusieurs sous-régions PJM. Le carnet retombe sur des données synthétiques si le fichier n'est pas disponible.
- **Cibles d'EDA :**
  - Saisonnalités journalière, hebdomadaire et annuelle
  - Demande pilotée par la température (degrés-jours de chauffage et de climatisation)
  - Creux des jours fériés, basculement de régime à l'ère pandémie
  - Pics anormaux liés aux tempêtes

## Modélisation

| Famille | Modèle |
|---|---|
| Baseline classique | SARIMA sur la charge agrégée journalière |
| Espace d'états | `UnobservedComponents` avec niveau variant dans le temps + termes de Fourier hebdomadaires/journaliers + régresseurs exogènes |
| Challenger ML | GBM (`GradientBoostingRegressor`) avec features lag, rolling et calendaires |

## Validation

- Backtest à holdout de 60 jours en fin de série
- Métriques : MAPE, RMSE, couverture des intervalles de prévision à 95 %
- MAPE SARIMA 14,5 %, MAPE UC 19,3 %, MAPE GBM 6,2 % — mais le chiffre GBM est une évaluation à un pas d'avance avec la charge réelle de la veille révélée. Pas directement comparable aux prévisions multi-pas SARIMA / UC. Voir l'étude de cas pour la discussion complète.
- Couverture empirique des IP 95 % du modèle UC : 60/60 (IC Clopper-Pearson à 95 % [0,94 ; 1,00] — l'échantillon est trop petit pour distinguer 95 % de 99 %).

## Esquisse de déploiement

- Candidat gagnant (SARIMA journalier à ce périmètre) pourrait être servi derrière un ré-entraînement planifié + artefact picklé.
- Pas un système de production — le carnet s'arrête à la prévision hors-ligne sur données PJME réelles.

## Résultat métier

- Prévision de charge à J+1 sur données PJME réelles ; SARIMA est le choix opérationnel (baseline multi-pas honnête) devant la variante espace d'états UC sur ce run.
- L'écart d'erreur ponctuelle entre SARIMA (14,5 %) et GBM (6,2 %, à un pas d'avance) est largement un artefact du protocole de comparaison — une vraie évaluation du GBM en mode récursif est la prochaine étape naturelle avant toute revendication côté achats.
