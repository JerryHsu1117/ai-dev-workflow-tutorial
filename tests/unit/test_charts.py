"""Unit tests for src/charts.py — ECOM-6"""
import pandas as pd
import pytest


def make_time_series():
    return pd.DataFrame({
        "period": pd.to_datetime(["2024-01-01", "2024-02-01", "2024-03-01"]),
        "total_sales": [1000.0, 1500.0, 1200.0],
    })


def make_category_df():
    return pd.DataFrame({
        "category": ["Audio", "Accessories", "Clothing"],
        "total_sales": [2000.0, 1500.0, 800.0],
    })


def make_region_df():
    return pd.DataFrame({
        "region": ["North", "South", "East", "West"],
        "total_sales": [3000.0, 2500.0, 1800.0, 1200.0],
    })


# ---------------------------------------------------------------------------
# make_trend_chart
# ---------------------------------------------------------------------------

def test_make_trend_chart_returns_figure():
    from src.charts import make_trend_chart
    import plotly.graph_objects as go
    df = make_time_series()
    fig = make_trend_chart(df, "monthly")
    assert isinstance(fig, go.Figure)


def test_make_trend_chart_title():
    from src.charts import make_trend_chart
    df = make_time_series()
    fig = make_trend_chart(df, "monthly")
    assert fig.layout.title.text == "Sales Over Time"


def test_make_trend_chart_has_x_and_y_data():
    from src.charts import make_trend_chart
    df = make_time_series()
    fig = make_trend_chart(df, "monthly")
    assert len(fig.data) > 0
    assert len(fig.data[0].x) == 3


def test_make_trend_chart_daily_granularity():
    from src.charts import make_trend_chart
    import plotly.graph_objects as go
    df = make_time_series()
    fig = make_trend_chart(df, "daily")
    assert isinstance(fig, go.Figure)


# ---------------------------------------------------------------------------
# make_category_chart
# ---------------------------------------------------------------------------

def test_make_category_chart_returns_figure():
    from src.charts import make_category_chart
    import plotly.graph_objects as go
    df = make_category_df()
    fig = make_category_chart(df)
    assert isinstance(fig, go.Figure)


def test_make_category_chart_title():
    from src.charts import make_category_chart
    df = make_category_df()
    fig = make_category_chart(df)
    assert fig.layout.title.text == "Which Categories Drive Revenue?"


def test_make_category_chart_is_horizontal_bar():
    from src.charts import make_category_chart
    df = make_category_df()
    fig = make_category_chart(df)
    assert fig.data[0].orientation == "h"


# ---------------------------------------------------------------------------
# make_region_chart
# ---------------------------------------------------------------------------

def test_make_region_chart_returns_figure():
    from src.charts import make_region_chart
    import plotly.graph_objects as go
    df = make_region_df()
    fig = make_region_chart(df)
    assert isinstance(fig, go.Figure)


def test_make_region_chart_title():
    from src.charts import make_region_chart
    df = make_region_df()
    fig = make_region_chart(df)
    assert fig.layout.title.text == "Sales Performance by Region"


def test_make_region_chart_is_horizontal_bar():
    from src.charts import make_region_chart
    df = make_region_df()
    fig = make_region_chart(df)
    assert fig.data[0].orientation == "h"
