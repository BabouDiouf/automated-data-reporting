
from pathlib import Path
import pandas as pd


# ==================================================
# 1. CONFIGURATION
# ==================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_DIR / "data" / "processed"
OUTPUT_DIR = PROJECT_DIR / "reports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ==================================================
# 2. CHARGEMENT DES DONNÉES NETTOYÉES
# ==================================================

orders = pd.read_csv(DATA_DIR / "orders_clean.csv")
products = pd.read_csv(DATA_DIR / "products_clean.csv")
customers = pd.read_csv(DATA_DIR / "customers_clean.csv")

orders["Order_Date"] = pd.to_datetime(orders["Order_Date"])


# ==================================================
# 3. ENRICHISSEMENT DES DONNÉES
# ==================================================

# Ajout des informations sur les produits
sales = orders.merge(
    products[["Product_ID", "Product_Name", "Category"]],
    on="Product_ID",
    how="left",
    validate="many_to_one",
)

# Ajout des informations sur les clients
sales = sales.merge(
    customers[["Customer_ID", "City", "Region"]],
    on="Customer_ID",
    how="left",
    validate="many_to_one",
)

# Création d'une colonne correspondant au mois
sales["Month"] = sales["Order_Date"].dt.to_period("M").astype(str)


# ==================================================
# 4. CALCUL DES KPI GÉNÉRAUX
# ==================================================

total_revenue = sales["Net_Amount"].sum()
gross_revenue = sales["Gross_Amount"].sum()

total_discounts = gross_revenue - total_revenue

total_orders = sales["Order_ID"].nunique()
total_quantity = sales["Quantity"].sum()

average_order_value = (
    total_revenue / total_orders if total_orders else 0
)

average_selling_price = (
    total_revenue / total_quantity if total_quantity else 0
)

average_discount = sales["Discount"].mean() * 100

kpi = pd.DataFrame(
    {
        "Indicateur": [
            "Chiffre d'affaires net",
            "Chiffre d'affaires brut",
            "Montant total des remises",
            "Nombre de commandes",
            "Quantité totale vendue",
            "Panier moyen",
            "Prix moyen par unité vendue",
            "Taux moyen de remise (%)",
        ],
        "Valeur": [
            round(total_revenue, 2),
            round(gross_revenue, 2),
            round(total_discounts, 2),
            total_orders,
            total_quantity,
            round(average_order_value, 2),
            round(average_selling_price, 2),
            round(average_discount, 2),
        ],
    }
)


# ==================================================
# 5. ANALYSE PAR CATÉGORIE
# ==================================================

sales_by_category = (
    sales.groupby("Category", as_index=False)
    .agg(
        Chiffre_Affaires=("Net_Amount", "sum"),
        Quantite_Vendue=("Quantity", "sum"),
        Nombre_Commandes=("Order_ID", "nunique"),
    )
    .sort_values("Chiffre_Affaires", ascending=False)
)

sales_by_category["Part_CA_%"] = (
    sales_by_category["Chiffre_Affaires"]
    / total_revenue
    * 100
).round(2)


# ==================================================
# 6. ANALYSE PAR RÉGION
# ==================================================

sales_by_region = (
    sales.groupby("Region", as_index=False)
    .agg(
        Chiffre_Affaires=("Net_Amount", "sum"),
        Quantite_Vendue=("Quantity", "sum"),
        Nombre_Commandes=("Order_ID", "nunique"),
    )
    .sort_values("Chiffre_Affaires", ascending=False)
)


# ==================================================
# 7. TOP 10 DES PRODUITS
# ==================================================

top_products = (
    sales.groupby(
        ["Product_ID", "Product_Name", "Category"],
        as_index=False,
    )
    .agg(
        Chiffre_Affaires=("Net_Amount", "sum"),
        Quantite_Vendue=("Quantity", "sum"),
        Nombre_Commandes=("Order_ID", "nunique"),
    )
    .sort_values("Chiffre_Affaires", ascending=False)
    .head(10)
)


# ==================================================
# 8. ÉVOLUTION MENSUELLE
# ==================================================

monthly_sales = (
    sales.groupby("Month", as_index=False)
    .agg(
        Chiffre_Affaires=("Net_Amount", "sum"),
        Nombre_Commandes=("Order_ID", "nunique"),
        Quantite_Vendue=("Quantity", "sum"),
    )
    .sort_values("Month")
)

monthly_sales["Evolution_CA_%"] = (
    monthly_sales["Chiffre_Affaires"]
    .pct_change()
    .mul(100)
    .round(2)
)


# ==================================================
# 9. EXPORT DES RÉSULTATS
# ==================================================

kpi.to_csv(
    OUTPUT_DIR / "kpi_summary.csv",
    index=False,
    encoding="utf-8-sig",
)

sales_by_category.to_csv(
    OUTPUT_DIR / "sales_by_category.csv",
    index=False,
    encoding="utf-8-sig",
)

sales_by_region.to_csv(
    OUTPUT_DIR / "sales_by_region.csv",
    index=False,
    encoding="utf-8-sig",
)

top_products.to_csv(
    OUTPUT_DIR / "top_10_products.csv",
    index=False,
    encoding="utf-8-sig",
)

monthly_sales.to_csv(
    OUTPUT_DIR / "monthly_sales.csv",
    index=False,
    encoding="utf-8-sig",
)


# ==================================================
# 10. AFFICHAGE DES RÉSULTATS
# ==================================================

print("=" * 50)
print("ANALYSE COMMERCIALE DE SUNU MARKET")
print("=" * 50)

print("\nINDICATEURS GÉNÉRAUX")
#print(kpi.to_string(index=False))
print(
    kpi.to_string(
        index=False,
        formatters={
            "Valeur": lambda valeur: f"{valeur:,.2f}"
        },
    )
)

print("\nCHIFFRE D'AFFAIRES PAR CATÉGORIE")
print(sales_by_category.to_string(index=False))

print("\nTOP 10 DES PRODUITS")
print(top_products.to_string(index=False))

print("\nÉVOLUTION MENSUELLE")
print(monthly_sales.to_string(index=False))

print("\nLes résultats ont été enregistrés dans :")
print(OUTPUT_DIR)
