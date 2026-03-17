<!--
SYNC IMPACT REPORT
==================
Version change: (unversioned template) → 1.0.0
Modified principles: N/A (initial ratification)
Added sections:
  - Core Principles (5 principles)
  - Technology Stack & Constraints
  - Development Workflow
  - Governance
Removed sections: N/A
Templates reviewed:
  - .specify/templates/plan-template.md  ✅ compatible (Constitution Check section present)
  - .specify/templates/spec-template.md  ✅ compatible (mandatory sections align)
  - .specify/templates/tasks-template.md ✅ compatible (phase/story structure unchanged)
Deferred TODOs: none
-->

# E-Commerce Analytics Dashboard Constitution

## Core Principles

### I. Performance-First

Dashboard load time and data processing efficiency are non-negotiable constraints, not
afterthoughts. Concretely:

- Initial page render MUST complete within 3 seconds on a standard broadband connection.
- Data transformations MUST use vectorized Pandas operations; row-iteration loops are
  prohibited in hot paths.
- Hybrid data (static CSV + live API sources) MUST be cached at the appropriate layer:
  static reference data cached at startup, live transactional data cached with an
  explicit TTL (default: 5 minutes).
- Any new chart or KPI widget MUST be profiled before merge; regressions >10% require
  justification.

**Rationale**: The primary audience includes executives who will abandon a slow dashboard.
Performance is a feature, not polish.

### II. Audience Clarity (NON-NEGOTIABLE)

Every visual element MUST be interpretable by a non-technical business user without
tooltip or documentation assistance. Concretely:

- Chart titles MUST state the business question being answered (e.g., "Sales by Region —
  Last 30 Days"), not the chart type.
- KPI scorecards MUST display units and time context inline (e.g., "$1.2M total revenue,
  Jan–Mar 2024").
- Color palettes MUST meet WCAG AA contrast standards.
- No raw column names, data-type labels, or technical identifiers MUST appear in any
  user-facing element.

**Rationale**: The mixed audience (executives + analysts) means the lowest common
denominator governs UI copy, not the highest.

### III. Data Integrity & Hybrid Source Discipline

Static and live data sources MUST be treated as distinct layers with explicit contracts.
Concretely:

- The data layer MUST expose a single `load_data()` interface that abstracts whether
  data is read from CSV or a live source; callers MUST NOT branch on source type.
- Schema validation (column names, dtypes, non-null constraints) MUST run at load time
  for both sources; invalid data MUST raise an informative error, not silently corrupt
  charts.
- Live data failures MUST degrade gracefully: fall back to the most recent cached
  snapshot and display a staleness banner to the user.
- Reference data (product categories, region mappings) MUST be versioned in
  `data/` and MUST NOT be fetched dynamically.

**Rationale**: Hybrid sources are the most common cause of subtle data bugs in dashboards.
Explicit contracts prevent silent inconsistencies.

### IV. Minimal, Justified Stack

Dependencies MUST be limited to what is required. Adding a library requires written
justification in the PR description. Concretely:

- Core stack is fixed: Python 3.11+, Streamlit, Plotly, Pandas. No alternatives to these
  four are permitted without a constitution amendment.
- Additional libraries MUST each solve a problem that cannot be solved with the core
  stack within a reasonable effort threshold.
- `uv` is the ONLY permitted package manager for this project.
- No dashboard feature MUST require a backend service or database beyond what the hybrid
  data model provides.

**Rationale**: A minimal stack reduces onboarding friction for workshop participants and
lowers long-term maintenance burden.

### V. Traceability

Every change MUST be traceable from code back to a Jira issue. Concretely:

- Every commit message MUST include a Jira issue key (e.g., `ECOM-1`).
- PRs MUST reference the originating Jira issue in their description.
- Spec-kit artifacts (constitution → specification → plan → tasks) MUST be produced in
  order before implementation begins on any non-trivial feature.
- Task IDs in `tasks.md` MUST map 1:1 to Jira subtasks; ad-hoc work without a Jira issue
  is prohibited.

**Rationale**: Traceability is a first-class learning objective of this tutorial. It also
ensures any contributor can reconstruct the "why" behind any line of code.

## Technology Stack & Constraints

**Language**: Python 3.11+
**UI Framework**: Streamlit (latest stable)
**Visualization**: Plotly Express (preferred) or Plotly Graph Objects for custom charts
**Data Processing**: Pandas
**Package Manager**: uv
**Primary Data Source**: `data/sales-data.csv` (static reference)
**Secondary Data Source**: Live transactional API (hybrid layer — see Principle III)
**Deployment Target**: Streamlit Cloud
**Reference Dashboard**: https://sales-dashboard-greg-lontok.streamlit.app/

**Constraints**:
- No SQL database or ORM.
- No authentication layer (internal tool, network-restricted).
- Dashboard MUST run with a single `streamlit run dashboard.py` command after `uv` install.
- All secrets (API keys for live data) MUST be managed via Streamlit Cloud secrets
  or `.streamlit/secrets.toml` locally; MUST NOT be committed to the repository.

## Development Workflow

1. **Spec before code**: For any feature beyond a trivial bug fix, produce spec-kit
   artifacts in order: constitution (this doc) → `spec.md` → `plan.md` → `tasks.md`.
2. **Jira first**: Create or identify the Jira issue (`ECOM-N`) before writing any code.
3. **Branch per issue**: One feature branch per Jira issue, named `ECOM-N-short-description`.
4. **Commit discipline**: Every commit references its Jira key. Squash commits are
   permitted before merge but the final commit message MUST retain the issue key.
5. **Deploy on merge**: Merges to `main` MUST be deployable to Streamlit Cloud immediately.
   No "WIP on main" commits.
6. **UI caveat**: Streamlit Cloud and Atlassian UIs change frequently. Tutorial
   instructions MUST include a caveat that participants should adapt when steps diverge
   from screenshots.

## Governance

This constitution supersedes all other practices and conventions in this repository.

- **Amendments** require: (1) a written rationale, (2) a version bump per the policy
  below, (3) an updated `LAST_AMENDED_DATE`, and (4) a review of all dependent
  spec-kit artifacts for consistency.
- **Versioning policy**:
  - MAJOR: Removal or redefinition of a core principle.
  - MINOR: New principle or section added; material expansion of existing guidance.
  - PATCH: Clarifications, wording fixes, non-semantic refinements.
- **Compliance**: All PRs MUST verify that changes satisfy the five core principles.
  The `Constitution Check` gate in `plan.md` MUST be completed before implementation
  begins.
- **Complexity justification**: Any deviation from Principle IV (Minimal Stack) MUST be
  documented in the `Complexity Tracking` table of the relevant `plan.md`.

**Version**: 1.0.0 | **Ratified**: 2026-03-13 | **Last Amended**: 2026-03-13
