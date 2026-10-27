
from pathlib import Path
import pandas as pd


# ==================================================
# 1. CONFIGURATION
# ==================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = PROJECT_DIR / "data" / "raw"
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# ==================================================
# 2. CHARGEMENT DES DONNÉES
# ==================================================

orders = pd.read_csv(RAW_DIR / "orders.csv")
products = pd.read_csv(RAW_DIR / "products.csv")
customers = pd.read_csv(RAW_DIR / "customers.csv")

initial_rows = len(orders)

print("=" * 50)
print("NETTOYAGE DES DONNÉES COMMERCIALES")
print("=" * 50)

print(f"\nNombre initial de lignes : {initial_rows}")


# ==================================================
# 3. SUPPRESSION DES DOUBLONS EXACTS
# ==================================================

duplicates_count = orders.duplicated().sum()

orders = orders.drop_duplicates().copy()

print(f"Doublons supprimés : {duplicates_count}")


# ==================================================
# 4. CONVERSION DES TYPES
# ==================================================

orders["Order_Date"] = pd.to_datetime(
    orders["Order_Date"],
    errors="coerce",
)

numeric_columns = [
    "Quantity",
    "Unit_Price",
    "Discount",
    "Gross_Amount",
    "Net_Amount",
]

for column in numeric_columns:
    orders[column] = pd.to_numeric(
        orders[column],
        errors="coerce",
    )


# ==================================================
# 5. CONTRÔLE DES IDENTIFIANTS
# ==================================================

invalid_product_ids = ~orders["Product_ID"].isin(
    products["Product_ID"]
)

invalid_customer_ids = (
    orders["Customer_ID"].notna()
    & ~orders["Customer_ID"].isin(customers["Customer_ID"])
)

print(
    "\nLignes avec un produit inconnu :",
    invalid_product_ids.sum(),
)

print(
    "Lignes avec un client inconnu :",
    invalid_customer_ids.sum(),
)


# ==================================================
# 6. SUPPRESSION DES LIGNES INEXPLOITABLES
# ==================================================

rows_before_validation = len(orders)

required_columns = [
    "Order_ID",
    "Order_Date",
    "Customer_ID",
    "Product_ID",
    "Quantity",
    "Unit_Price",
    "Discount",
]

orders = orders.dropna(
    subset=required_columns
).copy()

missing_rows_removed = (
    rows_before_validation - len(orders)
)

# Les quantités doivent être strictement positives.
orders = orders.loc[
    orders["Quantity"] > 0
].copy()

# Les prix doivent être strictement positifs.
orders = orders.loc[
    orders["Unit_Price"] > 0
].copy()

# La remise doit être comprise entre 0 et 1.
orders = orders.loc[
    orders["Discount"].between(0, 1)
].copy()

# Les produits et les clients doivent exister.
orders = orders.loc[
    ~invalid_product_ids.loc[orders.index]
].copy()

orders = orders.loc[
    ~invalid_customer_ids.loc[orders.index]
].copy()

print(
    "\nLignes supprimées pour données manquantes :",
    missing_rows_removed,
)

print(
    "Lignes restantes après validation :",
    len(orders),
)


# ==================================================
# 7. VALIDATION DES PRIX PAR RAPPORT AU CATALOGUE
# ==================================================

orders = orders.merge(
    products[["Product_ID", "Unit_Price"]].rename(
        columns={"Unit_Price": "Catalog_Unit_Price"}
    ),
    on="Product_ID",
    how="left",
    validate="many_to_one",
)

price_mismatches = (
    orders["Unit_Price"] != orders["Catalog_Unit_Price"]
)

print(
    "\nÉcarts de prix par rapport au catalogue :",
    price_mismatches.sum(),
)

# Le catalogue constitue notre référence pour les prix.
orders["Unit_Price"] = orders["Catalog_Unit_Price"]

orders = orders.drop(
    columns=["Catalog_Unit_Price"]
)


# ==================================================
# 8. RECALCUL DES MONTANTS
# ==================================================

orders["Gross_Amount"] = (
    orders["Quantity"] * orders["Unit_Price"]
)

orders["Net_Amount"] = (
    orders["Gross_Amount"] * (1 - orders["Discount"])
).round(2)


# ==================================================
# 9. NORMALISATION DES TYPES
# ==================================================

orders["Quantity"] = orders["Quantity"].astype(int)

orders["Unit_Price"] = orders["Unit_Price"].astype(int)

orders["Order_Date"] = orders["Order_Date"].dt.strftime(
    "%Y-%m-%d"
)


# ==================================================
# 10. EXPORT DES DONNÉES NETTOYÉES
# ==================================================

orders.to_csv(
    PROCESSED_DIR / "orders_clean.csv",
    index=False,
    encoding="utf-8-sig",
)

products.to_csv(
    PROCESSED_DIR / "products_clean.csv",
    index=False,
    encoding="utf-8-sig",
)

customers.to_csv(
    PROCESSED_DIR / "customers_clean.csv",
    index=False,
    encoding="utf-8-sig",
)

#===================================================
print("\nContrôle des quantités après nettoyage :")

print(
    "Quantités manquantes :",
    orders["Quantity"].isna().sum()
)

print(
    "Quantités nulles ou négatives :",
    (orders["Quantity"] <= 0).sum()
)

print(
    "Quantités non entières :",
    (orders["Quantity"] % 1 != 0).sum()
)

print(
    "Identifiants clients manquants :",
    orders["Customer_ID"].isna().sum()
)

# ==================================================
# 11. BILAN DU NETTOYAGE
# ==================================================

print("\n" + "=" * 50)
print("BILAN DU NETTOYAGE")
print("=" * 50)

print(f"Lignes initiales : {initial_rows}")
print(f"Lignes finales : {len(orders)}")
print(f"Lignes supprimées au total : {initial_rows - len(orders)}")

print(
    "\nValeurs manquantes restantes :",
    orders.isna().sum().sum(),
)

print(
    "Doublons exacts restants :",
    orders.duplicated().sum(),
)

print(
    "\nFichiers nettoyés enregistrés dans :",
    PROCESSED_DIR,
)

print("\nNettoyage terminé.")
