import pandas as pd

# Load the raw dataset
sales_df = pd.read_csv("sales_data.csv")

print("Original rows:", len(sales_df))
print("\nFirst 5 rows:")
print(sales_df.head())
print("\nMissing values:")
print(sales_df.isnull().sum())

# Convert numeric fields to numbers and handle missing values
sales_df["quantity"] = pd.to_numeric(sales_df["quantity"], errors="coerce")
sales_df["unit_price"] = pd.to_numeric(sales_df["unit_price"], errors="coerce")

# Remove rows with required information missing
sales_df = sales_df.dropna(subset=["customer_name", "date", "quantity", "unit_price"]).copy()

# Create a revenue column
sales_df["total_revenue"] = sales_df["quantity"] * sales_df["unit_price"]

# Keep it simple: summarize by product
product_summary = (
    sales_df.groupby("product")
    .agg(total_revenue=("total_revenue", "sum"), total_units=("quantity", "sum"))
    .sort_values("total_revenue", ascending=False)
)

# Region summary
region_summary = (
    sales_df.groupby("region")["total_revenue"].sum().sort_values(ascending=False)
)

print("\nCleaned data rows:", len(sales_df))
print("\nTotal revenue:", round(sales_df["total_revenue"].sum(), 2))
print("\nTop products by revenue:")
print(product_summary)
print("\nRevenue by region:")
print(region_summary)

# Save cleaned outputs
sales_df.to_csv("clean_sales_data.csv", index=False)
product_summary.to_csv("product_summary.csv")
region_summary.to_csv("region_summary.csv")

print("\nFiles created: clean_sales_data.csv, product_summary.csv, region_summary.csv")
