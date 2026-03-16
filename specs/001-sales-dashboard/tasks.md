# Tasks: ShopSmart Sales Analytics Dashboard

**Input**: Design documents from `specs/001-sales-dashboard/`
**Prerequisites**: plan.md ✅ | spec.md ✅ | data-model.md ✅ | contracts/ ✅ | research.md ✅

**Approach**: TDD — tests MUST be written and verified to FAIL before implementation begins.
**Granularity**: Module-level — one task per file.
**Foundational**: Full `src/` package implemented and tested before any page work begins.
**MVP**: All four user stories required.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1–US4)
- Exact file paths included in every task description

---

## Phase 1: Setup

**Purpose**: Project initialization and directory scaffolding.

- [x] T001 Create directory structure: `src/`, `pages/`, `tests/unit/`, `tests/integration/`, `data/`, `.streamlit/`
- [x] T002 Create `pyproject.toml` with dependencies (`streamlit>=1.28`, `plotly>=5.0`, `pandas>=2.0`) and dev group (`pytest>=8.0`) managed by `uv`
- [x] T003 [P] Create `.streamlit/config.toml` with `layout = "wide"` and theme defaults
- [x] T004 [P] Create `src/__init__.py`, `tests/__init__.py`, `tests/unit/__init__.py`, `tests/integration/__init__.py`

**Checkpoint**: `uv sync` completes without errors.

---

## Phase 2: Foundational — Full `src/` Package

**Purpose**: Implement and unit-test all shared logic before any Streamlit page is built.
All three modules are tested and verified before user story page work begins.

**⚠️ CRITICAL**: No user story page work can begin until this phase is complete.

### Tests for Foundational ⚠️ Write FIRST — verify they FAIL before implementing

- [x] T005 [P] Write failing unit tests for all `src/data.py` functions (`load_data` happy path + schema errors, `apply_filters` date/category/combined/empty cases, `get_kpi_metrics` totals, `get_time_series` daily + monthly aggregations, `get_category_summary` sort order, `get_region_summary` sort order) in `tests/unit/test_data.py`
- [x] T006 [P] Write failing unit tests for all `src/charts.py` functions (`make_trend_chart` returns Plotly Figure with correct title + axes, `make_category_chart` horizontal bar with business-question title, `make_region_chart` horizontal bar with business-question title) in `tests/unit/test_charts.py`
- [x] T007 [P] Write failing unit tests for all `src/filters.py` functions (`init_filter_state` default values from dataset, idempotency; filter state dict structure) in `tests/unit/test_filters.py`

### Implementation for Foundational

- [x] T008 Implement `src/data.py` — `load_data()` with `@st.cache_data` and schema validation, `apply_filters(df, filters)` AND logic returning empty DataFrame on no match, `get_kpi_metrics(df)`, `get_time_series(df, granularity)`, `get_category_summary(df)`, `get_region_summary(df)`
- [x] T009 [P] Implement `src/charts.py` — `make_trend_chart(df, granularity)` using `px.line` with title "Sales Over Time", `make_category_chart(df)` using horizontal `px.bar` with title "Which Categories Drive Revenue?", `make_region_chart(df)` using horizontal `px.bar` with title "Sales Performance by Region"
- [x] T010 [P] Implement `src/filters.py` — `init_filter_state(df)` idempotent session state init with date bounds and empty category list, `render_date_filter(df)` sidebar date inputs + Last 30 Days / Last 90 Days / Year to Date / All Time presets, `render_category_filter(df)` inline multiselect populated from dataset

**Checkpoint**: `uv run pytest tests/unit/` — all unit tests pass. The entire `src/` package is verified before any page is written.

---

## Phase 3: User Story 1 — At-a-Glance KPI Overview (Priority: P1) 🎯 MVP Start

**Goal**: Home page displays Total Sales and Total Orders as formatted KPI scorecards on load.

**Independent Test**: Open the dashboard; verify Total Sales ≈ $650–700k and Total Orders = 482
with no filters applied. Values must match manual CSV calculations.

### Tests for US1 ⚠️ Write FIRST — verify they FAIL before implementing

