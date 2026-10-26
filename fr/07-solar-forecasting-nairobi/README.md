<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/fr/) · [Étude de cas](https://gabayae.github.io/data-portfolio/fr/case-studies/solar/) · [Carnet](https://github.com/gabayae/data-portfolio/blob/main/07-solar-forecasting-nairobi/notebook.ipynb)

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
  - `ALLSKY_SFC_SW_DWN`: irradiance shortwave de surface (kWh/m²/jour) — la **cible de prévision**
  - `T2M`: température à 2 m (°C)
  - `RH2M`: humidité relative à 2 m (%)
  - `WS2M`: vitesse du vent à 2 m (m/s)
  - `PRECTOTCORR`: précipitations corrigées (mm/jour)
  - `CLOUD_AMT`: couverture nuageuse (%)

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
- Métriques : MAPE, RMSE, couverture empirique des IP 95 %
- Baselines : naïf-dernier, naïf-saisonnier (lag 365 jours), climatologie mensuelle (calculée **sur le train seul** — pas sur la série complète)
- MAPE en tête sur ce run : **GBM 9,4 % · climatologie mensuelle 12,6 % · SARIMA 13,8 % · UC 19,6 %**. À la latitude de Nairobi l'enveloppe saisonnière porte l'essentiel de la prédictibilité : la climatologie bat SARIMA. Le GBM gagne en erreur ponctuelle uniquement parce qu'il voit les covariables nuage/humidité du jour.
- Couverture empirique des IP 95 % : SARIMA 89/90, UC 89/90 — l'IC Clopper-Pearson autour de 89/90 est environ [0,94 ; 1,00], donc ces échantillons sont compatibles avec toute vraie couverture ≥ 94 %. Les intervalles sont directionnels, pas formellement calibrés à cette taille d'échantillon.

## Esquisse de déploiement

- Ré-entraînement planifié + artefact SARIMA/UC picklé ; le même pipeline s'étend à toute ville africaine en changeant la lat/lon dans `download_data.py`.
- Les prévisions ponctuelles GBM conditionnées météo nécessitent une prévision météo chaînée au-delà d'un horizon de 1 jour (le nuage du jour est le levier).

## Résultat métier

- Visibilité à 30 jours sur l'irradiance solaire avec IP 95 % directionnels — appuie les décisions de dispatch et de dimensionnement batterie pour le solaire grande échelle et le pay-as-you-go.
- À cette latitude, la climatologie est une baseline forte ; le gain du ML vient de la météo du jour, pas de la structure temporelle.
- Entièrement reproductible depuis une source de données gratuite et programmatique — facile à auditer.
