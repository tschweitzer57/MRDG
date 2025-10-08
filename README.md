# MRDG
Multi-Robots Dataset Generator is a generator of datasets for multi-robots scenarios. It can generate data for backend algorithms

---

```markdown
![MRDG global scheme](0_Documentation\Ressources\MRDG_scheme.png)
```

```markdown
![MRDG global scheme](0_Documentation\Ressources\Global_CSLAM_MRDG.png)
```

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

- [Generator](./01_Generator) : Contient les scripts capables de générer les datasets selon les différents scénarios envisagés
- [Configurations](./02_Configurations) : Contient les fichiers de configuration des datasets
- [Metrics](./03_Metrics) : Contient des scripts pour calculer les différentes erreurs et les afficher/visualiser
- [Datasets](./04_Datasets) : Contient les datasets ayant été générés
- [Results](./05_Results) : Contient les résultats obtenus (erreurs et visualisations)

---

## Future improvements

[Todo list](./TODO.md)
