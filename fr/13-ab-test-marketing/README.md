<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/fr/) · [Carnet](https://github.com/gabayae/data-portfolio/blob/main/13-ab-test-marketing/notebook.ipynb)

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
| Test t de Welch avec Bonferroni | Comparaisons par paires entre promotions |
| ANOVA à un facteur | Test conjoint sur les trois promotions |
| OLS avec ajustement + SE cluster-robust sur `LocationID` | Inférence honnête sous clustering au niveau magasin |
| Test formel d'interaction `C(Promotion) × C(MarketSize)` | Garde-fou Simpson avec p-valeur |
| Postérieur Normal-Normal à prior plat sur la moyenne de chaque bras | `P(a > b)` comme probabilité directe (en reconnaissant le prior plat impropre, pas une vraie analyse bayésienne informative) |

## Validation

- 548 observations = **137 localisations × 4 semaines** — non indépendantes. Les SE OLS naïves sont trop étroites ; le carnet reporte à la fois les SE naïves et cluster-robust sur `LocationID` pour que l'inflation soit visible.
- Correction pour comparaisons multiples (Bonferroni sur 3 tests t par paires).
- Taille d'effet : d de Cohen (P1 vs P2 d = 0,68 modéré-grand ; P1 vs P3 d = 0,16 négligeable).
- F d'interaction = 4,93, p = 0,0007 — le garde-fou Simpson est statistiquement réel, pas seulement visuel.

## Esquisse de déploiement

- Tableau de bord résumant ventes par bras + IC 95 % (clustered) + estimation de lift vs bras de référence.
- Règle de décision : déployer la promotion gagnante si (a) ANOVA p < 0,01 ET (b) p par paires clustered < 0,01 vs toutes alternatives ET (c) d de Cohen > 0,3 ET (d) le gagnant tient dans chaque strate de taille de marché.

## Résultat métier

- Décision de déploiement de promotion défendable statistiquement avec inférence clustered.
- Le test formel d'interaction confirme l'interaction taille-de-marché × promotion (visible dans la table des moyennes stratifiées).
- La couche « bayésienne » à prior plat est une lecture de commodité, pas une vraie analyse bayésienne informative ; un modèle hiérarchique propre avec effets aléatoires magasin élargirait encore les postérieurs.
