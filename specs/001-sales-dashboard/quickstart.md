# Quickstart: ShopSmart Sales Analytics Dashboard

**Branch**: `001-sales-dashboard` | **Date**: 2026-03-13

## Prerequisites

- Python 3.11+
- `uv` package manager (`pip install uv` or see https://docs.astral.sh/uv/getting-started/installation/)
- Git

## Setup

```bash
# 1. Clone the repo and switch to the feature branch
git clone <repo-url>
cd <repo-name>
git checkout 001-sales-dashboard

# 2. Install dependencies
uv sync

# 3. Verify the data file is present
ls data/sales-data.csv
```

## Run Locally

```bash
uv run streamlit run dashboard.py
```

Open http://localhost:8501 in your browser. You should see:
- **Home page**: Total Sales KPI, Total Orders KPI, Sales Trend line chart
- **Sidebar**: Date range filter (Start/End date inputs + preset buttons)
- **Navigation**: "Segment Analysis" page in the left sidebar nav

Navigate to **Segment Analysis** to see:
- Category multi-select filter (inline, above chart)
- Sales by Category bar chart
- Sales by Region bar chart

## Run Tests

```bash
# All tests
uv run pytest

# Unit tests only
uv run pytest tests/unit/

# Integration tests only
uv run pytest tests/integration/

# Verbose output
uv run pytest -v
```

## Validation Checklist

After running locally, verify:

- [ ] Total Sales displays as formatted currency (e.g., `$672,340`)
- [ ] Total Orders displays as a whole number (e.g., `482`)
- [ ] Sales Trend chart renders with time on X-axis and sales on Y-axis
- [ ] Granularity toggle switches between Daily and Monthly views
- [ ] Selecting "Last 30 Days" in sidebar updates all components
- [ ] Selecting a category on Segment Analysis page updates the Region chart and KPIs
- [ ] Clearing all filters restores full-dataset values
- [ ] No errors or warnings in the terminal or browser console

## Deploy to Streamlit Cloud

1. Push branch to GitHub.
2. Sign in at https://share.streamlit.io
3. Click **New app** → select repo, branch `001-sales-dashboard`, main file `dashboard.py`.
4. Click **Deploy**.

> **Note**: Streamlit Cloud UI changes frequently. If these steps don't match exactly,
> adapt based on the current interface. The goal is: point Streamlit Cloud at
> `dashboard.py` on this branch.

## Project Layout

```
dashboard.py                  # Home page: KPIs + Sales Trend
pages/
  1_Segment_Analysis.py       # Category + Region breakdowns
src/
  __init__.py
  data.py                     # load_data(), filters, aggregations
  charts.py                   # Plotly chart factory functions
  filters.py                  # Filter UI components and session state
data/
  sales-data.csv              # ~1,000 transaction records
tests/
  unit/
    test_data.py
    test_charts.py
    test_filters.py
  integration/
    test_home.py
    test_segment.py
.streamlit/
  config.toml
pyproject.toml
```
