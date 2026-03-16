"""Plotly chart factory functions — ECOM-6"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def make_trend_chart(df: pd.DataFrame, granularity: str) -> go.Figure:
    """Line chart of sales over time."""
    fig = px.line(
        df,
        x="period",
        y="total_sales",
        title="Sales Over Time",
        labels={"period": "Date", "total_sales": "Total Sales ($)"},
    )
    return fig


def make_category_chart(df: pd.DataFrame) -> go.Figure:
    """Horizontal bar chart of sales by category."""
    fig = px.bar(
        df,
        x="total_sales",
        y="category",
        orientation="h",
        title="Which Categories Drive Revenue?",
        labels={"total_sales": "Total Sales ($)", "category": "Category"},
    )
    return fig


def make_region_chart(df: pd.DataFrame) -> go.Figure:
    """Horizontal bar chart of sales by region."""
    fig = px.bar(
        df,
        x="total_sales",
        y="region",
        orientation="h",
        title="Sales Performance by Region",
        labels={"total_sales": "Total Sales ($)", "region": "Region"},
    )
    return fig
