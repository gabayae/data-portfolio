<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/fr/) · [Carnet](https://gabayae.github.io/data-portfolio/13-ab-test-marketing/notebook.ipynb)

---

# Cadre de test A/B — promotion marketing multi-bras

## Question métier

Laquelle des trois stratégies de promotion (Promotion 1 vs 2 vs 3) génère les ventes les plus élevées ? Une vraie chaîne de fast-food les a déployées dans ses magasins ; on applique un cadre rigoureux de tests A/B/n pour tirer des conclusions correctes et recommander un déploiement.

La boîte à outils démontrée ici s'applique directement aux expériences marketing en retail ou télécom africain (par ex. campagnes push de MTN Nigeria, stratégies promo de Jumia).

## Données

- **Source :** [Fast Food Marketing Campaign A/B Test (Kaggle)](https://www.kaggle.com/datasets/chebotinaa/fast-food-marketing-campaign-ab-test) — 548 observations de ventes hebdomadaires sur 137 emplacements × 4 semaines × 3 promotions, avec taille de marché (Petite/Moyenne/Grande) et âge du magasin.

Lancer `python download_data.py`.

## Cibles d'EDA

- Distribution des ventes par bras de promotion
- Taille de marché comme stratifieur
- Effet de l'âge du magasin

## Analyses statistiques

| Test | Usage |
|---|---|
| Test t de Welch (deux échantillons) | Comparaisons par paires entre promotions |
| ANOVA à un facteur | Test conjoint sur les trois promotions |
| Analyse stratifiée (par MarketSize) | Éviter le paradoxe de Simpson |
| OLS avec ajustement par covariables | Contrôle pour `AgeOfStore`, `MarketSize` |
| A/B bayésien (Bêta-Binomial sur moyennes) | Postérieur P(promo 1 > promo 3) |

## Validation

- Correction pour comparaisons multiples (Bonferroni / Holm)
- Taille d'effet : d de Cohen
- Vérification de puissance (l'expérience était-elle correctement dimensionnée ?)

## Déploiement

- Tableau de bord résumant ventes par bras + IC 95 % + estimation de lift vs contrôle
- Règle de décision : déployer la promotion gagnante globalement si lift > 5 % avec p < 0,01 (corrigé)

## Résultat métier

- Décision de déploiement de promotion défendable statistiquement
- La stratification fait remonter les effets d'interaction (la promo 3 fonctionne-t-elle mieux dans les petits marchés ?)
- Pipeline réutilisable pour toute expérience randomisée marketing ou produit
