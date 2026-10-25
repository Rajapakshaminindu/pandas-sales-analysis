"""
Unit tests for SalesAnalyzer and data pipeline.
"""

import tempfile
from pathlib import Path
import pytest
import pandas as pd

from src.sales_analyzer import SalesAnalyzer


@pytest.fixture
def sample_sales_data():
    """Provides a synthetic sales dataframe with clean and messy rows."""
    data = {
        "order_id": [1, 2, 3, 4, 5],
        "customer_name": ["Alice", "Bob", None, "David", "Eve"],
        "product": ["Laptop", "Mouse", "Keyboard", "Laptop", "Monitor"],
        "region": ["North", "South", "East", "North", "West"],
        "quantity": ["2", "5", "1", None, "1"],
        "unit_price": [800.0, 20.0, 50.0, 800.0, 300.0],
        "date": ["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04", None],
    }
    return pd.DataFrame(data)


def test_clean_data_removes_invalid_rows(sample_sales_data):
    analyzer = SalesAnalyzer()
    cleaned = analyzer.clean_data(sample_sales_data)

    # Row 3 has missing customer_name
    # Row 4 has missing quantity
    # Row 5 has missing date
    # Only rows 1 and 2 should remain
    assert len(cleaned) == 2
    assert "total_revenue" in cleaned.columns
    # Row 1: 2 * 800 = 1600; Row 2: 5 * 20 = 100
    expected_revenues = [1600.0, 100.0]
    assert list(cleaned["total_revenue"]) == expected_revenues


def test_kpi_calculation(sample_sales_data):
    analyzer = SalesAnalyzer()
    cleaned = analyzer.clean_data(sample_sales_data)
    kpis = analyzer.get_kpis(cleaned)

    assert kpis["total_revenue"] == 1700.0
    assert kpis["total_units"] == 7
    assert kpis["total_orders"] == 2
    assert kpis["avg_order_value"] == 850.0
    assert kpis["top_product"] == "Laptop"
    assert kpis["top_region"] == "North"


def test_summarize_by_product(sample_sales_data):
    analyzer = SalesAnalyzer()
    cleaned = analyzer.clean_data(sample_sales_data)
    summary = analyzer.summarize_by_product(cleaned)

    assert "total_revenue" in summary.columns
    assert "total_units" in summary.columns
    assert summary.loc["Laptop", "total_revenue"] == 1600.0
    assert summary.loc["Laptop", "total_units"] == 2
    assert summary.loc["Mouse", "total_revenue"] == 100.0


def test_summarize_by_region(sample_sales_data):
    analyzer = SalesAnalyzer()
    cleaned = analyzer.clean_data(sample_sales_data)
    summary = analyzer.summarize_by_region(cleaned)

    assert summary.loc["North", "total_revenue"] == 1600.0
    assert summary.loc["South", "total_revenue"] == 100.0


def test_export_results(sample_sales_data):
    analyzer = SalesAnalyzer()
    analyzer.clean_data(sample_sales_data)

    with tempfile.TemporaryDirectory() as tmp_dir:
        clean_p, prod_p, reg_p = analyzer.export_results(output_dir=tmp_dir)

        assert Path(clean_p).exists()
        assert Path(prod_p).exists()
        assert Path(reg_p).exists()

        df_loaded = pd.read_csv(clean_p)
        assert len(df_loaded) == 2


def test_missing_file_raises_error():
    analyzer = SalesAnalyzer("non_existent_file.csv")
    with pytest.raises(FileNotFoundError):
        analyzer.load_data()
