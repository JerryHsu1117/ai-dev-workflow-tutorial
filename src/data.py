"""Data loading and transformation functions — ECOM-6"""
import os
import pandas as pd
import streamlit as st

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "sales-data.csv")

REQUIRED_COLUMNS = {"date", "order_id", "product", "category", "region", "quantity", "unit_price", "total_amount"}


@st.cache_data
def load_data() -> pd.DataFrame:
    """Load and validate the sales CSV. Raises ValueError on schema errors."""
    df = pd.read_csv(DATA_PATH)

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required column(s): {', '.join(sorted(missing))}")

    try:
        df["date"] = pd.to_datetime(df["date"])
    except Exception as exc:
        raise ValueError(f"date column contains unparseable values: {exc}") from exc

    df["quantity"] = df["quantity"].astype("int64")
    df["unit_price"] = df["unit_price"].astype("float64")
    df["total_amount"] = df["total_amount"].astype("float64")

    if (df["quantity"] <= 0).any():
        raise ValueError("quantity column contains non-positive values")
    if (df["unit_price"] <= 0).any():
        raise ValueError("unit_price column contains non-positive values")
    if (df["total_amount"] <= 0).any():
        raise ValueError("total_amount column contains non-positive values")

    return df


def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """Apply date and category filters. Returns a new DataFrame; never mutates input."""
    mask = pd.Series([True] * len(df), index=df.index)

    if filters.get("date_start") is not None:
        mask &= df["date"] >= pd.Timestamp(filters["date_start"])
    if filters.get("date_end") is not None:
        mask &= df["date"] <= pd.Timestamp(filters["date_end"])

    selected = filters.get("selected_categories", [])
    if selected:
        mask &= df["category"].isin(selected)

    return df[mask].copy()


def get_kpi_metrics(df: pd.DataFrame) -> dict:
    """Return total_sales (float) and total_orders (int) from a filtered DataFrame."""
    return {
        "total_sales": float(df["total_amount"].sum()),
        "total_orders": int(df["order_id"].nunique()),
    }


def get_time_series(df: pd.DataFrame, granularity: str) -> pd.DataFrame:
    """Aggregate sales by day or month. Returns DataFrame with ['period', 'total_sales']."""
    if granularity == "daily":
        period = df["date"].dt.floor("D")
    else:
        period = df["date"].dt.to_period("M").dt.to_timestamp()

    result = (
        df.assign(period=period)
        .groupby("period", as_index=False)["total_amount"]
        .sum()
        .rename(columns={"total_amount": "total_sales"})
        .sort_values("period")
        [["period", "total_sales"]]
    )
    return result.reset_index(drop=True)


def get_category_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sales by category, sorted descending."""
    return (
        df.groupby("category", as_index=False)["total_amount"]
        .sum()
        .rename(columns={"total_amount": "total_sales"})
        .sort_values("total_sales", ascending=False)
        [["category", "total_sales"]]
        .reset_index(drop=True)
    )


def get_region_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sales by region, sorted descending."""
    return (
        df.groupby("region", as_index=False)["total_amount"]
        .sum()
        .rename(columns={"total_amount": "total_sales"})
        .sort_values("total_sales", ascending=False)
        [["region", "total_sales"]]
        .reset_index(drop=True)
    )
