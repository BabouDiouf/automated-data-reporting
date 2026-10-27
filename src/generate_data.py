
from pathlib import Path
import numpy as np
import pandas as pd


# ==================================================
# 1. CONFIGURATION DU PROJET
# ==================================================

# Dossier racine du projet
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Dossier de stockage des données brutes
DATA_DIR = PROJECT_DIR / "data" / "raw"

# Création du dossier si nécessaire
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Graine aléatoire pour reproduire les mêmes résultats
rng = np.random.default_rng(42)

# Période étudiée
START_DATE = "2026-01-01"
END_DATE = "2026-09-30"


# ==================================================
# 2. GÉNÉRATION DU CATALOGUE DE PRODUITS
# ==================================================

product_categories = {
    "Alimentation": [
        "Riz parfumé",
        "Huile végétale",
        "Sucre",
        "Lait en poudre",
        "Pâtes alimentaires",
    ],
    "Électronique": [
        "Téléviseur",
        "Téléphone",
        "Ordinateur portable",
        "Écouteurs",
        "Chargeur",
    ],
    "Électroménager": [
        "Ventilateur",
        "Mixeur",
        "Réfrigérateur",
        "Fer à repasser",
        "Micro-ondes",
    ],
    "Hygiène": [
        "Savon liquide",
        "Dentifrice",
        "Shampoing",
        "Déodorant",
        "Papier hygiénique",
    ],
    "Maison": [
        "Chaise",
        "Table",
        "Lampe",
        "Matelas",
        "Rangement plastique",
    ],
}

# Prix indicatifs en FCFA
category_price_ranges = {
    "Alimentation": (500, 10000),
    "Électronique": (2000, 300000),
    "Électroménager": (5000, 250000),
    "Hygiène": (500, 10000),
    "Maison": (2000, 150000),
}

products = []

for category, product_names in product_categories.items():
    min_price, max_price = category_price_ranges[category]

    for product_name in product_names:
        products.append(
            {
                "Product_Name": product_name,
                "Category": category,
                "Unit_Price": int(
                    rng.integers(min_price, max_price + 1)
                ),
            }
        )

products_df = pd.DataFrame(products)

# Attribution d'un identifiant unique à chaque produit
products_df.insert(
    0,
    "Product_ID",
    [f"PR{i:03d}" for i in range(1, len(products_df) + 1)],
)

# Export du catalogue
products_df.to_csv(
    DATA_DIR / "products.csv",
    index=False,
    encoding="utf-8-sig",
)


# ==================================================
# 3. GÉNÉRATION DES CLIENTS
# ==================================================

cities_by_region = {
    "Dakar": ["Dakar", "Pikine", "Guédiawaye", "Rufisque"],
    "Thiès": ["Thiès", "Mbour", "Tivaouane"],
    "Saint-Louis": ["Saint-Louis", "Richard-Toll", "Dagana"],
    "Diourbel": ["Diourbel", "Touba", "Mbacké"],
    "Kaolack": ["Kaolack", "Nioro du Rip"],
    "Ziguinchor": ["Ziguinchor", "Bignona", "Oussouye"],
    "Louga": ["Louga", "Kébémer", "Linguère"],
    "Fatick": ["Fatick", "Foundiougne"],
    "Kolda": ["Kolda", "Vélingara"],
    "Matam": ["Matam", "Ourossogui"],
    "Tambacounda": ["Tambacounda", "Bakel"],
    "Kaffrine": ["Kaffrine", "Koungheul"],
    "Sédhiou": ["Sédhiou", "Goudomp"],
    "Kédougou": ["Kédougou", "Salémata"],
}

regions = list(cities_by_region.keys())

customers_df = pd.DataFrame(
    {
        "Customer_ID": [
            f"CL{i:04d}" for i in range(1, 501)
        ],
        "Customer_Name": [
            f"Client {i:03d}" for i in range(1, 501)
        ],
        "Region": rng.choice(regions, size=500),
    }
)

