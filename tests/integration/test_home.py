"""Integration tests for dashboard.py (Home page) — ECOM-7/ECOM-8/ECOM-10"""
from datetime import date
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


# ---------------------------------------------------------------------------
# US2: Sales Trend Chart
# ---------------------------------------------------------------------------

def test_trend_chart_renders(app):
    """A Plotly chart is rendered on the home page."""
    charts = app.get("plotly_chart")
    assert len(charts) > 0, "Expected at least one Plotly chart on the home page"


def test_granularity_toggle_exists(app):
    """Monthly/Daily radio toggle is present."""
    radio_labels = [r.label for r in app.radio]
    assert len(radio_labels) > 0, f"Expected a granularity radio widget, got none"


def test_granularity_toggle_has_monthly_daily_options(app):
    """Granularity toggle offers Monthly and Daily options."""
    radios = app.radio
    assert len(radios) > 0, "No radio widgets found"
    options = radios[0].options
    assert "Monthly" in options, f"Expected 'Monthly' option, got: {options}"
    assert "Daily" in options, f"Expected 'Daily' option, got: {options}"


def test_granularity_default_is_monthly(app):
    """Granularity toggle defaults to Monthly."""
    assert app.radio[0].value == "Monthly", (
        f"Expected default 'Monthly', got: {app.radio[0].value}"
    )


def test_switching_to_daily_rerenders_chart(app):
    """Switching granularity to Daily re-renders the chart without error."""
    app.radio[0].set_value("Daily").run()
    assert len(app.error) == 0, f"Errors after switching to Daily: {[e.value for e in app.error]}"
    charts = app.get("plotly_chart")
    assert len(charts) > 0, "Chart disappeared after switching to Daily"


# ---------------------------------------------------------------------------
# US4: Date Filter Propagation
# ---------------------------------------------------------------------------

def test_date_filter_reduces_total_orders():
    """Narrowing date range to January 2024 reduces Total Orders from 482 to 40."""
    at = AppTest.from_file("dashboard.py", default_timeout=30)
    at.session_state["filters"] = {
        "date_start": date(2024, 1, 3),   # dataset starts 2024-01-03
        "date_end": date(2024, 1, 31),
        "selected_categories": [],
    }
    at.run()
    assert len(at.error) == 0, f"Errors with date filter: {[e.value for e in at.error]}"
    orders_metric = next(m for m in at.metric if "orders" in m.label.lower())
    orders = int(orders_metric.value.replace(",", ""))
    assert orders == 40, f"Expected 40 orders for Jan 2024, got {orders}"


def test_date_filter_reduces_total_sales():
    """Narrowing date range to January 2024 reduces Total Sales below full-dataset value."""
    at = AppTest.from_file("dashboard.py", default_timeout=30)
    at.session_state["filters"] = {
        "date_start": date(2024, 1, 3),   # dataset starts 2024-01-03
        "date_end": date(2024, 1, 31),
        "selected_categories": [],
    }
    at.run()
    sales_metric = next(m for m in at.metric if "sales" in m.label.lower())
    sales = float(sales_metric.value.replace("$", "").replace(",", ""))
    assert sales < 116500, f"Expected sales < full-dataset $116,500, got ${sales:,.2f}"
    assert sales > 0, "Expected non-zero sales for January 2024"


def test_empty_date_range_shows_info_not_error():
    """A date that has no transactions shows st.info() empty-state, not st.error()."""
    at = AppTest.from_file("dashboard.py", default_timeout=30)
    # 2024-01-13 is a known day with no transactions in the dataset
    at.session_state["filters"] = {
        "date_start": date(2024, 1, 13),
        "date_end": date(2024, 1, 13),
        "selected_categories": [],
    }
    at.run()
    assert len(at.error) == 0, "Expected no st.error() for empty filter result"
    assert len(at.info) > 0, "Expected st.info() empty-state message"
