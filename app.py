"""
Interactive Sales Analysis Dashboard (Streamlit App)
Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
from pathlib import Path
from src.sales_analyzer import SalesAnalyzer
from src.visualize import generate_sales_dashboard

st.set_page_config(
    page_title="Pandas Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📊 Retail Sales Analytics Dashboard")
st.markdown("Interactive exploratory data analysis, KPI monitoring, and regional sales performance.")

# Sidebar
st.sidebar.header("📁 Data Source & Filters")
data_source = st.sidebar.radio("Data Source", ["Use Sample Data (sales_data.csv)", "Upload CSV"], index=0)

analyzer = SalesAnalyzer()

if data_source == "Upload CSV":
    uploaded = st.sidebar.file_uploader("Upload sales CSV", type=["csv"])
    if uploaded is not None:
        raw_df = pd.read_csv(uploaded)
    else:
        st.info("Please upload a CSV file or switch to sample data.")
        st.stop()
else:
    sample_path = Path("sales_data.csv")
    if sample_path.exists():
        raw_df = analyzer.load_data(str(sample_path))
    else:
        st.error("sales_data.csv not found in the project root.")
        st.stop()

# Clean data
cleaned_df = analyzer.clean_data(raw_df)

# Filters
all_regions = sorted(cleaned_df["region"].unique().tolist())
selected_regions = st.sidebar.multiselect("Filter by Region", options=all_regions, default=all_regions)

all_products = sorted(cleaned_df["product"].unique().tolist())
selected_products = st.sidebar.multiselect("Filter by Product", options=all_products, default=all_products)

# Apply filters
filtered_df = cleaned_df[
    (cleaned_df["region"].isin(selected_regions)) &
    (cleaned_df["product"].isin(selected_products))
]

if filtered_df.empty:
    st.warning("No records match the selected filters.")
    st.stop()

# Top KPIs
kpis = analyzer.get_kpis(filtered_df)
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Revenue", f"${kpis['total_revenue']:,.2f}")
c2.metric("Orders", f"{kpis['total_orders']}")
c3.metric("Units Sold", f"{kpis['total_units']:,}")
c4.metric("Avg Order Value", f"${kpis['avg_order_value']:,.2f}")
c5.metric("Top Product", f"{kpis['top_product']}")

st.divider()

tab1, tab2, tab3 = st.tabs(["📈 Visual Dashboard", "📋 Cleaned Records", "📑 Summaries & Exports"])

with tab1:
    prod_summary = analyzer.summarize_by_product(filtered_df)
    reg_summary = analyzer.summarize_by_region(filtered_df)

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("Revenue by Product")
        st.bar_chart(prod_summary["total_revenue"], color="#38bdf8")

    with col_right:
        st.subheader("Revenue by Region")
        st.bar_chart(reg_summary["total_revenue"], color="#818cf8")

    st.subheader("Daily Sales Trend")
    daily_rev = filtered_df.groupby(filtered_df["date"].dt.date)["total_revenue"].sum()
    st.line_chart(daily_rev, color="#ec4899")

with tab2:
    st.subheader("Dataset Preview")
    col_a, col_b = st.columns(2)
    col_a.write(f"**Cleaned Records Count:** {len(filtered_df)}")
    col_b.write(f"**Original Raw Count:** {len(raw_df)}")
    st.dataframe(filtered_df, use_container_width=True)

    csv_data = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Cleaned CSV", data=csv_data, file_name="clean_sales_data.csv", mime="text/csv")

with tab3:
    col_p, col_r = st.columns(2)
    with col_p:
        st.subheader("Product Summary")
        prod_tbl = analyzer.summarize_by_product(filtered_df)
        st.dataframe(prod_tbl, use_container_width=True)
        st.download_button("📥 Download Product Summary", data=prod_tbl.to_csv().encode("utf-8"), file_name="product_summary.csv", mime="text/csv")

    with col_r:
        st.subheader("Region Summary")
        reg_tbl = analyzer.summarize_by_region(filtered_df)
        st.dataframe(reg_tbl, use_container_width=True)
        st.download_button("📥 Download Region Summary", data=reg_tbl.to_csv().encode("utf-8"), file_name="region_summary.csv", mime="text/csv")
