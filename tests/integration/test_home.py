"""Integration tests for dashboard.py (Home page) — ECOM-7"""
import pytest
from streamlit.testing.v1 import AppTest


@pytest.fixture
def app():
    at = AppTest.from_file("dashboard.py", default_timeout=30)
    at.run()
    return at


# ---------------------------------------------------------------------------
# US1: KPI Scorecards
# ---------------------------------------------------------------------------

def test_kpi_total_sales_visible(app):
    """Total Sales metric is visible on load."""
    metric_labels = [m.label for m in app.metric]
    assert any("sales" in label.lower() or "Sales" in label for label in metric_labels), (
        f"Expected a 'Total Sales' metric, got labels: {metric_labels}"
    )


def test_kpi_total_orders_visible(app):
    """Total Orders metric is visible on load."""
    metric_labels = [m.label for m in app.metric]
    assert any("orders" in label.lower() or "Orders" in label for label in metric_labels), (
        f"Expected a 'Total Orders' metric, got labels: {metric_labels}"
    )


def test_kpi_total_sales_is_currency_string(app):
    """Total Sales value is formatted as a currency string (starts with $)."""
    sales_metric = next(
        (m for m in app.metric if "sales" in m.label.lower()),
        None,
    )
    assert sales_metric is not None, "Total Sales metric not found"
    assert sales_metric.value.startswith("$"), (
        f"Expected currency format starting with '$', got: {sales_metric.value}"
    )


def test_kpi_total_orders_is_integer_string(app):
    """Total Orders value is a whole number (no decimal point)."""
    orders_metric = next(
        (m for m in app.metric if "orders" in m.label.lower()),
        None,
    )
    assert orders_metric is not None, "Total Orders metric not found"
    # Should be a whole number — no decimal separator
    assert "." not in orders_metric.value, (
        f"Expected whole number, got: {orders_metric.value}"
    )
    # Should be parseable as int
    int(orders_metric.value.replace(",", ""))


def test_no_errors_on_load(app):
    """Dashboard loads without any st.error() messages."""
    assert len(app.error) == 0, f"Unexpected errors on load: {[e.value for e in app.error]}"
