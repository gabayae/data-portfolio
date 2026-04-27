<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/fr/) · [Carnet](https://github.com/gabayae/data-portfolio/blob/main/09-flight-demand-southern-africa/notebook.ipynb)

---

# Prévision de demande et de prix aériens — Afrique australe

## Question métier

Peut-on prévoir prix et demande sur les routes aériennes d'Afrique australe à 7–30 jours pour que :
- Les compagnies aériennes (FlySafair, LIFT, SAA) ajustent dynamiquement leurs prix
- Les agences de voyage conseillent leurs clients sur les fenêtres optimales de réservation
- Les offices de tourisme anticipent la pression saisonnière de demande sur les routes Le Cap, Durban, Johannesburg

C'est l'analogue africain du projet de fréquentation des transports de Calgary — même boîte à outils de séries temporelles et de modélisation de la demande, appliquée à la demande inter-villes du transport aérien.

## Données

- **Source :** [Southern Africa Flight Prices (Kaggle)](https://www.kaggle.com/datasets/mazano/southern-africa-flight-prices) — 15 393 vols, horodatages départ/arrivée, compagnie, route, prix.

Lancer `python download_data.py` (Kaggle CLI requis).

## Cibles d'EDA

- Distribution des prix par compagnie et route
- Effets jour-de-la-semaine et heure-de-la-journée
- Patterns de tarification selon le délai avant départ
- Top des routes par volume (CPT–JNB, JNB–DUR, etc.)

## Modélisation

| Famille | Modèle |
|---|---|
| Séries temporelles classiques | SARIMA sur volume journalier de vols par route |
| ML pour la prévision | Prédicteur de prix gradient-boosté (route, compagnie, jour-de-la-semaine, délai) |
| Demande + prix conjoints | LightGBM avec features d'élasticité-prix |

## Validation

- 20 % des vols mis de côté pour la prédiction de prix (MAE, RMSE, MAPE)
- Découpage temporel pour la prévision de volume journalier

## Déploiement

- API `GET /forecast?route=CPT-JNB&horizon=30` retournant volume attendu journalier + IP 95 %
- Endpoint de tarification dynamique pour les compagnies

## Résultat métier

- Les prévisions de volume journalier alimentent la planification équipage/avion
- L'insight d'élasticité-prix éclaire les décisions de revenue management
- Le même pipeline s'étend trivialement aux réseaux de routes d'Afrique de l'Ouest et de l'Est
