"""
Visualization Module for Sales Data
Generates executive-ready charts and visual dashboards from analyzed sales data.
"""

from pathlib import Path
from typing import Optional
import matplotlib.pyplot as plt
import pandas as pd


def generate_sales_dashboard(
    cleaned_df: pd.DataFrame,
    product_summary: pd.DataFrame,
    region_summary: pd.DataFrame,
    output_image_path: str = "assets/sales_dashboard.png",
) -> Path:
    """
    Generates a multi-panel visual dashboard showing sales metrics:
    1. Revenue by Product (Horizontal Bar Chart)
    2. Revenue Distribution by Region (Donut Chart)
    3. Daily Revenue Timeline (Line & Area Chart)
    4. Executive Summary KPI Highlights
    """
    out_file = Path(output_image_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    # Setup figure aesthetics
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    fig = plt.figure(figsize=(15, 10), dpi=300)
    fig.patch.set_facecolor("#0f172a")

    # Create a 2x2 grid
    gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.25, top=0.90, bottom=0.08, left=0.08, right=0.95)

    # 1. Product Revenue (Top-Left)
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor("#1e293b")
    products = product_summary.index.tolist()
    revenues = product_summary["total_revenue"].tolist()
    bars = ax1.barh(products, revenues, color="#38bdf8", edgecolor="#0284c7", height=0.6)
    ax1.invert_yaxis()
    ax1.set_title("Revenue by Product ($)", color="#f8fafc", fontsize=13, fontweight="bold", pad=12)
    ax1.tick_params(colors="#cbd5e1", labelsize=10)
    for spine in ax1.spines.values():
        spine.set_color("#334155")
    ax1.grid(color="#334155", linestyle="--", alpha=0.6)
    for bar in bars:
        w = bar.get_width()
        ax1.text(w + max(revenues) * 0.02, bar.get_y() + bar.get_height() / 2, f"${w:,.2f}",
                 va="center", color="#f1f5f9", fontsize=9, fontweight="bold")

    # 2. Regional Revenue Distribution (Top-Right)
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor("#1e293b")
    region_labels = region_summary.index.tolist()
    region_vals = region_summary["total_revenue"].tolist()
    colors = ["#6366f1", "#ec4899", "#10b981", "#f59e0b"][:len(region_labels)]
    wedges, texts, autotexts = ax2.pie(
        region_vals,
        labels=region_labels,
        autopct="%1.1f%%",
        startangle=140,
        colors=colors,
        pctdistance=0.75,
        textprops=dict(color="#f8fafc", fontsize=10, fontweight="bold"),
        wedgeprops=dict(width=0.45, edgecolor="#0f172a", linewidth=2),
    )
    for autotext in autotexts:
        autotext.set_color("#ffffff")
    ax2.set_title("Revenue Share by Region", color="#f8fafc", fontsize=13, fontweight="bold", pad=12)

    # 3. Revenue Trend over Time (Bottom-Left)
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_facecolor("#1e293b")
    timeline = (
        cleaned_df.dropna(subset=["date"])
        .groupby(cleaned_df["date"].dt.strftime("%b %d"))["total_revenue"]
        .sum()
        .reset_index()
    )
    timeline.columns = ["date_str", "rev"]
    ax3.plot(timeline["date_str"], timeline["rev"], marker="o", color="#a855f7", linewidth=2.5, markersize=7)
    ax3.fill_between(range(len(timeline)), timeline["rev"], color="#a855f7", alpha=0.2)
    ax3.set_title("Revenue Timeline (Daily)", color="#f8fafc", fontsize=13, fontweight="bold", pad=12)
    ax3.tick_params(colors="#cbd5e1", labelsize=9)
    ax3.tick_params(axis="x", rotation=30)
    for spine in ax3.spines.values():
        spine.set_color("#334155")
    ax3.grid(color="#334155", linestyle="--", alpha=0.6)

    # 4. Executive Summary KPI Dashboard Cards (Bottom-Right)
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_facecolor("#1e293b")
    ax4.axis("off")
    total_rev = cleaned_df["total_revenue"].sum()
    total_orders = len(cleaned_df)
    total_units = cleaned_df["quantity"].sum()
    avg_order = total_rev / total_orders if total_orders else 0
    top_p = product_summary.index[0] if not product_summary.empty else "N/A"
    top_r = region_summary.index[0] if not region_summary.empty else "N/A"

    kpis = [
        ("Total Revenue", f"${total_rev:,.2f}", "#38bdf8"),
        ("Total Units Sold", f"{int(total_units):,} units", "#10b981"),
        ("Avg Order Value", f"${avg_order:,.2f}", "#f59e0b"),
        ("Top Product", f"{top_p}", "#ec4899"),
        ("Top Region", f"{top_r}", "#a855f7"),
    ]

    ax4.text(0.05, 0.95, "Executive Performance Overview", color="#f8fafc", fontsize=13, fontweight="bold", transform=ax4.transAxes)
    y_pos = 0.78
    for title, val, col in kpis:
        ax4.text(0.05, y_pos, title.upper(), color="#94a3b8", fontsize=8, fontweight="bold", transform=ax4.transAxes)
        ax4.text(0.05, y_pos - 0.08, val, color=col, fontsize=14, fontweight="bold", transform=ax4.transAxes)
        y_pos -= 0.17

    fig.suptitle("Pandas Sales Analysis - Executive Performance Dashboard", color="#ffffff", fontsize=18, fontweight="bold", y=0.96)

    plt.savefig(out_file, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none", bbox_inches="tight")
    plt.close(fig)
    return out_file


if __name__ == "__main__":
    from sales_analyzer import SalesAnalyzer
    analyzer = SalesAnalyzer("sales_data.csv")
    cleaned = analyzer.clean_data(analyzer.load_data())
    prod = analyzer.summarize_by_product(cleaned)
    reg = analyzer.summarize_by_region(cleaned)
    path = generate_sales_dashboard(cleaned, prod, reg)
    print(f"Dashboard successfully generated at: {path}")
