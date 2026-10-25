"""
Pandas Sales Analysis Main Runner
Demonstrates foundational and advanced pandas workflows for data analysis and reporting.
"""

import argparse
import sys
from pathlib import Path
import pandas as pd

# Allow running from project root
sys.path.insert(0, str(Path(__file__).parent))

from src.sales_analyzer import SalesAnalyzer
from src.visualize import generate_sales_dashboard


def run_pipeline(
    input_file: str = "sales_data.csv",
    output_dir: str = ".",
    generate_charts: bool = True,
):
    """
    Executes the complete sales data pipeline:
    1. Loads raw dataset
    2. Identifies missing and irregular values
    3. Cleans and transforms numeric columns
    4. Computes KPIs and aggregates
    5. Exports CSV summaries
    6. Generates visual executive dashboard
    """
    print(f"=== Starting Sales Analysis Pipeline ===")
    print(f"Dataset: {input_file}\n")

    analyzer = SalesAnalyzer(input_file)
    raw_df = analyzer.load_data()

    print("Original rows:", len(raw_df))
    print("\nFirst 5 rows:")
    print(raw_df.head())
    print("\nMissing values:")
    print(raw_df.isnull().sum())

    cleaned_df = analyzer.clean_data(raw_df)
    kpis = analyzer.get_kpis(cleaned_df)
    product_summary = analyzer.summarize_by_product(cleaned_df)
    region_summary = analyzer.summarize_by_region(cleaned_df)

    print("\nCleaned data rows:", len(cleaned_df))
    print(f"\nTotal revenue: ${kpis['total_revenue']:,.2f}")
    print(f"Average order value: ${kpis['avg_order_value']:,.2f}")
    print(f"Total units sold: {kpis['total_units']}")

    print("\nTop products by revenue:")
    print(product_summary)

    print("\nRevenue by region:")
    print(region_summary)

    clean_path, prod_path, reg_path = analyzer.export_results(
        output_dir=output_dir,
        clean_filename="clean_sales_data.csv",
        product_filename="product_summary.csv",
        region_filename="region_summary.csv",
    )

    print(f"\nFiles created: {clean_path.name}, {prod_path.name}, {reg_path.name}")

    if generate_charts:
        chart_path = Path(output_dir) / "assets" / "sales_dashboard.png"
        generate_sales_dashboard(cleaned_df, product_summary, region_summary, str(chart_path))
        print(f"Visual dashboard created: {chart_path}")

    print("\n=== Pipeline Completed Successfully ===")


def main():
    parser = argparse.ArgumentParser(description="Pandas Sales Analysis & Reporting CLI")
    parser.add_argument("--input", default="sales_data.csv", help="Path to input sales CSV")
    parser.add_argument("--output-dir", default=".", help="Directory to save generated CSVs and charts")
    parser.add_argument("--no-charts", action="store_true", help="Skip generating visual dashboard chart")

    args = parser.parse_args()
    run_pipeline(
        input_file=args.input,
        output_dir=args.output_dir,
        generate_charts=not args.no_charts,
    )


if __name__ == "__main__":
    main()
