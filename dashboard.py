"""ShopSmart Sales Dashboard — Home page (KPIs + Sales Trend) — ECOM-7"""
import streamlit as st

from src.data import load_data, get_kpi_metrics, apply_filters
from src.filters import init_filter_state, render_date_filter

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")

# --- Load data ---
try:
    df = load_data()
except ValueError as e:
    st.error(f"Failed to load sales data: {e}")
    st.stop()

# --- Filter state & sidebar ---
init_filter_state(df)
render_date_filter(df)

# --- Apply filters ---
filtered_df = apply_filters(df, st.session_state["filters"])

# --- KPI Scorecards ---
kpis = get_kpi_metrics(filtered_df)

col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${kpis['total_sales']:,.0f}")
col2.metric("Total Orders", f"{kpis['total_orders']:,}")
