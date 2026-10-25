"""
Sales Data Analyzer Module
Provides data cleaning, transformation, aggregation, and reporting for retail sales datasets.
"""

from pathlib import Path
from typing import Dict, Any, Tuple, Optional
import pandas as pd


class SalesAnalyzer:
    """A production-grade sales data processor and analyzer using Pandas."""

    REQUIRED_COLUMNS = ["customer_name", "date", "quantity", "unit_price", "product", "region"]

    def __init__(self, data_path: Optional[str] = None):
        """
        Initialize the analyzer.
        
        Args:
            data_path: Optional path to the CSV dataset.
        """
        self.data_path = Path(data_path) if data_path else None
        self.raw_df: Optional[pd.DataFrame] = None
        self.cleaned_df: Optional[pd.DataFrame] = None

    def load_data(self, file_path: Optional[str] = None) -> pd.DataFrame:
        """
        Loads CSV dataset into a pandas DataFrame.
        
        Args:
            file_path: Path to the CSV file. If None, uses self.data_path.
            
        Returns:
            pd.DataFrame: Loaded raw dataset.
        """
        path = Path(file_path) if file_path else self.data_path
        if not path or not path.exists():
            raise FileNotFoundError(f"Dataset not found at: {path}")

        self.raw_df = pd.read_csv(path)
        return self.raw_df

    def clean_data(self, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Cleans sales data by casting numeric columns, parsing dates,
        and filtering out missing mandatory fields.
        
        Args:
            df: Optional DataFrame to clean. Defaults to self.raw_df.
            
        Returns:
            pd.DataFrame: Cleaned and enriched dataset with total_revenue column.
        """
        if df is None:
            if self.raw_df is None:
                raise ValueError("No data loaded. Call load_data() first.")
            df = self.raw_df.copy()
        else:
            df = df.copy()

        # Ensure numeric fields are properly parsed
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
        df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

        # Parse date field
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")

        # Drop rows with missing values in critical columns
        required = [col for col in self.REQUIRED_COLUMNS if col in df.columns]
        cleaned = df.dropna(subset=required).copy()

        # Calculate revenue
        cleaned["total_revenue"] = cleaned["quantity"] * cleaned["unit_price"]

        self.cleaned_df = cleaned
        return self.cleaned_df

    def get_kpis(self, df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
        """
        Calculates key performance indicators (KPIs) for the dataset.
        
        Args:
            df: Cleaned sales DataFrame.
            
        Returns:
            dict: Summary metrics including total revenue, orders, units sold, and top performers.
        """
        target_df = self._get_target_df(df)
        if target_df.empty:
            return {
                "total_revenue": 0.0,
                "total_units": 0,
                "total_orders": 0,
                "avg_order_value": 0.0,
                "top_product": None,
                "top_region": None,
            }

        total_rev = round(float(target_df["total_revenue"].sum()), 2)
        total_units = int(target_df["quantity"].sum())
        total_orders = len(target_df)
        avg_order = round(total_rev / total_orders, 2) if total_orders > 0 else 0.0

        top_prod = target_df.groupby("product")["total_revenue"].sum().idxmax()
        top_reg = target_df.groupby("region")["total_revenue"].sum().idxmax()

        return {
            "total_revenue": total_rev,
            "total_units": total_units,
            "total_orders": total_orders,
            "avg_order_value": avg_order,
            "top_product": top_prod,
            "top_region": top_reg,
        }

    def summarize_by_product(self, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Groups data by product, aggregating revenue and units sold.
        """
        target_df = self._get_target_df(df)
        return (
            target_df.groupby("product")
            .agg(total_revenue=("total_revenue", "sum"), total_units=("quantity", "sum"))
            .sort_values("total_revenue", ascending=False)
            .round({"total_revenue": 2, "total_units": 0})
        )

    def summarize_by_region(self, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Groups data by region, aggregating total revenue.
        """
        target_df = self._get_target_df(df)
        return (
            target_df.groupby("region")["total_revenue"]
            .sum()
            .sort_values(ascending=False)
            .round(2)
            .to_frame(name="total_revenue")
        )

    def summarize_by_date(self, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Groups data by date for time-series trend analysis.
        """
        target_df = self._get_target_df(df)
        if "date" not in target_df.columns:
            raise KeyError("Column 'date' not present in dataset.")

        return (
            target_df.groupby(target_df["date"].dt.date)["total_revenue"]
            .sum()
            .round(2)
            .to_frame(name="daily_revenue")
        )

    def export_results(
        self,
        output_dir: str = ".",
        clean_filename: str = "clean_sales_data.csv",
        product_filename: str = "product_summary.csv",
        region_filename: str = "region_summary.csv",
    ) -> Tuple[Path, Path, Path]:
        """
        Exports cleaned data and summary tables to CSV.
        """
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)

        target_df = self._get_target_df()
        prod_df = self.summarize_by_product(target_df)
        reg_df = self.summarize_by_region(target_df)

        clean_path = out_path / clean_filename
        prod_path = out_path / product_filename
        reg_path = out_path / region_filename

        target_df.to_csv(clean_path, index=False)
        prod_df.to_csv(prod_path)
        reg_df.to_csv(reg_path)

        return clean_path, prod_path, reg_path

    def _get_target_df(self, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        if df is not None:
            return df
        if self.cleaned_df is not None:
            return self.cleaned_df
        if self.raw_df is not None:
            return self.clean_data()
        raise ValueError("No sales data available. Load or pass a DataFrame.")
