"""Segment Analysis page — Sales by Category and Region — ECOM-9"""
import streamlit as st

from src.data import load_data, get_category_summary, get_region_summary, apply_filters
from src.filters import init_filter_state, render_date_filter, render_category_filter
from src.charts import make_category_chart, make_region_chart

st.set_page_config(page_title="Segment Analysis — ShopSmart", layout="wide")
st.title("Segment Analysis")

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

# --- Category filter (inline) ---
render_category_filter(df)
filtered_df = apply_filters(df, st.session_state["filters"])

# --- Side-by-side charts ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales by Category")
    if len(filtered_df) == 0:
        st.info("No data matches the selected filters.")
    else:
        cat_df = get_category_summary(filtered_df)
        st.plotly_chart(make_category_chart(cat_df), use_container_width=True)

with col2:
    st.subheader("Sales by Region")
    if len(filtered_df) == 0:
        st.info("No data matches the selected filters.")
    else:
        reg_df = get_region_summary(filtered_df)
        st.plotly_chart(make_region_chart(reg_df), use_container_width=True)
