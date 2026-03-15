# Data Model: ShopSmart Sales Analytics Dashboard

**Branch**: `001-sales-dashboard` | **Date**: 2026-03-13

## Source Schema — `data/sales-data.csv`

| Column         | Type     | Nullable | Validation                          |
|----------------|----------|----------|-------------------------------------|
| `date`         | date     | No       | ISO 8601 (YYYY-MM-DD), parseable    |
| `order_id`     | string   | No       | Non-empty string                    |
| `product`      | string   | No       | Non-empty string                    |
| `category`     | string   | No       | One of 5 known categories           |
| `region`       | string   | No       | One of 4 known regions              |
| `quantity`     | integer  | No       | > 0                                 |
| `unit_price`   | decimal  | No       | > 0.0                               |
| `total_amount` | decimal  | No       | > 0.0, should equal qty × unit_price|

**Schema validation** runs at load time inside `load_data()`. Any violation raises a
`ValueError` with a human-readable message displayed via `st.error()`.

---

## Runtime Entities

### Transaction

Represents a single row from the CSV after loading and type-casting.

| Field          | Python type | Notes                          |
|----------------|-------------|--------------------------------|
| `date`         | `date`      | Parsed from string at load     |
| `order_id`     | `str`       |                                |
| `product`      | `str`       |                                |
| `category`     | `str`       | Used as filter dimension       |
| `region`       | `str`       | Used as filter dimension       |
| `quantity`     | `int`       |                                |
| `unit_price`   | `float`     |                                |
| `total_amount` | `float`     | Primary metric for aggregation |

In practice, transactions live in a single `pd.DataFrame` — not individual objects.

---

### FilterState

Represents the active filter selections at any point in time. Stored in
`st.session_state["filters"]` and shared across all pages.

| Field                  | Python type    | Default          | Notes                                |
|------------------------|----------------|------------------|--------------------------------------|
| `date_start`           | `date \| None` | Earliest in data | None means "no lower bound"          |
| `date_end`             | `date \| None` | Latest in data   | None means "no upper bound"          |
| `selected_categories`  | `list[str]`    | `[]` (all)       | Empty list means all categories shown|

**Semantics**: Filters combine as AND. An empty `selected_categories` list means
"no category filter active" (show all). Both `date_start` and `date_end` must be set
together for a date filter to be active.

---

### KPIMetrics

Derived from the filtered DataFrame. Recalculated on every filter change.

| Field          | Python type | Calculation                   | Display format   |
|----------------|-------------|-------------------------------|------------------|
| `total_sales`  | `float`     | `df["total_amount"].sum()`    | `$1,234,567`     |
| `total_orders` | `int`       | `df["order_id"].nunique()`    | `482`            |

---

### TimeSeries

Aggregated from the filtered DataFrame for the Trend chart.

| Field         | Python type | Granularity        | Notes                         |
|---------------|-------------|--------------------|-------------------------------|
| `period`      | `date`      | day or month-start | Monthly: truncated to 1st     |
| `total_sales` | `float`     | Sum of `total_amount` within period |                |

`granularity` is a UI state value (`"daily"` or `"monthly"`) stored in
`st.session_state["trend_granularity"]`, defaulting to `"monthly"`.

---

### CategorySummary

Aggregated from the filtered DataFrame for the Category bar chart.

| Field          | Python type | Calculation                              |
|----------------|-------------|------------------------------------------|
| `category`     | `str`       | Group key                                |
| `total_sales`  | `float`     | `sum(total_amount)` per category         |

Sorted descending by `total_sales` before rendering.

---

### RegionSummary

Aggregated from the filtered DataFrame for the Region bar chart.

| Field          | Python type | Calculation                              |
|----------------|-------------|------------------------------------------|
| `region`       | `str`       | Group key                                |
| `total_sales`  | `float`     | `sum(total_amount)` per region           |

Sorted descending by `total_sales` before rendering.

---

## Data Flow

```
data/sales-data.csv
        │
        ▼
  load_data()                 ← @st.cache_data (no TTL), runs once per page load
  schema validation
        │
        ▼
  raw DataFrame (all rows)
        │
        ▼
  apply_filters(df, FilterState)   ← called on every render cycle
        │
        ▼
  filtered DataFrame
        │
    ┌───┴──────────────────────────────────┐
    │           │            │             │
    ▼           ▼            ▼             ▼
 KPIMetrics  TimeSeries  CategorySummary  RegionSummary
    │           │            │             │
    ▼           ▼            ▼             ▼
 st.metric  px.line      px.bar (h)    px.bar (h)
```

---

## Session State Keys

| Key                        | Type         | Owner page            | Purpose                        |
|----------------------------|--------------|-----------------------|--------------------------------|
| `filters`                  | `dict`       | sidebar (all pages)   | Global filter state            |
| `trend_granularity`        | `str`        | `dashboard.py`        | "daily" or "monthly"           |
| `selected_categories`      | `list[str]`  | `1_Segment_Analysis`  | Inline category multi-select   |
