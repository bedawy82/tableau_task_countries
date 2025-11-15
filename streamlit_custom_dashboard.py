import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# -----------------------------------------------------
# Load Data
# -----------------------------------------------------
csv_path = Path(__file__).parent / "cleaned_tableau_input.csv"
df = pd.read_csv(csv_path)

# -----------------------------------------------------
# Beautiful Page Config
# -----------------------------------------------------
st.set_page_config(
    page_title="Business Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------
# CSS Styling (Professional Look)
# -----------------------------------------------------
st.markdown("""
<style>

html, body, [class*="css"]  {
    font-family: 'Segoe UI', sans-serif;
}

/* KPI Card */
.card {
    background: linear-gradient(135deg, #0066ff 0%, #00c6ff 100%);
    padding: 25px;
    border-radius: 18px;
    color: white;
    text-align: center;
    font-size: 22px;
    font-weight: bold;
    box-shadow: 0 7px 20px rgba(0,0,0,0.15);
}

.card_small {
    font-size: 14px;
    opacity: 0.85;
}

/* Title Styling */
.big-title {
    font-size: 38px;
    font-weight: 700;
    text-shadow: 1px 1px 4px rgba(0,0,0,0.15);
}

/* Section Subtitle */
.section-title {
    padding: 8px 0;
    font-size: 23px;
    font-weight: 600;
    color: #003366;
}

/* Transition on cards */
.card:hover {
    transform: scale(1.03);
    transition: 0.2s ease-in-out;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------
# Header
# -----------------------------------------------------
st.markdown("<div class='big-title'>📊 Business Performance Dashboard</div>", unsafe_allow_html=True)
st.write("Interactive dashboard with filters, animations, and business insights.")

# -----------------------------------------------------
# Sidebar Filters
# -----------------------------------------------------
st.sidebar.header("🔍 Filters")

cats = sorted(df['Category'].dropna().unique()) if 'Category' in df.columns else []
regions = sorted(df['Region'].dropna().unique()) if 'Region' in df.columns else []

selected_cats = st.sidebar.multiselect("Category", cats, default=cats)
selected_regions = st.sidebar.multiselect("Region", regions, default=regions)

dff = df.copy()

if selected_cats:
    dff = dff[dff['Category'].isin(selected_cats)]
if selected_regions:
    dff = dff[dff['Region'].isin(selected_regions)]

# -----------------------------------------------------
# KPIs — Styled Cards
# -----------------------------------------------------
total_sales = dff['Sales'].sum() if 'Sales' in dff.columns else 0
total_profit = dff['Profit'].sum() if 'Profit' in dff.columns else 0
total_orders = len(dff)

col1, col2, col3 = st.columns(3)

col1.markdown(f"""
<div class='card'>
    ${total_sales:,.2f}
    <div class='card_small'>Total Sales</div>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div class='card'>
    ${total_profit:,.2f}
    <div class='card_small'>Total Profit</div>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div class='card'>
    {total_orders:,}
    <div class='card_small'>Orders</div>
</div>
""", unsafe_allow_html=True)

st.write("")  # spacing

# -----------------------------------------------------
# Animated Bar Chart – Sales by Category
# -----------------------------------------------------
st.markdown("<div class='section-title'>📦 Sales by Category (Animated)</div>", unsafe_allow_html=True)

if 'Category' in dff.columns:
    animated_bar = px.bar(
        dff,
        x="Category",
        y="Sales",
        animation_frame="Order_Month" if "Order_Month" in dff.columns else None,
        title="Sales by Category (Animated by Month)",
        color="Category"
    )
    st.plotly_chart(animated_bar, use_container_width=True)

# -----------------------------------------------------
# Animated Line Chart – Sales Trend
# -----------------------------------------------------
st.markdown("<div class='section-title'>📈 Sales Trend Over Time (Animated)</div>", unsafe_allow_html=True)

if "Order_Month" in dff.columns:
    animated_line = px.line(
        dff,
        x="Order_Month",
        y="Sales",
        color="Category" if "Category" in dff.columns else None,
        animation_frame="Order_Month",
        title="Sales Trend (Animated)"
    )
    st.plotly_chart(animated_line, use_container_width=True)

# -----------------------------------------------------
# Top Products – Table
# -----------------------------------------------------
st.markdown("<div class='section-title'>🏆 Top 15 Products</div>", unsafe_allow_html=True)

if "Product_Name" in dff.columns:
    top_products = (
        dff.groupby("Product_Name", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
        .head(15)
    )
    st.table(top_products)
