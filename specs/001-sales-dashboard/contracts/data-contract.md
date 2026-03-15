# Contract: Data Layer Interface

**Module**: `src/data.py`
**Branch**: `001-sales-dashboard` | **Date**: 2026-03-13

This contract defines the public interface that all Streamlit pages MUST use when
loading and transforming sales data. Pages MUST NOT read the CSV directly or branch
on data source type (Constitution Principle III).

---

## `load_data() -> pd.DataFrame`

Loads and validates the sales CSV. Decorated with `@st.cache_data` (no TTL).

**Returns**: A validated `pd.DataFrame` with columns cast to correct types:

| Column         | dtype          |
|----------------|----------------|
| `date`         | `datetime64`   |
| `order_id`     | `object` (str) |
| `product`      | `object` (str) |
| `category`     | `object` (str) |
| `region`       | `object` (str) |
| `quantity`     | `int64`        |
| `unit_price`   | `float64`      |
| `total_amount` | `float64`      |

**Raises**: `ValueError` with a human-readable message if:
- Any required column is missing
- `date` column contains unparseable values
- `quantity`, `unit_price`, or `total_amount` contain non-positive values

**Callers MUST** wrap calls inside a `try/except` and render `st.error(str(e))` on
failure. They MUST NOT catch the exception silently.

---

## `apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame`

Applies the global filter state to the raw DataFrame. Returns a new DataFrame;
does not mutate the input.

**Parameters**:

| Name      | Type           | Description                                          |
|-----------|----------------|------------------------------------------------------|
| `df`      | `pd.DataFrame` | Full unfiltered dataset (output of `load_data()`)    |
| `filters` | `dict`         | Filter state from `st.session_state["filters"]`      |

**Filter dict structure**:

```python
{
    "date_start": date | None,   # inclusive lower bound; None = no lower bound
    "date_end":   date | None,   # inclusive upper bound; None = no upper bound
    "selected_categories": list[str],  # empty list = all categories
}
```

**Returns**: Filtered `pd.DataFrame` (may be empty if no rows match).

**Contract**: An empty result MUST be returned as an empty DataFrame with the same
schema — callers MUST handle the empty case gracefully (render an empty-state message,
not an error).

---

## `get_kpi_metrics(df: pd.DataFrame) -> dict`

Computes headline KPI values from the (already filtered) DataFrame.

**Returns**:

```python
{
    "total_sales":  float,   # sum of total_amount
    "total_orders": int,     # count of unique order_id values
}
```

---

## `get_time_series(df: pd.DataFrame, granularity: str) -> pd.DataFrame`

Aggregates sales by time period for the trend chart.

**Parameters**:

| Name          | Type           | Values              |
|---------------|----------------|---------------------|
| `df`          | `pd.DataFrame` | Filtered dataset    |
| `granularity` | `str`          | `"daily"` or `"monthly"` |

**Returns**: DataFrame with columns `["period", "total_sales"]`, sorted ascending by
`period`. `period` is a `datetime64` value (day-start for daily, month-start for
monthly).

---

## `get_category_summary(df: pd.DataFrame) -> pd.DataFrame`

Aggregates sales by product category, sorted descending.

**Returns**: DataFrame with columns `["category", "total_sales"]`.

---

## `get_region_summary(df: pd.DataFrame) -> pd.DataFrame`

Aggregates sales by geographic region, sorted descending.

**Returns**: DataFrame with columns `["region", "total_sales"]`.
