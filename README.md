# Automated Data Reporting System

## 1. Présentation du projet

Ce projet consiste à développer un système automatisé de collecte, de nettoyage, d'analyse et de reporting de données commerciales à l'aide de Python.

L'objectif est de concevoir un pipeline capable de traiter des données de ventes, de contrôler leur qualité, de calculer des indicateurs de performance et de générer automatiquement un rapport Excel accompagné de visualisations.

Le projet repose sur une entreprise fictive, **Sunu Market**, afin de simuler un contexte commercial et de mettre en pratique les compétences acquises en analyse de données.

> **Important :** toutes les données utilisées dans ce projet sont synthétiques. Elles ne représentent pas les ventes réelles d'une entreprise ni les statistiques du marché sénégalais.

## 2. Objectifs

- Générer et structurer des données commerciales.
- Explorer les données afin d'identifier les problèmes de qualité.
- Nettoyer et valider les données avec Python.
- Calculer les principaux indicateurs de performance commerciale.
- Analyser les ventes par catégorie, région, produit et mois.
- Générer automatiquement des graphiques.
- Produire un rapport Excel organisé et réutilisable.
- Automatiser l'ensemble du processus à l'aide d'un script principal.

## 3. Technologies utilisées

| Technologie | Utilisation |
|---|---|
| Python | Automatisation du pipeline |
| Pandas | Manipulation, nettoyage et analyse des données |
| NumPy | Opérations numériques |
| Matplotlib | Création de visualisations |
| Seaborn | Visualisation statistique |
| OpenPyXL | Création et mise en forme du rapport Excel |
| CSV | Stockage des données et des résultats |
| Excel | Consultation des rapports commerciaux |

## 4. Architecture du projet

```text
automated-data-reporting/
│
├── data/
│   ├── raw/
│   │   ├── customers.csv
│   │   ├── orders.csv
│   │   └── products.csv
│   │
│   └── processed/
│       ├── customers_clean.csv
│       ├── orders_clean.csv
│       └── products_clean.csv
│
├── outputs/
│   ├── charts/
│   │   ├── monthly_revenue.png
│   │   ├── revenue_by_category.png
│   │   ├── revenue_by_region.png
│   │   └── top_10_products.png
│   └── logs/
│
├── reports/
│   ├── kpi_summary.csv
│   ├── sales_by_category.csv
│   ├── sales_by_region.csv
│   ├── top_10_products.csv
│   ├── monthly_sales.csv
│   └── rapport_commercial.xlsx
│
├── src/
│   ├── generate_data.py
│   ├── explore_data.py
│   ├── clean_data.py
│   ├── analyze_data.py
│   ├── generate_charts.py
│   ├── generate_report.py
│   └── main.py
│
├── requirements.txt
└── README.md
```

## 5. Fonctionnement du pipeline

Le pipeline est composé de six étapes principales.

### Étape 1 — Génération des données

Le script `generate_data.py` crée des jeux de données synthétiques comprenant :

- des produits et leurs catégories ;
- des clients et leurs informations géographiques ;
- des commandes et leurs montants commerciaux.

Des anomalies sont volontairement introduites dans les données de commandes pour simuler des problèmes de qualité rencontrés dans un contexte professionnel.

### Étape 2 — Exploration des données

Le script `explore_data.py` examine les fichiers bruts afin d'identifier notamment :

- les valeurs manquantes ;
- les doublons ;
- les quantités invalides ;
- les incohérences potentielles ;
- les dimensions des jeux de données.

### Étape 3 — Nettoyage et validation

Le script `clean_data.py` applique plusieurs contrôles :

- suppression des doublons exacts ;
- traitement des données manquantes ;
- exclusion des quantités nulles ou négatives ;
- validation des identifiants clients et produits ;
- contrôle des prix par rapport au catalogue ;
- recalcul des montants bruts et nets.

Les données validées sont enregistrées dans `data/processed/`.

### Étape 4 — Analyse commerciale

Le script `analyze_data.py` calcule les indicateurs et produit plusieurs tableaux analytiques :

- synthèse des indicateurs clés ;
- chiffre d'affaires par catégorie ;
- chiffre d'affaires par région ;
- classement des dix produits les plus performants en chiffre d'affaires ;
- évolution mensuelle des ventes.

### Étape 5 — Visualisation

Le script `generate_charts.py` produit quatre graphiques :

