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
| Fréquence | GLM Poisson (lien log, exposition en offset) |
| Gravité | GLM Gamma sur sinistres positifs |
| Prime pure (unifiée) | GLM Tweedie / Poisson composé, `var_power = 1,5` avec scan de sensibilité 1,3-1,7 |
| Challenger ML | `GradientBoostingRegressor` avec décomposition Poisson-fréquence × log1p-gravité et **lissage de Duan** sur la rétro-transformation |

## Validation

- Découpage déterministe 80/20 unique ; **la CV 5-folds n'est pas exécutée dans ce carnet** — à 678k polices les estimations ponctuelles sont stables ; un bootstrap sur Gini est une extension routinière si un IC formel est nécessaire.
- **Courbes de Lorenz + Gini** (métrique actuarielle standard) et **lift top-décile** (segmentation queue haute).
- **Courbes de fiabilité** (prime pure prédite vs observée par décile) ajoutées pour que la calibration soit visible.
- **Sensibilité du `var_power` Tweedie** scannée sur 1,3-1,7 : Gini reste dans 0,307-0,313, confirmant la robustesse au choix de la puissance.
- **Facteur de lissage de Duan ≈ 1,55** sur la rétro-transformation du GBM gravité : le `expm1(predict_log)` naïf sous-prédisait la gravité d'environ 35 % car $E[\exp(X)] \neq \exp(E[X])$ pour cibles log-ajustées. La correction corrige le niveau absolu de la prime pure (et l'adéquation des réserves) ; le Gini est invariant au rang donc inchangé par cette correction.

**Chiffres en tête :**

| Modèle | Gini | Lift top-décile |
|---|---|---|
| **GLM Tweedie** | **0,310** | 2,52 |
| GLM Poisson + Gamma | 0,241 | **2,66** |
| GBM (lissage Duan) | 0,211 | 1,45 |
| GBM (rétro-transformation naïve) | 0,211 | 1,45 |

Deux métriques différentes choisissent deux modèles différents. **Tweedie gagne au Gini ; Poisson + Gamma gagne au lift top-décile.** Le choix est actuariel — une tarification orientée Gini favorise Tweedie ; un programme à exposition réassurance en queue haute favorise Poisson + Gamma.

## Esquisse de déploiement

- Export des coefficients GLM (CSV, interprétables, versionnables, audit-friendly) + artefacts GBM picklés ; le moteur tarifaire consomme les deux.
- Note actuarielle avec graphiques de dépendance partielle, courbes de Lorenz, diagramme de fiabilité, et table de sensibilité var_power.

## Résultat métier

- Lift de segmentation mesurable (Gini 0,31 Tweedie, lift 2,66 Poisson + Gamma) tout en préservant l'explicabilité niveau GLM.
- Le challenger GBM sous-performe les deux GLM en segmentation sur ce jeu — rappel que pour la tarification actuarielle, les modèles structurels peuvent battre le ML non contraint.
