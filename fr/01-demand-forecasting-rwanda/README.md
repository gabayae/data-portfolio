<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/fr/) · [Carnet](https://github.com/gabayae/data-portfolio/blob/main/01-demand-forecasting-rwanda/notebook.ipynb)

---

# Prévision de la demande — chaîne d'approvisionnement en santé du Rwanda

## Question métier

Peut-on prévoir la consommation mensuelle de médicaments essentiels (ARV, HRDT) pour que les responsables logistiques planifient les réapprovisionnements et réduisent les ruptures ? Le Rwanda est le pays-cible (105 observations mensuelles, 2007–2015, 94 mois non-nuls) dans un jeu de données public réel de 10 324 expéditions PEPFAR/USAID SCMS sur 43 pays.

## Données

- **Source :** registres d'expéditions réels PEPFAR / USAID Supply Chain Management System (SCMS) — [apoorvwatsky/supply-chain-shipment-pricing-data](https://www.kaggle.com/datasets/apoorvwatsky/supply-chain-shipment-pricing-data). 10 324 expéditions sur 43 pays, 2006–2015. Agrégées en unités mensuelles livrées ; le Rwanda est la série modélisée (105 mois, 94 non-nuls).
- La mention antérieure dans le README d'un « fallback synthétique 12 SKU × 10 districts × 60 mois » est retirée — le carnet modélise directement l'agrégat Rwanda réel.

## Modélisation

| Famille | Modèle |
|---|---|
| Séries temporelles classiques | SARIMA(1,1,1)(1,1,1)₁₂ |
| Espace d'états | UnobservedComponents (local-linear-trend + saisonnier stochastique) |
| Lissage exponentiel | Holt-Winters additif triple |
| ML pour la prévision | `GradientBoostingRegressor` sur features lag/calendrier/rolling |
| Baseline de référence | Naïf-saisonnier (mois prochain = même mois il y a un an) |

## Validation

- **Backtest à origine glissante, 18 folds à un pas d'avance**, les quatre candidats ré-ajustés à chaque origine sur données d'entraînement uniquement.
- Métrique : WAPE (robuste aux mois à ventes nulles, contrairement au MAPE vanilla).
- Chiffres en tête sur ce run :

| Modèle | WAPE | Gain vs naïf |
|---|---|---|
| **GBM (récursif 1 pas)** | **0,863** | **24 % d'amélioration** |
| SARIMA | 0,941 | 17 % d'amélioration |
| Naïf-saisonnier | 1,130 | — |
| Holt-Winters | 1,143 | −1 % (pire) |

Un WAPE dans cette fourchette est un score *absolu* faible ; cela reflète la difficulté réelle des données mensuelles de chaîne logistique santé à demande intermittente (94 mois non-nuls sur 105), pas une faiblesse des modèles. Le gain de 24 % du GBM sur le naïf-saisonnier est le résultat honnête.

- **Couverture IP 95 % de SARIMA** sur les 18 folds glissants : **18/18 = 100 %**, demi-largeur moyenne ≈ 385k unités — intervalles trop larges (sur-couverture par rapport au nominal 95 %), pas calibrés. L'IC Clopper-Pearson autour de 18/18 est environ [0,81 ; 1,00], donc l'échantillon est compatible avec toute vraie couverture ≥ 81 %.

## Esquisse de déploiement

- Ré-entraînement mensuel par série (pays × catégorie de produit) ; artefacts versionnés.
- Pas un système de production — le carnet s'arrête à la prévision hors-ligne sur l'extraction PEPFAR réelle.

## Résultat métier

- Visibilité à 12 mois sur les unités mensuelles livrées PEPFAR au Rwanda ; le GBM est le choix opérationnel sur ce run selon le WAPE à origine glissante.
- Régime de demande intermittente : s'attendre à un WAPE dans la fourchette 0,8–1,0 sur les agrégats mensuels de chaîne logistique santé ; les prévisions d'intervalle importent plus que les prévisions ponctuelles pour les décisions de réapprovisionnement.

**Prochaines itérations :** réconciliation hiérarchique (pays → région → global), régresseurs exogènes (lancements de programmes, cycles de financement), méthode de Croston par SKU à faible rotation.
