"""Filter state management and UI components — ECOM-6"""
from datetime import date, timedelta
import pandas as pd
import streamlit as st


def init_filter_state(df: pd.DataFrame) -> None:
    """Idempotently initialize st.session_state['filters'] with dataset defaults."""
    if "filters" not in st.session_state:
        st.session_state["filters"] = {
            "date_start": df["date"].min().date(),
            "date_end": df["date"].max().date(),
            "selected_categories": [],
        }


def render_date_filter(df: pd.DataFrame) -> None:
    """Render date range filter widgets in the sidebar."""
    st.sidebar.header("Filters")

    today = date.today()
    min_date = df["date"].min().date()
    max_date = df["date"].max().date()

    col1, col2 = st.sidebar.columns(2)
    if col1.button("Last 30 Days"):
        st.session_state["filters"]["date_start"] = today - timedelta(days=30)
        st.session_state["filters"]["date_end"] = today
    if col2.button("Last 90 Days"):
        st.session_state["filters"]["date_start"] = today - timedelta(days=90)
        st.session_state["filters"]["date_end"] = today

    col3, col4 = st.sidebar.columns(2)
    if col3.button("Year to Date"):
        st.session_state["filters"]["date_start"] = date(today.year, 1, 1)
        st.session_state["filters"]["date_end"] = today
    if col4.button("All Time"):
        st.session_state["filters"]["date_start"] = min_date
        st.session_state["filters"]["date_end"] = max_date

    current_start = st.session_state["filters"].get("date_start") or min_date
    current_end = st.session_state["filters"].get("date_end") or max_date

    start = st.sidebar.date_input(
        "Start Date",
        value=current_start,
        min_value=min_date,
        max_value=max_date,
        key="date_start_input",
    )
    end = st.sidebar.date_input(
        "End Date",
        value=current_end,
        min_value=min_date,
        max_value=max_date,
        key="date_end_input",
    )

    if end < start:
        st.sidebar.error("End date must be on or after start date.")
    else:
        st.session_state["filters"]["date_start"] = start
        st.session_state["filters"]["date_end"] = end


def render_category_filter(df: pd.DataFrame) -> None:
    """Render category multiselect filter inline (not in sidebar)."""
    categories = sorted(df["category"].unique().tolist())
    selected = st.multiselect(
        "Filter by Category",
        options=categories,
        default=st.session_state["filters"].get("selected_categories", []),
        key="category_multiselect",
    )
    st.session_state["filters"]["selected_categories"] = selected
