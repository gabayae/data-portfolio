<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/fr/) · [Carnet](https://github.com/gabayae/data-portfolio/blob/main/09-flight-demand-southern-africa/notebook.ipynb)

---

# Demande et prix aériens — Afrique australe

## Périmètre

Analyse exploratoire d'une collecte Kaggle sur 31 jours des listings de vols d'Afrique australe. Prévision de volume sur la route principale (JNB–CPT) sur une fenêtre de holdout de 6 jours ; prédiction de prix conditionnelle à `(route, compagnie, dow, hour, day_index)` sur l'ensemble de la collecte.

**Ce que ce projet n'est pas.** Pas une prévision à 7–30 jours — le jeu de données couvre seulement 2025-03-14 à 2025-04-13, donc le holdout SARIMA est de 6 jours sur une série quasi-constante (moyenne ≈ 90 vols/jour, CV ≈ 8 %). Pas un modèle de courbe tarifaire — la collecte Kaggle ne porte que des dates de départ, pas de dates de réservation, donc il n'existe pas de variable délai-avant-départ ; la feature `day_index` est un index 0–30 dans la fenêtre, pas un délai.

## Données

- **Source :** [Southern Africa Flight Prices (Kaggle)](https://www.kaggle.com/datasets/mazano/southern-africa-flight-prices) — 15 393 listings de vols sur 31 jours, horodatages de départ, compagnie, route, prix.

Lancer `python download_data.py` (Kaggle CLI requis).

## Cibles d'EDA

- Distribution des prix par compagnie et route
- Effets jour-de-la-semaine et heure-de-la-journée
- Top des routes par volume (CPT–JNB, JNB–DUR, etc.)

## Modélisation

| Famille | Modèle |
|---|---|
| Séries temporelles classiques | SARIMA sur volume journalier (route principale) |
| Challenger ML | `GradientBoostingRegressor` sur `(route, compagnie, dow, hour, day_index)` pour la prédiction de prix |
| Baseline | naive-moyenne / naive-dernière / naive-saisonnière (volume) ; `groupby(route, compagnie, dow, hour).mean()` (prix) |

## Validation

- Volume : MAPE SARIMA à holdout de 6 jours, avec IC bootstrap sur les 6 erreurs de test (l'échantillon est trop petit pour une inférence autonome significative).
- Prix : découpage aléatoire 80/20 ; MAE du GBM comparée à une baseline lookup par moyenne de cellule pour voir si le GBM apprend quelque chose au-delà de `groupby.mean()`.

## Esquisse de déploiement

- Pas un système de production — le périmètre est trop étroit (fenêtre de 31 jours) pour un service de planification.
- Des collectes plus longues (6+ mois) avec métadonnées de date de réservation débloqueraient la dynamique tarifaire que la collecte actuelle ne peut pas porter.

## Résultat métier

- Esquisse méthodologique de volume journalier + prix conditionnel sur une collecte courte.
- Le GBM reproduit les moyennes de cellules ± bruit sur cette collecte — pas d'évidence d'apprentissage d'une courbe tarifaire au-delà du lookup. Le 2 % MAPE SARIMA sur 6 points de test est directionnel, pas une preuve de skill.
