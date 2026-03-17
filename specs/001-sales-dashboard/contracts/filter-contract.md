# Contract: Filter State & UI Interface

**Module**: `src/filters.py`
**Branch**: `001-sales-dashboard` | **Date**: 2026-03-13

This contract defines the shared filter state structure and the UI components that
read from and write to it. All pages MUST access filter state exclusively via
`st.session_state["filters"]` — no page-local filter variables.

---

## Session State: `st.session_state["filters"]`

**Type**: `dict`

**Canonical structure**:

```python
{
    "date_start": date | None,
    "date_end":   date | None,
    "selected_categories": list[str],
}
```

**Initialization**: `src/filters.py` exposes `init_filter_state(df)` which MUST be
called once per session before any filter UI is rendered. It populates defaults from
the loaded dataset (earliest date, latest date, empty category list).

---

## `init_filter_state(df: pd.DataFrame) -> None`

Initializes `st.session_state["filters"]` if not already set. Safe to call on every
page render — idempotent.

**Default values**:

| Key                     | Default                                 |
|-------------------------|-----------------------------------------|
| `date_start`            | `df["date"].min().date()`               |
| `date_end`              | `df["date"].max().date()`               |
| `selected_categories`   | `[]` (all categories shown)             |

---

## `render_date_filter(df: pd.DataFrame) -> None`

Renders the date range filter in the **sidebar**. Writes selections to
`st.session_state["filters"]["date_start"]` and `["date_end"]`.

**UI**: Two `st.sidebar.date_input` widgets (Start Date, End Date) plus preset
buttons (Last 30 Days, Last 90 Days, Year to Date, All Time).

**Constraint**: End date MUST be >= start date. If invalid, display
`st.sidebar.error(...)` and do not update session state.

---

## `render_category_filter(df: pd.DataFrame) -> None`

Renders the category multi-select filter **inline** (not in sidebar). Writes
selections to `st.session_state["filters"]["selected_categories"]`.

**UI**: `st.multiselect` populated with all unique categories from the loaded
dataset (not a hardcoded list). Label: "Filter by Category".

**Placement**: Rendered by `pages/1_Segment_Analysis.py` above the Category bar
chart. Its effect propagates globally — the calling page is responsible for passing
the updated filter state to `apply_filters()`.

---

## Filter Propagation Contract

Both `dashboard.py` and `pages/1_Segment_Analysis.py` MUST:

1. Call `init_filter_state(df)` at the top of the page script.
2. Call `render_date_filter(df)` to render the sidebar widget.
3. Call `apply_filters(df, st.session_state["filters"])` to get the filtered dataset
   before computing any KPI, chart, or summary.
4. Pass the filtered dataset to all chart and KPI functions on that page.

`pages/1_Segment_Analysis.py` additionally calls `render_category_filter(df)` inline.
