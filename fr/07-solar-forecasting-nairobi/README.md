<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/fr/) · [Étude de cas](https://gabayae.github.io/data-portfolio/fr/case-studies/solar/) · [Carnet](https://gabayae.github.io/data-portfolio/07-solar-forecasting-nairobi/notebook.ipynb)

---

# Prévision d'énergie solaire — Nairobi (NASA POWER)

## Question métier

Peut-on prévoir l'irradiance solaire de surface journalière à Nairobi à 7–30 jours pour que :
- Un développeur solaire utility-scale planifie le dispatch onduleur et batterie
- Les opérateurs solaire/stockage hors-réseau (le Kenya a l'un des plus grands marchés solaire pay-as-you-go d'Afrique) dimensionnent les réserves de batterie selon le soleil attendu
- Les gestionnaires de réseau quantifient la contribution solaire attendue face aux alternatives thermique/hydro

Une erreur d'irradiance à J+1 de seulement 5 % peut suffire à inverser la décision « remplir la batterie » ou « la laisser se décharger » — les enjeux opérationnels sont réels.

## Données

- **Source :** [API NASA POWER (Prediction Of Worldwide Energy Resources)](https://power.larc.nasa.gov/), gratuite, sans authentification.
- **Localisation :** Nairobi (lat -1,2921, lon 36,8219).
- **Période :** 2014-01-01 → 2023-12-31, journalière (3 653 observations).
- **Variables :**
  - `ALLSKY_SFC_SW_DWN` — irradiance shortwave de surface (kWh/m²/jour) — la **cible de prévision**
  - `T2M` — température à 2 m (°C)
  - `RH2M` — humidité relative à 2 m (%)
  - `WS2M` — vitesse du vent à 2 m (m/s)
  - `PRECTOTCORR` — précipitations corrigées (mm/jour)
  - `CLOUD_AMT` — couverture nuageuse (%)

Lancer `python download_data.py` pour récupérer des données fraîches (sans authentification).

## Cibles d'EDA

- Forte saisonnalité annuelle (saisons des pluies mars–mai et octobre–décembre réduisent l'irradiance)
- Couverture nuageuse et humidité inversement corrélées avec l'irradiance
- Persistance jour-à-jour (autocorrélation)
- Anomalies long terme (par ex. inondations d'Afrique de l'Est en 2019)

## Modélisation

| Famille | Modèle |
|---|---|
| Séries temporelles classiques | SARIMA sur irradiance journalière |
| Espace d'états | UnobservedComponents (niveau + saisonnalité annuelle harmonique + Fourier exogène) |
| ML pour la prévision | Régresseur gradient-boosté avec features lag/rolling/calendaires + covariables nuage/humidité |

## Validation

- Test mis de côté sur 90 jours
- Métriques : MAPE, RMSE, couverture des intervalles de prévision
- Baselines : naïf-dernier, naïf-saisonnier (lag 365 jours), climatologie mensuelle

## Déploiement

- FastAPI `/forecast?horizon=30d` retournant l'irradiance moyenne journalière + IP 95 % pour le mois suivant
- Tableau de bord Streamlit pour les développeurs solaires — bande de prévision d'irradiance, planificateur d'état de charge de batterie, estimateur d'impact production
- Rafraîchissement journalier depuis NASA POWER ; ré-entraînement hebdomadaire
- Le même pipeline s'étend trivialement à Lagos, Le Cap, Le Caire, Dakar — il suffit de changer lat/lon

## Résultat métier

- Visibilité à 30 jours sur l'irradiance solaire avec intervalles calibrés — réduit l'incertitude des décisions de dispatch et de stockage
- Quantifie production attendue vs scénario pessimiste pour budget et contrats réseau
- Entièrement reproductible depuis une source de données gratuite et programmatique — facile à auditer
