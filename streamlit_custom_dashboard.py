# streamlit_custom_dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from io import BytesIO

# ---------------------------
# Configuration & Styling
# ---------------------------
st.set_page_config(page_title="Custom BI Dashboard", layout="wide", initial_sidebar_state="expanded")

# Simple CSS for modern blue look
st.markdown("""
<style>
html, body, [class*="css"] { font-family: "Segoe UI", Roboto, sans-serif; }
.header { font-size:28px; font-weight:700; color:#012a4a; }
.kpi { background: linear-gradient(135deg,#0061ff 0%, #00c6ff 100%); color:white; padding:18px; border-radius:12px; box-shadow:0 5px 18px rgba(0,0,0,0.08); text-align:center;}
.kpi_small { font-size:14px; opacity:0.9;}
.section_title { font-size:20px; color:#012a4a; font-weight:600; margin-bottom:8px;}
.card { padding:12px; border-radius:10px; background: white; box-shadow: 0 4px 12px rgba(2,6,23,0.06); }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='header'>📊 Custom BI Dashboard — Modern Blue Theme</div>", unsafe_allow_html=True)
st.write("Multi-page dashboard • Maps • Category Analysis • Auto Path + Upload • Export")

# ---------------------------
# Data Loading (Auto-detect + Upload)
# ---------------------------
@st.cache_data(ttl=600)
def load_data_from_path(p):
    return pd.read_csv(p)

def try_auto_load():
    local_path = Path(__file__).parent / "cleaned_tableau_input.csv"
    win_path = Path(r"C:\Data Analysis\DEPI_R3\tableau_task_outputs\cleaned_tableau_input.csv")
    cloud_path = Path("/mount/src/tableau_task_countries/cleaned_tableau_input.csv")
    for p in (local_path, win_path, cloud_path):
        if p.exists():
            try:
                return load_data_from_path(p), str(p)
            except Exception:
                continue
    return None, None

uploaded_file = st.sidebar.file_uploader("Upload CSV (optional)", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    source_label = "Uploaded file"
else:
    auto_df, auto_path = try_auto_load()
    if auto_df is not None:
        df = auto_df
        source_label = auto_path
    else:
        st.sidebar.error("No CSV found. Upload a CSV or place cleaned_tableau_input.csv next to the script.")
        st.stop()

df = df.copy()

# Normalize column names
df.columns = [c.strip() for c in df.columns]

# detect important columns
def find_col(df, candidates):
    for c in candidates:
        for col in df.columns:
            if col.lower() == c.lower():
                return col
    for c in candidates:
        for col in df.columns:
            if c.lower() in col.lower():
                return col
    return None

country_col = find_col(df, ["Country", "Region"])
sales_col = find_col(df, ["Sales", "Revenue", "Amount"])
profit_col = find_col(df, ["Profit", "NetProfit"])
category_col = find_col(df, ["Category", "Product Category"])
product_col = find_col(df, ["Product", "Product_Name", "Item"])

# ensure numeric metrics
for metric in (sales_col, profit_col):
    if metric and metric in df.columns:
        df[metric] = pd.to_numeric(df[metric].astype(str).str.replace(',','').str.replace('$',''), errors='coerce')

# ---------------------------
# Sidebar - Navigation + Filters
# ---------------------------
st.sidebar.markdown("### Navigation")
page = st.sidebar.radio("", ["Overview", "Map", "Category Analysis", "Data & Export"])

st.sidebar.markdown("---")
st.sidebar.markdown("### Filters")

# category filter
if category_col:
    categories = sorted(df[category_col].dropna().unique().astype(str))
    sel_categories = st.sidebar.multiselect("Category", options=categories, default=categories)
else:
    sel_categories = []

# country filter
if country_col:
    countries = sorted(df[country_col].dropna().unique().astype(str))
    sel_countries = st.sidebar.multiselect("Country", options=countries, default=countries)
else:
    sel_countries = []

# apply filters
dff = df.copy()
if category_col and sel_categories:
    dff = dff[dff[category_col].astype(str).isin(sel_categories)]
if country_col and sel_countries:
    dff = dff[dff[country_col].astype(str).isin(sel_countries)]

# ---------------------------
# Export helpers
# ---------------------------
def to_excel_bytes(df_to_save):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df_to_save.to_excel(writer, index=False, sheet_name="data")
    return output.getvalue()

def to_csv_bytes(df_to_save):
    return df_to_save.to_csv(index=False).encode("utf-8")

def fig_to_html_bytes(fig):
    return fig.to_html(full_html=True, include_plotlyjs="cdn").encode("utf-8")

# ---------------------------
# KPI Section
# ---------------------------
def show_kpis(d):
    profit = d[profit_col].sum() if profit_col else 0
    num_countries = d[country_col].nunique() if country_col else 0

    # top 10 products or categories
    if product_col and sales_col and product_col in d.columns:
        top10 = d.groupby(product_col, as_index=False)[sales_col].sum().sort_values(sales_col, ascending=False).head(10)
    elif category_col and sales_col:
        top10 = d.groupby(category_col, as_index=False)[sales_col].sum().sort_values(sales_col, ascending=False).head(10)
    else:
        top10 = None

    c1, c2, c3 = st.columns([1,1,1])
    c1.markdown(f"<div class='kpi'><div>Total Profit</div><div style='font-size:22px;font-weight:700'>${profit:,.2f}</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='kpi'><div># Countries</div><div style='font-size:22px;font-weight:700'>{num_countries}</div></div>", unsafe_allow_html=True)

    if top10 is not None:
        c3.markdown("<div class='card'><b>Top 10 Items</b>" + top10.to_html(index=False, classes='table') + "</div>", unsafe_allow_html=True)
    else:
        c3.markdown("<div class='card'>Top 10 Items unavailable</div>", unsafe_allow_html=True)

# ---------------------------
# Pages
# ---------------------------

# --- Overview ---
if page == "Overview":
    st.markdown("<div class='section_title'>Overview</div>", unsafe_allow_html=True)
    show_kpis(dff)

    st.markdown("### Category Snapshot")
    if sales_col and category_col:
        snap = dff.groupby(category_col, as_index=False)[sales_col].sum().sort_values(sales_col, ascending=False).head(10)
        st.plotly_chart(px.bar(snap, x=category_col, y=sales_col, title="Top Categories (Sales)"), use_container_width=True)

    st.write(f"Data source: **{source_label}** • Rows: {len(dff)}")

# --- Map ---
elif page == "Map":
    st.markdown("<div class='section_title'>Geographic Sales Map</div>", unsafe_allow_html=True)
    if country_col and sales_col:
        agg = dff.groupby(country_col, as_index=False)[sales_col].sum()
        agg = agg.rename(columns={country_col:"country", sales_col:"sales"})

        try:
            fig = px.choropleth(agg, locations="country", locationmode="country names",
                                color="sales", title="Sales by Country",
                                hover_name="country")
            st.plotly_chart(fig, use_container_width=True)

            st.download_button("Download Map as HTML", fig_to_html_bytes(fig), "sales_map.html", mime="text/html")

        except Exception as e:
            st.error("Map failed: " + str(e))
    else:
        st.warning("Country or Sales column missing.")

# --- Category Analysis ---
elif page == "Category Analysis":
    st.markdown("<div class='section_title'>Category Analysis</div>", unsafe_allow_html=True)

    if category_col and sales_col:
        cat = dff.groupby(category_col, as_index=False)[[sales_col, profit_col]].sum()

        fig1 = px.treemap(cat, path=[category_col], values=sales_col, title="Sales Treemap")
        st.plotly_chart(fig1, use_container_width=True)

        fig2 = px.bar(cat.sort_values(sales_col, ascending=False).head(20),
                      x=category_col, y=sales_col, title="Top Categories (Bar)")
        st.plotly_chart(fig2, use_container_width=True)

        st.download_button("Download Category Summary Excel",
                           to_excel_bytes(cat),
                           "category_summary.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.warning("Category or Sales not found.")

# --- Data & Export ---
elif page == "Data & Export":
    st.markdown("<div class='section_title'>Filtered Data</div>", unsafe_allow_html=True)
    st.dataframe(dff.head(300), use_container_width=True)

    st.download_button("Download filtered CSV", to_csv_bytes(dff),
                       "filtered_data.csv", mime="text/csv")
    st.download_button("Download filtered Excel", to_excel_bytes(dff),
                       "filtered_data.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    st.markdown("### Column Mapping")
    st.json({
        "country_col": country_col,
        "sales_col": sales_col,
        "profit_col": profit_col,
        "category_col": category_col,
        "product_col": product_col
    })

# Footer
st.markdown("<hr>")
st.write("Built for: Mohmmed Elbedawy — Custom Dashboard (No Time Series)")
