
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# ==========================================
# 1. CONFIGURATION
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_DIR / "data" / "processed"
REPORTS_DIR = PROJECT_DIR / "reports"

CHARTS_DIR = PROJECT_DIR / "outputs" / "charts"
CHARTS_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid")


# ==========================================
# 2. CHARGEMENT DES DONNÉES
# ==========================================

orders = pd.read_csv(DATA_DIR / "orders_clean.csv")
products = pd.read_csv(DATA_DIR / "products_clean.csv")
customers = pd.read_csv(DATA_DIR / "customers_clean.csv")

orders["Order_Date"] = pd.to_datetime(orders["Order_Date"])

sales = orders.merge(
    products[["Product_ID", "Product_Name", "Category"]],
    on="Product_ID",
    how="left",
    validate="many_to_one",
)

sales = sales.merge(
    customers[["Customer_ID", "City", "Region"]],
    on="Customer_ID",
    how="left",
    validate="many_to_one",
)

sales["Month"] = sales["Order_Date"].dt.to_period("M").astype(str)


# ==========================================
# 3. CHIFFRE D'AFFAIRES MENSUEL
# ==========================================

monthly_sales = (
    sales.groupby("Month", as_index=False)["Net_Amount"]
    .sum()
    .sort_values("Month")
)

plt.figure(figsize=(12, 6))

sns.lineplot(
    data=monthly_sales,
    x="Month",
    y="Net_Amount",
    marker="o",
)

plt.title("Évolution mensuelle du chiffre d'affaires")
plt.xlabel("Mois")
plt.ylabel("Chiffre d'affaires net (FCFA)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    CHARTS_DIR / "monthly_revenue.png",
    dpi=300,
    bbox_inches="tight",
)

plt.close()


# ==========================================
# 4. CHIFFRE D'AFFAIRES PAR CATÉGORIE
# ==========================================

category_sales = (
    sales.groupby("Category", as_index=False)["Net_Amount"]
    .sum()
    .sort_values("Net_Amount", ascending=False)
)

plt.figure(figsize=(10, 6))

sns.barplot(
    data=category_sales,
    x="Net_Amount",
    y="Category",
)

plt.title("Chiffre d'affaires par catégorie")
plt.xlabel("Chiffre d'affaires net (FCFA)")
plt.ylabel("Catégorie")
plt.tight_layout()

plt.savefig(
    CHARTS_DIR / "revenue_by_category.png",
    dpi=300,
    bbox_inches="tight",
)

plt.close()


# ==========================================
# 5. TOP 10 DES PRODUITS
# ==========================================

top_products = (
    sales.groupby("Product_Name", as_index=False)["Net_Amount"]
    .sum()
    .nlargest(10, "Net_Amount")
    .sort_values("Net_Amount")
)

plt.figure(figsize=(12, 7))

sns.barplot(
    data=top_products,
    x="Net_Amount",
    y="Product_Name",
)

plt.title("Top 10 des produits par chiffre d'affaires")
plt.xlabel("Chiffre d'affaires net (FCFA)")
plt.ylabel("Produit")
plt.tight_layout()

plt.savefig(
    CHARTS_DIR / "top_10_products.png",
    dpi=300,
    bbox_inches="tight",
)

plt.close()


# ==========================================
# 6. CHIFFRE D'AFFAIRES PAR RÉGION
# ==========================================

region_sales = (
    sales.groupby("Region", as_index=False)["Net_Amount"]
    .sum()
    .sort_values("Net_Amount", ascending=False)
)

plt.figure(figsize=(12, 7))

sns.barplot(
    data=region_sales,
    x="Net_Amount",
    y="Region",
)

plt.title("Chiffre d'affaires par région")
plt.xlabel("Chiffre d'affaires net (FCFA)")
plt.ylabel("Région")
plt.tight_layout()

plt.savefig(
    CHARTS_DIR / "revenue_by_region.png",
    dpi=300,
    bbox_inches="tight",
)

plt.close()


# ==========================================
# 7. BILAN
# ==========================================

print("=" * 50)
print("GÉNÉRATION DES GRAPHIQUES TERMINÉE")
print("=" * 50)

for chart in CHARTS_DIR.glob("*.png"):
    print(f"Graphique créé : {chart.name}")

print(f"\nDossier de sortie : {CHARTS_DIR}")
