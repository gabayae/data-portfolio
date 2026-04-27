<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/fr/) · [Carnet](https://github.com/gabayae/data-portfolio/blob/main/03-insurance-claims-fremtpl2/notebook.ipynb) · [Étude de cas →](https://gabayae.github.io/data-portfolio/fr/case-studies/fremtpl2/)

---

# Sinistres : fréquence et gravité — freMTPL2

## Question métier

Peut-on produire des estimations de sinistres attendus au niveau de la police qui battent le GLM en place, tout en restant assez explicables pour une revue actuarielle et des décisions de tarification par tranche ?

## Données et EDA

- **Source :** [freMTPL2 / French Motor Third-Party Liability (Kaggle)](https://www.kaggle.com/datasets/floser/french-motor-claims-datasets-fremtpl2freq)
- **Volume :** ~680 000 polices avec exposition, âge du conducteur, véhicule, région et nombres/montants de sinistres.
- **Cibles d'EDA :**
  - Sur-dispersion de la fréquence de sinistres (variance > moyenne → alternative binomiale négative)
  - Asymétrie marquée à droite sur la gravité (longue queue → log/Gamma)
  - Interactions région × classe de véhicule
  - Exposition en offset (sinistres par police-année)

## Modélisation

| Cible | Modèle |
|---|---|
| Fréquence | GLM Poisson (lien log, exposition en offset) + alternative binomiale négative |
| Gravité | GLM Gamma sur sinistres positifs |
| Prime pure (unifiée) | GLM Tweedie / Poisson composé |
| Challenger ML | XGBoost avec objectifs Poisson et Gamma |

## Validation

- Validation croisée 5-folds sur déviance normalisée et Gini
- Tracés de fiabilité pour la calibration
- Courbes de Lorenz et lift du décile supérieur pour le pouvoir de segmentation
- Comparaison directe GLM vs Tweedie vs XGBoost

## Déploiement

- Artefacts du modèle (coefficients, ensembles d'arbres) exportés comme fonction de scoring pour le moteur tarifaire
- Note actuarielle avec graphiques de dépendance partielle et tables de sensibilité pour le comité de revue

## Résultat métier

- Lift mesurable en segmentation tout en préservant l'explicabilité
- Recommandations de réserves et ajustements tarifaires par tranche livrés comme insights actionnables pour la souscription
