<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/fr/) · [Carnet](https://github.com/gabayae/data-portfolio/blob/main/10-property-valuation-lagos/notebook.ipynb)

---

# Évaluation immobilière — Lagos, Nigeria

## Question métier

Peut-on prédire les prix des annonces de biens résidentiels à Lagos avec une précision suffisante pour :
- Aider les acheteurs à repérer les annonces sous-cotées ou sur-cotées
- Aider les agents immobiliers à ancrer leurs recommandations de prix
- Éclairer les modèles d'évaluation hypothécaire pour les prêteurs nigérians

## Données

- **Source :** [Housing Prices in Lagos, Nigeria (Kaggle)](https://www.kaggle.com/datasets/thedevastator/investigating-housing-prices-in-lagos-nigeria) — 9 784 annonces de vente, quartier, adresse, nom de bien en texte libre avec nombre de chambres et type de bien intégrés.

Lancer `python download_data.py`.

## Cibles d'EDA

- Distribution des prix par quartier (Ikoyi, Lekki, VI commandent une prime ; périphérie moins chère)
- Nombre de chambres et type de bien extraits de `Property_name`
- Différentiel de prix Terrain vs Appartement vs Maison vs Duplex

## Modélisation

| Famille | Modèle |
|---|---|
| Régression linéaire | OLS sur log-prix avec quartier + type de bien + chambres |
| GBM | `GradientBoostingRegressor` avec quartier en one-hot + features extraites |

## Validation

- Découpage aléatoire 80/20 (aléatoire car ce sont des annonces à dates non spécifiées, pas une prévision).
- Métriques à double échelle : **R²(log) 0,58, R²(niveau) implicitement plus bas ; MAPE brut 146 %, RMSE 366M NGN** pour le GBM. OLS : **R²(log) 0,51, MAPE brut 179 %, RMSE 396M NGN**. Le R² log est confortable ; la MAPE brute est honnête sur les limites — sur une cible de médiane ~50M NGN, se tromper routinièrement de plus que le vrai prix signifie que c'est un outil de classement, pas d'évaluation ponctuelle.
- Priorité de `parse_type` corrigée en « le plus spécifique d'abord » pour que `"semi-detached house"` → `semi-detached` (pas `house`), `"detached duplex"` → `detached` (pas `duplex`), etc.

## Esquisse de déploiement

- La sortie du modèle sert au *classement* d'annonces contre les baselines de quartier, pas à l'ancrage d'évaluations individuelles (la MAPE brute est trop large).
- Un déploiement d'estimation ponctuelle demanderait soit (a) un couple quantile-GBM (`loss='quantile'`, `alpha=0,1/0,9`) pour produire des intervalles honnêtes, soit (b) des features plus riches (surface, année de construction, état) absentes de cette collecte.

## Résultat métier

- Un modèle de prix résidentiels fonctionnel sur une collecte Kaggle Lagos gratuite ; c'est le pipeline qui compte, pas les prédictions.
- Utilisable pour le tri comparatif au niveau quartier × type × chambres. L'incertitude brute est trop large pour ancrer des expertises individuelles.
- Le même pipeline tournerait sur des collectes Abuja, Ibadan ou Port Harcourt avec la même structure.
