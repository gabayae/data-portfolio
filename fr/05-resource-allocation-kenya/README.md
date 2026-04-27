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
| Processus de décision | Processus décisionnel de Markov (état = stock, file, météo ; action = prochaine formation ; récompense = patients servis − coût de déplacement) |
| Solveur | Q-learning tabulaire |
| Baseline statique | Programmation linéaire (PL) max-couverture pour la localisation des formations |

## Validation

- Simulations rolling contre planning historique (manuel) et baseline PL
- Métriques : patients servis attendus, distance parcourue, couverture du quartile inférieur des bassins de captage

## Déploiement

- Interface Streamlit pour les responsables sanitaires de district — recommandations hebdomadaires de planning avec override manuel
- Ré-entraînement mensuel de la Q-table à mesure que les données de visites s'accumulent

## Résultat métier

- 20 % d'extension de couverture dans les régions sous-desservies vs le planning manuel
- Compromis couverture vs coût de déplacement explicité aux décideurs
