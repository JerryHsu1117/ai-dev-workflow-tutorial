"""Integration tests for pages/1_Segment_Analysis.py — ECOM-9/ECOM-10"""
import os
from datetime import date
import pytest
from streamlit.testing.v1 import AppTest

_SEGMENT_PAGE = os.path.join(
    os.path.dirname(__file__), "..", "..", "pages", "1_Segment_Analysis.py"
)


@pytest.fixture
def app():
    at = AppTest.from_file(_SEGMENT_PAGE, default_timeout=30)
    at.run()
    return at


# ---------------------------------------------------------------------------
# US3: Segment Analysis Page
# ---------------------------------------------------------------------------

def test_page_title_visible(app):
    """Segment Analysis page title is rendered."""
    titles = [t.value for t in app.title] + [h.value for h in app.header] + [h.value for h in app.subheader]
    assert any("segment" in t.lower() or "Segment" in t for t in titles), (
        f"Expected page title containing 'Segment', got: {titles}"
    )


def test_two_charts_rendered(app):
    """Both category and region charts are rendered."""
    charts = app.get("plotly_chart")
    assert len(charts) >= 2, f"Expected at least 2 Plotly charts, got: {len(charts)}"


def test_category_multiselect_exists(app):
    """Category multiselect filter widget is present."""
    multiselects = app.multiselect
    assert len(multiselects) > 0, "Expected at least one multiselect widget"
    labels = [m.label for m in multiselects]
    assert any("category" in label.lower() or "Category" in label for label in labels), (
        f"Expected 'Filter by Category' multiselect, got: {labels}"
    )


def test_no_errors_on_load(app):
    """Segment Analysis page loads without any st.error() messages."""
    assert len(app.error) == 0, f"Unexpected errors on load: {[e.value for e in app.error]}"


def test_category_filter_options_populated(app):
    """Category multiselect is populated with categories from the dataset (not empty)."""
    multiselects = app.multiselect
    assert len(multiselects) > 0, "No multiselect found"
    cat_select = next(
        (m for m in multiselects if "category" in m.label.lower()),
        multiselects[0],
    )
    assert len(cat_select.options) > 0, "Category multiselect has no options — expected dataset categories"


# ---------------------------------------------------------------------------
# US4: Category Filter Propagation
# ---------------------------------------------------------------------------

def test_category_filter_reduces_chart_data():
    """Selecting a single category shows only that category's data — charts still render."""
    at = AppTest.from_file(_SEGMENT_PAGE, default_timeout=30)
    at.session_state["filters"] = {
        "date_start": None,
        "date_end": None,
        "selected_categories": ["Audio"],
    }
    at.run()
    assert len(at.error) == 0, f"Errors with category filter: {[e.value for e in at.error]}"
    charts = at.get("plotly_chart")
    assert len(charts) >= 2, "Expected 2 charts even with category filter applied"


def test_category_filter_via_multiselect():
    """Selecting a category via the multiselect widget re-renders charts without error."""
    at = AppTest.from_file(_SEGMENT_PAGE, default_timeout=30)
    at.run()
    cat_select = next(
        (m for m in at.multiselect if "category" in m.label.lower()),
        at.multiselect[0],
    )
    cat_select.set_value(["Audio"]).run()
    assert len(at.error) == 0, f"Errors after selecting Audio: {[e.value for e in at.error]}"
    charts = at.get("plotly_chart")
    assert len(charts) >= 2, "Expected charts after category filter applied"


def test_empty_filter_shows_info():
    """A date filter with no matching transactions shows st.info(), not st.error()."""
    at = AppTest.from_file(_SEGMENT_PAGE, default_timeout=30)
    # 2024-01-13 is a known day with no transactions in the dataset
    at.session_state["filters"] = {
        "date_start": date(2024, 1, 13),
        "date_end": date(2024, 1, 13),
        "selected_categories": [],
    }
    at.run()
    assert len(at.error) == 0, "Expected no st.error() for empty filter result"
    assert len(at.info) > 0, "Expected st.info() empty-state message when no data matches"