- [x] T011 [US1] Write failing AppTest for KPI scorecards in `tests/integration/test_home.py` — assert Total Sales displays as currency string, Total Orders as integer, both visible without filter interaction

### Implementation for US1

- [x] T012 [US1] Implement KPI display in `dashboard.py` — call `load_data()`, `init_filter_state(df)`, `render_date_filter(df)` (sidebar), `get_kpi_metrics(df)`, display with `st.metric`; show `st.error()` on load failure; `st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")`

**Checkpoint**: `uv run pytest tests/integration/test_home.py` — US1 tests pass.
Dashboard shows correct KPI values. Deployable as MVP.

---

## Phase 4: User Story 2 — Sales Trend Over Time (Priority: P2)

**Goal**: Interactive line chart below KPIs with a Monthly/Daily granularity toggle; chart
updates without page reload.

**Independent Test**: Load the dashboard; verify line chart renders with correct monthly
totals. Toggle to daily; verify one data point per day. Hover tooltip shows exact value.

### Tests for US2 ⚠️ Write FIRST — verify they FAIL before implementing

- [x] T013 [US2] Write failing AppTest for trend chart presence and granularity radio button in `tests/integration/test_home.py` — assert chart renders, toggle exists with Monthly/Daily options, selecting Daily changes chart data

### Implementation for US2

- [x] T014 [US2] Add trend chart and granularity toggle to `dashboard.py` — `st.radio` for granularity stored in `st.session_state["trend_granularity"]` (default "Monthly"), call `get_time_series(filtered_df, granularity)`, render with `make_trend_chart()`; pass date-filtered df from existing filter wiring

**Checkpoint**: `uv run pytest tests/integration/test_home.py` — US1 + US2 tests pass.
Granularity toggle re-renders chart without page reload.

---

## Phase 5: User Story 3 — Category and Region Breakdowns (Priority: P3)

**Goal**: Segment Analysis page with two side-by-side horizontal bar charts — Sales by
Category and Sales by Region — both sorted descending.

**Independent Test**: Navigate to Segment Analysis; verify both charts render with all 5
categories and 4 regions sorted by sales descending. Chart totals match CSV aggregations.

### Tests for US3 ⚠️ Write FIRST — verify they FAIL before implementing

- [ ] T015 [US3] Write failing AppTest for Segment Analysis page in `tests/integration/test_segment.py` — assert page title visible, both charts present, category multiselect widget exists

### Implementation for US3

- [ ] T016 [US3] Implement `pages/1_Segment_Analysis.py` — `st.set_page_config`, call `load_data()`, `init_filter_state(df)`, `render_date_filter(df)` (sidebar), `render_category_filter(df)` (inline above category chart), `apply_filters(df, filters)`, display category and region charts side-by-side using `st.columns(2)` with `make_category_chart()` and `make_region_chart()`

**Checkpoint**: `uv run pytest tests/integration/test_segment.py` — US3 tests pass.
Navigate to Segment Analysis in browser; both charts render with correct sorted data.

---

## Phase 6: User Story 4 — Interactive Filtering (Priority: P4) 🏁 MVP Complete

**Goal**: Date range filter (sidebar) and category filter (inline) update all KPIs and charts
simultaneously via shared session state.

**Independent Test**: Select a single category; verify all KPIs and both charts reflect only
that category's data. Combined total matches manual CSV calculation. Clear filters; full
dataset values restore.

### Tests for US4 ⚠️ Write FIRST — verify they FAIL before implementing

- [ ] T017 [P] [US4] Write failing AppTest for date filter preset interactions in `tests/integration/test_home.py` — assert Last 30 Days / Last 90 Days presets update KPI values correctly
- [ ] T018 [P] [US4] Write failing AppTest for category filter propagation in `tests/integration/test_segment.py` — assert selecting one category updates region chart totals and KPIs to match filtered subset

### Implementation for US4

- [ ] T019 [US4] Wire filter state propagation in `dashboard.py` — pass `apply_filters(df, st.session_state["filters"])` result to `get_kpi_metrics` and `get_time_series`; add `st.info("No data matches the selected filters.")` empty-state guard before each component
- [ ] T020 [US4] Wire filter state propagation in `pages/1_Segment_Analysis.py` — pass `apply_filters(df, st.session_state["filters"])` result to `get_category_summary` and `get_region_summary`; add empty-state guard before each chart

