# MRDG
Multi-Robots Dataset Generator (MRDG) is a generator of datasets for multi-robots scenarios. It can generate data for backend algorithms.

<p align="center">
<img src="0_Documentation/Ressources/Global_CSLAM_MRDG.png"
    alt="Example JRL 2D Bearing & Range Dataset." 
    width="70%"/>
</p>

---

<p align="center">
<img src="0_Documentation/Ressources/MRDG_scheme.png"
    alt="Example JRL 2D Bearing & Range Dataset."
    width="70%"/>
</p>

## Prerequisites

- **Operating System** :
  - **Ubuntu 22.04**
  - **Windows 10/11**

- **Required** :
  - **Docker**
  - [For windows users] **WSL2 and X11 Server**
  - **Visual Studio Code (Plug in devcontainers)**

---

## Repository structure

- [Documentation](./0_Documentation) : Contient la documentation de MRDG
- [Generator](./1_Generator) : Contient les scripts capables de générer les datasets selon les différents scénarios envisagés
- [Configurations](./2_Configurations) : Contient les fichiers de configuration des datasets
- [Metrics](./3_Metrics) : Contient des scripts pour calculer les différentes erreurs et les afficher/visualiser
- [Datasets](./4_Datasets) : Contient les datasets ayant été générés
- [Results](./5_Results) : Contient les résultats obtenus (erreurs et visualisations)

---

## Future improvements

[Todo list](./TODO.md)
