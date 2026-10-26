<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/fr/) · [Carnet](https://github.com/gabayae/data-portfolio/blob/main/05-resource-allocation-kenya/notebook.ipynb) · [Étude de cas →](https://gabayae.github.io/data-portfolio/fr/case-studies/kenya/)

---

# Optimisation stochastique pour l'allocation de ressources — formations sanitaires du Kenya

## Question métier

Peut-on planifier des cliniques mobiles à travers les comtés sous-desservis pour maximiser la couverture populationnelle malgré une demande, des conditions routières et une disponibilité du personnel incertaines ?

## Données et EDA

- **Source :** liste des formations, populations de captage, historiques de visites, réseau routier, météo/saisonnalité. Substituts publics : [Kenya Open Data](https://www.opendata.go.ke/). Le carnet génère par défaut un scénario synthétique de 8 formations dans un comté.
- **Cibles d'EDA :**
  - Variations saisonnières de la demande
  - Clusters géographiques de sous-couverture
  - Forte variance de l'utilisation journalière

## Modélisation

| Composant | Choix |
|---|---|
| Processus de décision | Processus décisionnel de Markov (état = `(location, day_bucket)` ; action = prochaine formation ; récompense = patients servis − coût de déplacement − pénalité de visite récente) |
| Solveur | Q-learning tabulaire (|S|·|A| = 84·12) |
| Baseline statique | Programmation linéaire (PL) max-couverture, avec un plafond d'équité sur les visites par comté |
| Baseline manuelle | Planning en round-robin |

## Validation

- Simulations contre le planning manuel et la baseline PL plafonnée
- Métriques : patients servis, distance parcourue (km), couverture des comtés à faible demande
- Les politiques ne sont pas à budget équivalent : le round-robin manuel engage 87 km/jour de déplacement obligatoire ; Q-learning peut choisir de ne pas se déplacer. Voir l'étude de cas pour l'analyse complète.

## Esquisse de déploiement

- Interface Streamlit pour les responsables sanitaires de district — la sortie de la PL plafonnée est le candidat déployable ; la politique greedy du Q-learning s'est effondrée sur un unique comté dans ce run et ne doit pas être déployée en l'état.
- Ré-entraînement mensuel à mesure que les données de visites s'accumulent.

## Résultat métier

- La PL plafonnée atteint **+39 % de couverture** vs le planning manuel, avec une contrainte d'équité qui force les visites aux comtés à faible demande. C'est le chiffre déployable.
- Le **+122 %** du Q-learning vs manuel vient d'une politique greedy dégénérée (`total_travel_km = 0`, `low_demand_visits = 0`) ; voir l'encadré de l'étude de cas. Le reward-shaping fait l'essentiel du travail à l'entraînement et ne tient pas à l'évaluation.
- Leçon de fond : *la formulation des contraintes compte plus que l'algorithme.* Sur ce problème une PL plafonnée avec équité est plus défendable qu'une politique RL difficile à stabiliser.
