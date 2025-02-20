# MRDG
Multi-Robots Dataset Generator is a generator of datasets for multi-robots scenarios. It can generate data for backend algorithms

---

## Prerequisites

- **Operating System** :
  - **Ubuntu 22.04**
  - **Windows 10/11**

- **Required ** :
  - **Docker**
  - [For windows users] ** WSL2 and X11 Server **
  - **Visual Studio Code (Plug in devcontainers)**

---

## Repository structure

- [Generator](./01_Generator) : Contient les scripts capables de générer les datasets selon les différents scénarios envisagés
- [Configurations](./02_Configurations) : Contient les fichiers de configuration des datasets
- [Datasets](./03_Datasets) : Contient les datasets ayant été générés
- [Metrics](./04_Metrics) : Contient des scripts pour calculer les différentes erreurs
- [Display](./05_Display) : Contient des scripts pour afficher/visualiser les erreurs
- [Results](./06_Results) : Contient les résultats obtenus (erreurs et visualisations)

---

## Future improvements

[Todo list](./TODO.md)
