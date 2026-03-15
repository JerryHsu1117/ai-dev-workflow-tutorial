# Research: ShopSmart Sales Analytics Dashboard

**Branch**: `001-sales-dashboard` | **Date**: 2026-03-13

## Decision 1: Multi-Page Streamlit Structure

**Decision**: Use Streamlit's native multi-page app support (`pages/` directory).
`dashboard.py` is the home page (KPIs + Trend chart); `pages/1_Segment_Analysis.py`
hosts the Category and Regional breakdowns.

**Rationale**: Streamlit has supported multi-page apps natively since v1.10 with zero
extra dependencies. The home page serves the executive "quick glance" use case; the
segment analysis page serves the marketing/regional manager deep-dive use case. Pages
directory is also the natural extension point for Phase 2 features.

**Alternatives considered**:
- Single `dashboard.py` — simpler, but doesn't future-proof for Phase 2 expansion.
- `src/`-only modular without pages — adds structure but loses native Streamlit
  navigation.

**Reference**: https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app

---

## Decision 2: Testing — pytest + Streamlit AppTest

**Decision**: Use `pytest` for unit tests and `streamlit.testing.v1.AppTest` for
integration tests. No additional testing libraries required.

**Rationale**: `AppTest` is bundled with Streamlit (available since v1.28). It simulates
app execution without a browser, allowing assertions on widget state, rendered text, and
dataframe values. This covers integration testing without adding Selenium or Playwright
to the stack — consistent with the Minimal Stack principle.

**Unit test targets**: `src/data.py` (load, validate, aggregate), `src/charts.py`
(data preparation), `src/filters.py` (filter state logic).

**Integration test targets**: `dashboard.py` home page, `pages/1_Segment_Analysis.py`.

**Alternatives considered**:
- Playwright/Selenium — browser automation, overkill for a single-user dashboard,
  adds significant dependency weight.
- No tests — ruled out; spec requires unit + integration coverage.

**Reference**: https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest

---

## Decision 3: Data Caching — `@st.cache_data` with No TTL

**Decision**: Decorate `load_data()` with `@st.cache_data` (no TTL). Data is cached
for the session; a full page refresh clears the cache and re-reads the CSV.

**Rationale**: Matches the spec decision (Q4: "auto-refresh on page load"). For a
~1,000-row CSV, load time is negligible but caching still prevents redundant re-reads
on every widget interaction (filter changes, granularity toggle). No TTL is needed
because the stated refresh model is page-load-driven, not time-driven.

**Alternatives considered**:
- `ttl=300` — would auto-refresh every 5 minutes; not aligned with the "page load
  refresh" model chosen in the spec.
- No caching — acceptable for 1,000 rows but triggers a full CSV read on every
  Streamlit interaction (every filter change), which is wasteful and violates
  Performance-First.

---

## Decision 4: Filter Placement — Sidebar + Inline Split

**Decision**: Date range filter lives in the sidebar (persistent, globally visible).
Category multi-select lives inline above the "Sales by Category" chart on the Segment
Analysis page. Both filters affect all dashboard components (KPIs, trend, both charts)
when active.

**Rationale**: The date range filter has the widest scope (affects everything on both
pages) so placing it in the persistent sidebar ensures it's always accessible. The
category filter is contextually associated with the category chart, making inline
placement more intuitive — but its effect is still propagated globally via Streamlit
session state.

**Session state key**: `st.session_state["filters"]` dict holding `date_start`,
`date_end`, `selected_categories`. Both pages read from this shared state.

**Alternatives considered**:
- All filters in sidebar — cleaner but buries the category filter away from the chart
  it most visibly affects.
- All filters inline — requires duplicating the date filter on every page.

---

## Decision 5: Plotly Express vs. Graph Objects

**Decision**: Use Plotly Express (`px`) for all four chart types (line, bar × 3).
Fall back to `go.Figure` only if a specific customization cannot be achieved with `px`.

**Rationale**: Plotly Express covers all required chart types with one-line calls and
sensible defaults. Constitution Principle IV (Minimal Stack) favors `px` unless a
specific need justifies `go`. For this scope, no such need exists.

**Chart mapping**:
- Sales Trend: `px.line`
- Sales by Category: `px.bar` (horizontal, sorted)
- Sales by Region: `px.bar` (horizontal, sorted)

---

## Dependency List (final)

```toml
[project]
requires-python = ">=3.11"
dependencies = [
    "streamlit>=1.28",   # AppTest requires 1.28+
    "plotly>=5.0",
    "pandas>=2.0",
]

[dependency-groups]
dev = [
    "pytest>=8.0",
]
```

No additional runtime or test dependencies are required.
