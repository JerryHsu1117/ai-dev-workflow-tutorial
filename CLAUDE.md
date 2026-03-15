# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A tutorial teaching an AI-assisted development workflow. Participants build and deploy an e-commerce sales dashboard (Streamlit + Python) while learning the full professional dev cycle: PRD → spec-kit → Jira → code → Git → deploy.

This repo is primarily documentation. The dashboard code participants write lives in their own forks, not here.

## Repository structure

```
v2/                         # Current version (async pre-work + 3-hour workshop)
  pre-work-setup.md         # Accounts, tools, repo setup (~60-90 min solo)
  workshop-build-deploy.md  # Spec-kit, Jira, build, deploy (~3 hours live)
v1/                         # Original version (two 100-min sessions)
prd/ecommerce-analytics.md  # The PRD participants build from
data/sales-data.csv         # Sample dataset (~1000 transaction records)
```

## The workflow participants follow

```
PRD → spec-kit → Jira → Code (Claude Code) → Commit → Push (GitHub) → Deploy (Streamlit Cloud)
```

Key concepts the tutorial teaches:
- **Traceability**: Jira issue keys (e.g., `ECOM-1`) included in every commit message
- **Spec-driven development**: constitution → specification → plan → tasks, before any code
- **MCP integration**: Claude Code connects to Jira via Model Context Protocol

## Dashboard being built

Streamlit app with: KPI scorecards (Total Sales, Total Orders), sales trend line chart, sales-by-category bar chart, sales-by-region bar chart. Stack: Python 3.11+, Streamlit, Plotly, Pandas. Data source: `data/sales-data.csv`.

## Running the dashboard (when participants have built it)

```bash
# Install dependencies with uv
uv add streamlit plotly pandas

# Run locally
streamlit run dashboard.py
```

## Tool versions expected

```bash
git --version        # 2.x.x
python --version     # 3.11+
claude --version     # any current version
uv --version         # any current version
```

## When editing tutorial documents

- Both `v2/pre-work-setup.md` and `v2/workshop-build-deploy.md` contain UI-dependent instructions. Add or preserve the caveat that UIs change frequently and participants should adapt when steps don't match exactly.
- The finished dashboard reference: https://sales-dashboard-greg-lontok.streamlit.app/
- Jira issue key format used throughout: `ECOM-N`