# Attribution d'une ville en fonction de la région
customers_df["City"] = customers_df["Region"].map(
    lambda region: rng.choice(cities_by_region[region])
)

# Organisation des colonnes
customers_df = customers_df[
    ["Customer_ID", "Customer_Name", "City", "Region"]
]

# Export des clients
customers_df.to_csv(
    DATA_DIR / "customers.csv",
    index=False,
    encoding="utf-8-sig",
)


# ==================================================
# 4. GÉNÉRATION DES LIGNES DE VENTE
# ==================================================

n_orders = 5000

orders_df = pd.DataFrame(
    {
        "Order_ID": [
            f"CMD{i:05d}" for i in range(1, n_orders + 1)
        ],
        "Order_Date": pd.to_datetime(
            rng.choice(
                pd.date_range(START_DATE, END_DATE),
                size=n_orders,
            )
        ),
        "Customer_ID": rng.choice(
            customers_df["Customer_ID"],
            size=n_orders,
        ),
        "Product_ID": rng.choice(
            products_df["Product_ID"],
            size=n_orders,
        ),
        "Quantity": rng.integers(1, 11, size=n_orders),
        "Discount": rng.choice(
            [0, 0.05, 0.10, 0.15, 0.20],
            size=n_orders,
            p=[0.45, 0.20, 0.20, 0.10, 0.05],
        ),
    }
)

# Récupération du prix de chaque produit
orders_df = orders_df.merge(
    products_df[["Product_ID", "Unit_Price"]],
    on="Product_ID",
    how="left",
    validate="many_to_one",
)

# Calcul du montant brut et du montant net
orders_df["Gross_Amount"] = (
    orders_df["Quantity"] * orders_df["Unit_Price"]
)

orders_df["Net_Amount"] = (
    orders_df["Gross_Amount"] * (1 - orders_df["Discount"])
).round(2)

# Organisation des colonnes
orders_df = orders_df[
    [
        "Order_ID",
        "Order_Date",
        "Customer_ID",
        "Product_ID",
        "Quantity",
        "Unit_Price",
        "Discount",
        "Gross_Amount",
        "Net_Amount",
    ]
]


# ==================================================
# 5. INTRODUCTION D'ANOMALIES CONTRÔLÉES
# ==================================================

# Copie de travail pour préserver les données de référence
orders_raw_df = orders_df.copy()

# Introduction de quelques valeurs manquantes
missing_rows = rng.choice(
    orders_raw_df.index,
    size=10,
    replace=False,
)

orders_raw_df.loc[missing_rows[:5], "Quantity"] = np.nan
orders_raw_df.loc[missing_rows[5:], "Customer_ID"] = np.nan

# Introduction d'un doublon exact
duplicate_row = orders_raw_df.iloc[[100]].copy()

orders_raw_df = pd.concat(
    [orders_raw_df, duplicate_row],
    ignore_index=True,
)

# Introduction de deux quantités invalides
orders_raw_df.loc[200, "Quantity"] = -3
orders_raw_df.loc[201, "Quantity"] = 0

# Export des ventes brutes
orders_raw_df.to_csv(
    DATA_DIR / "orders.csv",
    index=False,
    encoding="utf-8-sig",
    date_format="%Y-%m-%d",
)


# ==================================================
# 6. RÉCAPITULATIF DE LA GÉNÉRATION
# ==================================================

print("=" * 50)
print("GÉNÉRATION DES DONNÉES TERMINÉE")
print("=" * 50)

print(f"Produits générés : {len(products_df)}")
print(f"Clients générés : {len(customers_df)}")
print(f"Lignes de vente générées : {len(orders_raw_df)}")

print(f"\nFichiers enregistrés dans : {DATA_DIR}")

print("\nFichiers créés :")
print("- products.csv")
print("- customers.csv")
print("- orders.csv")
