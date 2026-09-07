import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "Ecommerce_Sales_Customer_Insights_Dataset.csv"
OUTPUT_DIR = BASE_DIR / "visualizations"
OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA_FILE)
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df = df.drop_duplicates()
df = df.dropna(subset=["Order_ID","Order_Date","Customer_ID","Category","Product","Sales","Profit"])

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order_ID"].nunique()
total_customers = df["Customer_ID"].nunique()
total_quantity = df["Quantity"].sum()
aov = total_sales / total_orders
margin = total_profit / total_sales * 100

print("=" * 55)
print("E-COMMERCE SALES & CUSTOMER INSIGHTS")
print("=" * 55)
print(f"Total Sales         : ₹{total_sales:,.2f}")
print(f"Total Profit        : ₹{total_profit:,.2f}")
print(f"Total Orders        : {total_orders:,}")
print(f"Total Customers     : {total_customers:,}")
print(f"Total Quantity      : {total_quantity:,}")
print(f"Average Order Value : ₹{aov:,.2f}")
print(f"Profit Margin       : {margin:.2f}%")

monthly = df.groupby(df["Order_Date"].dt.to_period("M"))["Sales"].sum()
plt.figure(figsize=(10,6))
plt.plot(monthly.index.astype(str), monthly.values, marker="o")
plt.title("Monthly Sales Trend")
plt.xlabel("Month"); plt.ylabel("Sales (₹)")
plt.xticks(rotation=45); plt.grid(True, alpha=0.3)
plt.tight_layout(); plt.savefig(OUTPUT_DIR/"monthly_sales_trend.png", dpi=300); plt.close()

cat = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
plt.figure(figsize=(9,6))
plt.bar(cat.index, cat.values)
plt.title("Sales by Category")
plt.xlabel("Category"); plt.ylabel("Sales (₹)")
plt.xticks(rotation=20)
plt.tight_layout(); plt.savefig(OUTPUT_DIR/"sales_by_category.png", dpi=300); plt.close()

reg_profit = df.groupby("Region")["Profit"].sum().sort_values(ascending=False)
plt.figure(figsize=(9,6))
plt.bar(reg_profit.index, reg_profit.values)
plt.title("Profit by Region")
plt.xlabel("Region"); plt.ylabel("Profit (₹)")
plt.tight_layout(); plt.savefig(OUTPUT_DIR/"profit_by_region.png", dpi=300); plt.close()

top = df.groupby("Product")["Sales"].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10,7))
plt.barh(top.index[::-1], top.values[::-1])
plt.title("Top 10 Products by Sales")
plt.xlabel("Sales (₹)"); plt.ylabel("Product")
plt.tight_layout(); plt.savefig(OUTPUT_DIR/"top_10_products.png", dpi=300); plt.close()

pd.DataFrame({
    "Metric":["Total Sales","Total Profit","Total Orders","Total Customers","Total Quantity","Average Order Value","Profit Margin"],
    "Value":[total_sales,total_profit,total_orders,total_customers,total_quantity,aov,margin]
}).to_csv(OUTPUT_DIR/"project_kpi_summary.csv", index=False)

cat.rename("Sales").reset_index().to_csv(OUTPUT_DIR/"category_sales_analysis.csv", index=False)
df.groupby("Region").agg(Sales=("Sales","sum"),Profit=("Profit","sum"),Orders=("Order_ID","nunique")).sort_values("Sales",ascending=False).to_csv(OUTPUT_DIR/"region_analysis.csv")
top.rename("Sales").reset_index().to_csv(OUTPUT_DIR/"top_products_analysis.csv", index=False)

print("\nAnalysis completed. Files saved in:", OUTPUT_DIR)
