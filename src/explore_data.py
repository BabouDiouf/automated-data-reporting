
from pathlib import Path
import pandas as pd


# ==========================================
# 1. CONFIGURATION
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data" / "raw"


# ==========================================
# 2. CHARGEMENT DES FICHIERS
# ==========================================

orders = pd.read_csv(DATA_DIR / "orders.csv")
products = pd.read_csv(DATA_DIR / "products.csv")
customers = pd.read_csv(DATA_DIR / "customers.csv")


# ==========================================
# 3. EXPLORATION DES DONNÉES
# ==========================================

datasets = {
    "Commandes": orders,
    "Produits": products,
    "Clients": customers,
}

for name, df in datasets.items():

    print("\n" + "=" * 50)
    print(f"EXPLORATION : {name.upper()}")
    print("=" * 50)

    print(f"\nNombre de lignes : {df.shape[0]}")
    print(f"Nombre de colonnes : {df.shape[1]}")

    print("\nNoms des colonnes :")
    print(df.columns.tolist())

    print("\nTypes de données :")
    print(df.dtypes)

    print("\nValeurs manquantes par colonne :")
    print(df.isnull().sum())

    print("\nNombre de doublons exacts :")
    print(df.duplicated().sum())

    print("\nAperçu des cinq premières lignes :")
    print(df.head())


# ==========================================
# 4. CONTRÔLES SPÉCIFIQUES AUX VENTES
# ==========================================

print("\n" + "=" * 50)
print("CONTRÔLES SPÉCIFIQUES AUX COMMANDES")
print("=" * 50)

print(
    "\nNombre de commandes distinctes :",
    orders["Order_ID"].nunique()
)

print(
    "\nQuantités nulles ou négatives :",
    (orders["Quantity"].isna() | (orders["Quantity"] <= 0)).sum()
)

print(
    "\nPrix unitaires nuls ou négatifs :",
    (orders["Unit_Price"] <= 0).sum()
)

print(
    "\nRemises hors limites :",
    (~orders["Discount"].between(0, 1)).sum()
)

print(
    "\nIdentifiants de produits absents du catalogue :",
    (~orders["Product_ID"].isin(products["Product_ID"])).sum()
)

print(
    "\nIdentifiants de clients absents du fichier clients :",
    (
        orders["Customer_ID"].notna()
        & ~orders["Customer_ID"].isin(customers["Customer_ID"])
    ).sum()
)
