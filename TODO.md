## devcontainers
- [x] fusionner metrics et display

---

## 1. Generator
- [ ] Ajouter différents patterns de trajectoires
- [ ] Ajouter des outliers (mesures, perceptual aliasing)
- [x] Générer dataset avec landmarks 2 - 2
- [ ] Meilleure solution de configuration et génération des datasets
- [ ] Vérifier la répartition des landmarks
- [ ] définir le nom du dataset d'après le nom du fichier de configuration
- [ ] si repeats > 1 ajouter num au nom du dataset
- [ ] Améliorer script parser

---

## 2. Configurations
- [ ] Ajouter une section pour les patterns de trajectoire
- [ ] Ajouter section pour les outliers
- [ ] Retirer nom des paramètres de configuration

---

## 3. Datasets

---

## 4. Metrics
- [X] Script pour extraire dans Results l'ensemble des erreurs
- [X] Add Method to export all errors in a text file
- [ ] Add Absolute Mean Square error computation

---

## 5. Display
- [ ] Scripts pour afficher de différentes manières les erreurs (Stats, 3D, ..)
- [ ] Add visualization tools for error display
- [X] Merge devcontainer with metrics to get errors data

---

## 6. Results
- [ ] Définir une structure de résultats
---

## Ideas
- Trouver une manière pour optimiser le workfow avec CSLAM
- Génération en C++ ?
- Simplifier le fonctionnement des résultats