- évolution mensuelle du chiffre d'affaires ;
- chiffre d'affaires par catégorie ;
- chiffre d'affaires par région ;
- classement des dix premiers produits.

Les graphiques sont enregistrés dans `outputs/charts/`.

### Étape 6 — Génération du rapport Excel

Le script `generate_report.py` rassemble les résultats dans un classeur Excel nommé `rapport_commercial.xlsx`.

Le classeur comprend six feuilles :

1. Synthèse KPI
2. Ventes par catégorie
3. Ventes par région
4. Top 10 produits
5. Ventes mensuelles
6. Dashboard

Le tableau de bord intègre les quatre graphiques générés par le pipeline.

## 6. Indicateurs clés

Le projet calcule notamment les indicateurs suivants :

| Indicateur | Description |
|---|---|
| Chiffre d'affaires net | Total des ventes après remises |
| Chiffre d'affaires brut | Total des ventes avant remises |
| Remises | Montant total des réductions accordées |
| Nombre de commandes | Nombre de commandes distinctes |
| Quantités vendues | Nombre total d'unités vendues |
| Panier moyen | Chiffre d'affaires net divisé par le nombre de commandes |
| Performance par catégorie | Contribution de chaque catégorie au chiffre d'affaires |
| Performance régionale | Chiffre d'affaires généré par région |
| Performance des produits | Classement des produits par chiffre d'affaires |
| Évolution mensuelle | Variation du chiffre d'affaires au fil des mois |

Les valeurs obtenues dépendent des données synthétiques générées lors de l'exécution du pipeline.

## 7. Installation

### Prérequis

- Python installé sur l'ordinateur ;
- Git pour la gestion du code source ;
- un terminal ou un éditeur de code tel que Visual Studio Code.

### Étape 1 — Récupérer le projet

Après publication sur GitHub, cloner le dépôt :

```bash
git clone <URL_DU_DEPOT>
```

Se placer ensuite dans le dossier du projet :

```bash
cd automated-data-reporting
```

Remplacer `<URL_DU_DEPOT>` par l'adresse réelle du dépôt GitHub.

### Étape 2 — Installer les dépendances

```bash
python -m pip install -r requirements.txt
```

## 8. Exécution

Depuis la racine du projet, lancer :

```bash
python src/main.py
```

Le script principal exécute automatiquement les étapes suivantes :

1. Génération des données.
2. Exploration des données brutes.
3. Nettoyage et validation.
4. Analyse commerciale.
5. Génération des graphiques.
6. Création du rapport Excel.

À la fin du processus, le rapport est disponible dans :

```text
reports/rapport_commercial.xlsx
```

Les fichiers CSV analytiques sont enregistrés dans `reports/`, les graphiques dans `outputs/charts/` et les données nettoyées dans `data/processed/`.

> **Attention :** l'exécution du pipeline régénère les données synthétiques et remplace les fichiers de sortie existants.

## 9. Compétences mises en pratique

Ce projet permet de mettre en œuvre plusieurs compétences utiles pour un poste de Data Analyst :

- préparation et nettoyage des données ;
- contrôle de la qualité des données ;
- manipulation de fichiers CSV ;
- analyse exploratoire ;
- calcul d'indicateurs commerciaux ;
- regroupement et agrégation des données ;
- création de visualisations ;
- automatisation de tâches avec Python ;
- génération de rapports Excel ;
- organisation d'un projet Python ;
- documentation technique et préparation à la publication sur GitHub.

## 10. Limites et améliorations possibles

Le projet constitue une simulation pédagogique. Il ne comprend pas encore de connexion à une base de données réelle ni de collecte depuis un système commercial externe.

Plusieurs améliorations sont envisageables :

- intégrer une base de données SQL ;
- automatiser l'import de fichiers commerciaux externes ;
- ajouter des tests automatisés pour les contrôles de qualité ;
- mettre en place un système de journalisation des exécutions ;
- enrichir les analyses avec des indicateurs de rentabilité ;
- développer un tableau de bord interactif dans Power BI ;
- planifier l'exécution périodique du pipeline.

## 11. Conclusion

Ce projet illustre la conception d'un pipeline de reporting commercial avec Python, depuis la génération et la préparation des données jusqu'à la production automatisée d'un rapport Excel.

Il met l'accent sur la qualité des données, la reproductibilité des analyses et l'automatisation des tâches répétitives, trois aspects importants du travail d'un Data Analyst.

---

**Projet personnel de portfolio — Data Analytics & Python**