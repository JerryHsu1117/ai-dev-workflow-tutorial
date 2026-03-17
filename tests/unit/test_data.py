"""Unit tests for src/data.py — ECOM-6"""
import pytest
import pandas as pd
from datetime import date
from unittest.mock import patch

VALID_CSV = """date,order_id,product,category,region,quantity,unit_price,total_amount
2024-01-03,ORD-001,Widget A,Audio,North,2,79.99,159.98
2024-01-04,ORD-002,Widget B,Accessories,South,3,24.99,74.97
2024-01-05,ORD-003,Widget C,Audio,East,1,49.99,49.99
2024-02-10,ORD-004,Widget D,Clothing,West,2,19.99,39.98
2024-02-15,ORD-005,Widget E,Accessories,North,1,99.99,99.99
"""


def make_df(csv_text=VALID_CSV):
    from io import StringIO
    return pd.read_csv(StringIO(csv_text), parse_dates=["date"])


# ---------------------------------------------------------------------------
# load_data
# ---------------------------------------------------------------------------

def test_load_data_returns_dataframe(tmp_path):
    from src.data import load_data
    csv_file = tmp_path / "sales-data.csv"
    csv_file.write_text(VALID_CSV)
    df = _call_load_data(load_data, str(csv_file))
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 5


def _call_load_data(load_data, path):
    """Helper to call load_data bypassing st.cache_data."""
    import src.data as data_mod
    orig = data_mod.DATA_PATH
    data_mod.DATA_PATH = path
    # Clear cache if possible
    try:
        load_data.clear()
    except Exception:
        pass
    result = load_data()
    data_mod.DATA_PATH = orig
    return result


def test_load_data_column_dtypes(tmp_path):
    from src.data import load_data
    import src.data as data_mod
    csv_file = tmp_path / "sales-data.csv"
    csv_file.write_text(VALID_CSV)
    orig = data_mod.DATA_PATH
    data_mod.DATA_PATH = str(csv_file)
    try:
        load_data.clear()
    except Exception:
        pass
    df = load_data()
    data_mod.DATA_PATH = orig
    assert df["date"].dtype == "datetime64[ns]"
    assert df["quantity"].dtype == "int64"
    assert df["unit_price"].dtype == "float64"
    assert df["total_amount"].dtype == "float64"


def test_load_data_raises_on_missing_column(tmp_path):
    from src.data import load_data
    import src.data as data_mod
    bad_csv = "date,order_id,product\n2024-01-01,ORD-001,Widget\n"
    csv_file = tmp_path / "sales-data.csv"
    csv_file.write_text(bad_csv)
    orig = data_mod.DATA_PATH
    data_mod.DATA_PATH = str(csv_file)
    try:
        load_data.clear()
    except Exception:
        pass
    with pytest.raises(ValueError, match="column"):
        load_data()
    data_mod.DATA_PATH = orig


# ---------------------------------------------------------------------------
# apply_filters
# ---------------------------------------------------------------------------

def test_apply_filters_no_filters_returns_all():
    from src.data import apply_filters
    df = make_df()
    filters = {"date_start": None, "date_end": None, "selected_categories": []}
    result = apply_filters(df, filters)
    assert len(result) == 5


def test_apply_filters_date_start():
    from src.data import apply_filters
    df = make_df()
    filters = {"date_start": date(2024, 2, 1), "date_end": None, "selected_categories": []}
    result = apply_filters(df, filters)
    assert len(result) == 2
    assert all(r >= pd.Timestamp("2024-02-01") for r in result["date"])


def test_apply_filters_date_end():
    from src.data import apply_filters
    df = make_df()
    filters = {"date_start": None, "date_end": date(2024, 1, 31), "selected_categories": []}
    result = apply_filters(df, filters)
    assert len(result) == 3


def test_apply_filters_combined_date_and_category():
    from src.data import apply_filters
    df = make_df()
    filters = {
        "date_start": date(2024, 1, 1),
        "date_end": date(2024, 1, 31),
        "selected_categories": ["Audio"],
    }
    result = apply_filters(df, filters)
    assert len(result) == 2
    assert all(r == "Audio" for r in result["category"])


def test_apply_filters_empty_result_returns_empty_dataframe():
    from src.data import apply_filters
    df = make_df()
    filters = {"date_start": date(2030, 1, 1), "date_end": date(2030, 12, 31), "selected_categories": []}
    result = apply_filters(df, filters)
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 0
    assert list(result.columns) == list(df.columns)


def test_apply_filters_does_not_mutate_input():
    from src.data import apply_filters
    df = make_df()
    original_len = len(df)
    filters = {"date_start": date(2024, 2, 1), "date_end": None, "selected_categories": []}
    apply_filters(df, filters)
    assert len(df) == original_len


# ---------------------------------------------------------------------------
# get_kpi_metrics
# ---------------------------------------------------------------------------

def test_get_kpi_metrics_totals():
    from src.data import get_kpi_metrics
    df = make_df()
    result = get_kpi_metrics(df)
    assert "total_sales" in result
    assert "total_orders" in result
    assert abs(result["total_sales"] - (159.98 + 74.97 + 49.99 + 39.98 + 99.99)) < 0.01
    assert result["total_orders"] == 5


def test_get_kpi_metrics_empty_df():
    from src.data import get_kpi_metrics
    df = make_df()
    empty = df.iloc[0:0]
    result = get_kpi_metrics(empty)
    assert result["total_sales"] == 0.0
    assert result["total_orders"] == 0


# ---------------------------------------------------------------------------
# get_time_series
# ---------------------------------------------------------------------------

def test_get_time_series_daily():
    from src.data import get_time_series
    df = make_df()
    result = get_time_series(df, "daily")
    assert list(result.columns) == ["period", "total_sales"]
    assert len(result) == 5  # 5 distinct days
    assert result["period"].is_monotonic_increasing


def test_get_time_series_monthly():
    from src.data import get_time_series
    df = make_df()
    result = get_time_series(df, "monthly")
    assert list(result.columns) == ["period", "total_sales"]
    assert len(result) == 2  # Jan and Feb
    assert result["period"].is_monotonic_increasing


# ---------------------------------------------------------------------------
# get_category_summary
# ---------------------------------------------------------------------------

def test_get_category_summary_sort_order():
    from src.data import get_category_summary
    df = make_df()
    result = get_category_summary(df)
    assert list(result.columns) == ["category", "total_sales"]
    assert result["total_sales"].is_monotonic_decreasing


# ---------------------------------------------------------------------------
# get_region_summary
# ---------------------------------------------------------------------------

def test_get_region_summary_sort_order():
    from src.data import get_region_summary
    df = make_df()
    result = get_region_summary(df)
    assert list(result.columns) == ["region", "total_sales"]
    assert result["total_sales"].is_monotonic_decreasing