**Checkpoint**: `uv run pytest` — all US1–US4 tests pass. Apply date + category filter
simultaneously; all four components update. Clear filters; full dataset values restore.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and quality pass.

- [ ] T021 [P] Verify no raw column names appear in any user-facing element across `dashboard.py` and `pages/1_Segment_Analysis.py` (chart axes, labels, KPI titles must use business language per Constitution Principle II)
- [ ] T022 Run complete test suite: `uv run pytest -v` — zero failures, zero warnings
- [ ] T023 Run quickstart.md validation checklist — install fresh via `uv sync`, run `streamlit run dashboard.py`, verify all 8 checklist items pass manually

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 — BLOCKS all user story phases
- **US1 (Phase 3)**: Depends on Foundational complete
- **US2 (Phase 4)**: Depends on US1 (trend chart sits on same page as KPIs)
- **US3 (Phase 5)**: Depends on Foundational — independent of US1/US2, can run in parallel with US2
- **US4 (Phase 6)**: Depends on US1 + US2 + US3 complete (filter must update all components)
- **Polish (Phase 7)**: Depends on all stories complete

### Within Each User Story (TDD Order)

1. Write tests → run → verify they FAIL (red)
2. Implement → run tests → verify they PASS (green)
3. Story checkpoint → validate independently before next story

### Parallel Opportunities

| Phase | Parallel tasks |
|-------|---------------|
| Phase 1 | T003, T004 |
| Phase 2 (tests) | T005, T006, T007 |
| Phase 2 (impl) | T009, T010 (after T008 complete) |
| Phase 6 (tests) | T017, T018 |
| Phase 7 | T021 |

---

## Parallel Example: Foundational Phase (highest parallelism)

```bash
# All 3 unit test files in parallel (all write to different files):
Task T005: tests/unit/test_data.py
Task T006: tests/unit/test_charts.py
Task T007: tests/unit/test_filters.py

# After T005–T007 verified failing:
# T008 runs first (data.py — charts.py and filters.py have no dependency on it at unit level)
# T009 and T010 can run in parallel after T008:
Task T009: src/charts.py
Task T010: src/filters.py
```

---

## Implementation Strategy

### TDD Cycle (per phase)

1. Write all test tasks for the phase → confirm they fail
2. Implement modules → re-run tests after each file
3. All tests green → run phase checkpoint
4. Move to next phase

### MVP First (US1 — 6 tasks)

1. Complete Phase 1: Setup (T001–T004)
2. Complete Phase 2: Foundational (T005–T010)
3. Complete Phase 3: US1 (T011–T012)
4. **STOP and VALIDATE**: KPI scorecards show correct values → deployable

### Incremental Delivery

1. Setup + Foundational → full `src/` verified
2. US1 (T011–T012) → KPI dashboard deployable
3. US2 (T013–T014) → add trend chart → deploy
4. US3 (T015–T016) → add segment analysis page → deploy
5. US4 (T017–T020) → add filtering → full MVP → deploy
6. Polish (T021–T023) → production-ready

### Parallel Team Strategy (2 developers)

- **Phase 2 tests**: All three test files in parallel (T005, T006, T007)
- **After T008**: Developer A on `src/charts.py` (T009), Developer B on `src/filters.py` (T010)
- **After Foundational**: Developer A on US1→US2 (same page), Developer B on US3 (different page)
- **US4**: Both join to wire filter propagation (different files: T019, T020 parallelizable)

---

## Notes

- `[P]` tasks write to different files with no shared state — safe to run simultaneously
- TDD is non-negotiable: tests MUST fail before implementation begins
- `apply_filters()` lives in `src/data.py`; filter UI lives in `src/filters.py` (per data contract)
- Empty filtered DataFrame must never raise an exception — always show `st.info()` empty state
- All chart titles must answer a business question, not name the chart type (Constitution II)
- Commit after each phase checkpoint with Jira issue key in the message (Constitution V)
