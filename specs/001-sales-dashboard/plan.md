# Implementation Plan: ShopSmart Sales Analytics Dashboard

**Branch**: `001-sales-dashboard` | **Date**: 2026-03-13 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/001-sales-dashboard/spec.md`

## Summary

Build a Streamlit multi-page sales analytics dashboard for ShopSmart. The home page
displays KPI scorecards (Total Sales, Total Orders) and an interactive sales trend chart
with a daily/monthly granularity toggle. A dedicated Segment Analysis page displays
category and regional bar charts with an inline category filter. A global date-range
filter lives in the sidebar. Data is loaded from `data/sales-data.csv` via a single
`load_data()` interface, cached at page load with `@st.cache_data`, and schema-validated
at startup. Stack: Python 3.11+, Streamlit, Plotly Express, Pandas. Tests: pytest +
Streamlit AppTest.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Streamlit ≥1.28, Plotly ≥5.0, Pandas ≥2.0
**Storage**: CSV file (`data/sales-data.csv`) — no database
**Testing**: pytest + `streamlit.testing.v1.AppTest` (bundled with Streamlit ≥1.28)
**Target Platform**: Streamlit Cloud (Linux), modern desktop browsers ≥1024px
**Project Type**: web-app (Streamlit multi-page)
**Performance Goals**: Initial page render <3s; filter/chart updates <2s (Constitution I)
**Constraints**: ~1,000 rows CSV; no auth; `uv` only; single `streamlit run dashboard.py`
entrypoint; no backend service or database
**Scale/Scope**: Single-user at a time (Streamlit Cloud free tier); ~1,000 transactions;
4 pages max (1 home + 3 future)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-checked after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Performance-First | ✅ PASS | `@st.cache_data` caches CSV at startup; all aggregations use vectorized Pandas ops; ~1,000 rows is well within 3s render budget |
| II. Audience Clarity | ✅ PASS | Chart titles will state business questions; KPIs show units and time context; no raw column names in any UI element |
| III. Data Integrity | ✅ PASS | Single `load_data()` interface; schema validation at load time; `apply_filters()` returns empty DataFrame (not error) when no rows match; callers handle empty gracefully |
| IV. Minimal Stack | ✅ PASS | Python 3.11+, Streamlit, Plotly, Pandas only; `uv` is the only package manager; no backend service required |
| V. Traceability | ✅ PASS | Spec-kit artifacts produced in order (constitution → spec → plan → tasks); Jira issues to be created before coding begins |

**Gate result**: All 5 principles pass. Implementation may proceed.

## Project Structure

### Documentation (this feature)

```text
specs/001-sales-dashboard/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/
│   ├── data-contract.md
│   └── filter-contract.md
└── tasks.md             # Phase 2 output (/speckit.tasks — NOT created here)
```

### Source Code (repository root)

```text
dashboard.py                  # Streamlit entrypoint — Home page (KPIs + Trend chart)
pages/
  1_Segment_Analysis.py       # Category & Region breakdowns + inline category filter
src/
  __init__.py
  data.py                     # load_data(), apply_filters(), aggregation functions
  charts.py                   # Plotly chart factory functions
  filters.py                  # Filter UI components and session state helpers
data/
  sales-data.csv              # Source data (~1,000 transactions)
tests/
  unit/
    test_data.py              # load_data(), schema validation, aggregation logic
    test_charts.py            # chart data preparation
    test_filters.py           # filter state init and apply logic
  integration/
    test_home.py              # AppTest for dashboard.py
    test_segment.py           # AppTest for pages/1_Segment_Analysis.py
.streamlit/
  config.toml                 # Layout and theme settings
pyproject.toml                # uv-managed dependencies
```

**Structure Decision**: Multi-page Streamlit app (`pages/` directory). `dashboard.py`
is the Streamlit entrypoint and home page. All shared logic is in `src/` to keep page
files thin. The `pages/` directory is pre-structured for Phase 2 expansion without
requiring architectural changes.

## Complexity Tracking

> No constitution violations. This section is intentionally empty.
