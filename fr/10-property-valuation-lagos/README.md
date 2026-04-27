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
| GBM | LightGBM / GradientBoostingRegressor avec quartier en one-hot + features extraites |

## Validation

- Découpage aléatoire 80/20 ; métriques : R², MAE sur log-prix, MAPE
- Comparaison directe OLS vs GBM

## Déploiement

- API `POST /property-valuation` retournant estimation de prix + intervalle 80 %
- Tableau de bord agent immobilier avec superpositions de distributions par quartier

## Résultat métier

- Agents immobiliers et acheteurs ancrent leurs prix sur un modèle plutôt que des intuitions
- Les prêteurs hypothécaires obtiennent une référence d'évaluation explicable
- Le même pipeline s'étend trivialement à Abuja, Ibadan, Port Harcourt avec des données taggées par quartier
