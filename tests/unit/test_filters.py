"""Unit tests for src/filters.py — ECOM-6"""
import pandas as pd
import pytest
from datetime import date
from unittest.mock import patch, MagicMock


def make_df():
    return pd.DataFrame({
        "date": pd.to_datetime(["2024-01-03", "2024-06-15", "2024-12-31"]),
        "order_id": ["ORD-001", "ORD-002", "ORD-003"],
        "product": ["Widget A", "Widget B", "Widget C"],
        "category": ["Audio", "Accessories", "Clothing"],
        "region": ["North", "South", "East"],
        "quantity": [1, 2, 3],
        "unit_price": [10.0, 20.0, 30.0],
        "total_amount": [10.0, 40.0, 90.0],
    })


# ---------------------------------------------------------------------------
# init_filter_state
# ---------------------------------------------------------------------------

def test_init_filter_state_sets_defaults():
    from src.filters import init_filter_state
    mock_state = {}
    with patch("src.filters.st") as mock_st:
        mock_st.session_state = mock_state
        df = make_df()
        init_filter_state(df)
        assert "filters" in mock_state
        assert mock_state["filters"]["date_start"] == date(2024, 1, 3)
        assert mock_state["filters"]["date_end"] == date(2024, 12, 31)
        assert mock_state["filters"]["selected_categories"] == []


def test_init_filter_state_is_idempotent():
    from src.filters import init_filter_state
    existing = {
        "date_start": date(2024, 3, 1),
        "date_end": date(2024, 9, 30),
        "selected_categories": ["Audio"],
    }
    mock_state = {"filters": existing}
    with patch("src.filters.st") as mock_st:
        mock_st.session_state = mock_state
        df = make_df()
        init_filter_state(df)
        # State should not be overwritten
        assert mock_state["filters"]["date_start"] == date(2024, 3, 1)
        assert mock_state["filters"]["selected_categories"] == ["Audio"]


def test_init_filter_state_dict_structure():
    from src.filters import init_filter_state
    mock_state = {}
    with patch("src.filters.st") as mock_st:
        mock_st.session_state = mock_state
        df = make_df()
        init_filter_state(df)
        keys = set(mock_state["filters"].keys())
        assert keys == {"date_start", "date_end", "selected_categories"}
