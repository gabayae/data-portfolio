<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/fr/) · [Carnet](https://github.com/gabayae/data-portfolio/blob/main/04-retail-demand-m5/notebook.ipynb)

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
| Agrégat (national hebdomadaire) | SARIMA(1,1,1)(0,1,1)₅₂ |
| Base (item × magasin) | `GradientBoostingRegressor` avec features lag/calendrier/rolling |
| Réconciliation | Projection MinT-OLS sur toute la hiérarchie : TOTAL / STATE (3) / STATE×DEPT (15) / BOTTOM (130) |

## Validation

- **Test holdout 8 semaines**, RMSSE par série à chaque niveau de la hiérarchie (pas seulement TOTAL+BOTTOM), chaque série mise à l'échelle par sa propre erreur naïve d'entraînement selon le protocole canonique M5 WRMSSE.
- Chiffres en tête :

| Niveau | RMSSE moyen pré-recon | RMSSE moyen post-recon | Δ |
|---|---|---|---|
| TOTAL (1 série) | 3,11 | 3,13 | +0,02 (légère dégradation — tiré vers bottom-up) |
| STATE (3 séries) | 2,30 | 2,25 | **−0,05 (amélioration)** |
| STATE×DEPT (15 séries) | 1,59 | 1,57 | **−0,02 (amélioration)** |
| BOTTOM (130 séries) | 1,305 | 1,299 | −0,006 (négligeable) |

Ce que disent les chiffres : la cohérence tient par construction (les sommes bottom égalent TOTAL par algèbre linéaire). La réduction d'erreur mesurable n'apparaît qu'aux niveaux intermédiaires où MinT fait d'habitude son travail (STATE, STATE×DEPT). Le TOTAL se dégrade légèrement car la réconciliation tire l'agrégat SARIMA vers la somme bottom-up ; le BOTTOM bouge à peine.

## Esquisse de déploiement

- Pipeline batch hebdomadaire : GBM de base par (item × magasin), SARIMA agrégé, réconciliation MinT-OLS, sortie écrite sous forme de table `(niveau, série, semaine, prévision)` cohérente.
- Consommateurs : réapprovisionnement lit BOTTOM ; merchandising lit STATE×DEPT ; planification lit TOTAL — tous lisent les mêmes chiffres réconciliés.

## Résultat métier

- Un ensemble de prévisions cohérentes à travers TOTAL → STATE → STATE×DEPT → BOTTOM ; réapprovisionnement, merchandising et planification n'ont plus à débattre du chiffre correct.
- Le gain MinT-OLS est modeste en absolu (centièmes de RMSSE aux niveaux intermédiaires) ; la valeur opérationnelle est la cohérence, pas l'amélioration d'exactitude.

**Prochaines itérations :** réconciliation WLS / MinT-shrink avec covariances empiriques des erreurs ; features prix/promo du calendrier M5 ; évaluation sur fenêtres à origine glissante pour IC sur le Δ RMSSE à chaque niveau.
