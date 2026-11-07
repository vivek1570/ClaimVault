# Health Insurance Data Engineering Project — Complete Project Plan (Markdown)

Below is the complete project plan as a Markdown file. Copy everything between the `---BEGIN---` and `---END---` markers, save it as `PROJECT_PLAN.md`, and you're ready to go.

```
---BEGIN PROJECT_PLAN.md---

# 🏥 Health Insurance Data Engineering Project
## Medallion Architecture | Python + SQL + Streamlit | 1-Month Plan for 2 People

---

## 📌 Table of Contents
1. [Project Overview](#1-project-overview)
2. [Team & Roles](#2-team--roles)
3. [Tech Stack](#3-tech-stack)
4. [Architecture (Medallion)](#4-architecture-medallion)
5. [Schema Modeling](#5-schema-modeling)
6. [Feature Roadmap](#6-feature-roadmap)
7. [Repository Structure](#7-repository-structure)
8. [GitHub Setup & Workflow](#8-github-setup--workflow)
9. [Day-by-Day Execution Plan (20 Working Days)](#9-day-by-day-execution-plan-20-working-days)
10. [Data Quality & Testing](#10-data-quality--testing)
11. [Dashboard Specification](#11-dashboard-specification)
12. [Deployment Plan](#12-deployment-plan)
13. [Definition of Done](#13-definition-of-done)
14. [Risks & Mitigations](#14-risks--mitigations)
15. [Stretch Goals (Post-MVP)](#15-stretch-goals-post-mvp)
16. [Final Deliverables Checklist](#16-final-deliverables-checklist)

---

## 1. Project Overview

**Goal:** Build a complete, end-to-end data project from scratch using public health insurance claims data. The project will implement a **Medallion Architecture** (Bronze → Silver → Gold) using **Python** for ingestion and **SQL** for modeling, version-controlled in **GitHub**, and surfaced through an interactive **Streamlit dashboard**.

**Duration:** 1 month (~20 working days)
**Team Size:** 2 people
**Domain:** Health Insurance Claims (patients, providers, diagnoses, claim amounts)

**Success Criteria:**
- A reproducible pipeline that ingests raw data into a Bronze layer, cleans and models it into Silver and Gold layers.
- A live dashboard showing at least 4 KPIs and 3 charts, filterable by date and region.
- Full documentation, GitHub issues tracking, and a demo-ready repository.

---

## 2. Team & Roles

| Role | Person | Primary Responsibilities |
| :--- | :--- | :--- |
| **Data Engineer** | Person A | Python ingestion, orchestration, pipeline scripting, deployment |
| **Analytics Engineer** | Person B | SQL modeling (Silver/Gold), data quality, dashboard data queries |

**Shared responsibilities:** Schema design, GitHub management, dashboard UI, documentation, final presentation.

> **Rule:** Both people review each other's pull requests. No direct pushes to `main`.

---

## 3. Tech Stack

| Layer | Tool | Purpose |
| :--- | :--- | :--- |
| Language | Python 3.11+ | Ingestion, transformations, orchestration |
| Database | PostgreSQL 15+ | Storage for all Medallion layers |
| Python Libraries | `pandas`, `sqlalchemy`, `psycopg2-binary`, `python-dotenv` | Data handling & DB connection |
| Dashboard | Streamlit | Interactive BI layer |
| Version Control | Git + GitHub (Projects, Issues, PRs) | Collaboration & tracking |
| Environment | `venv` + `.env` file | Isolated dependencies & secrets |
| (Optional) | `scikit-learn` | Fraud/anomaly flagging |
| (Optional) | `dbt` | SQL transformation framework |
| (Optional) | `pytest` | Data quality tests |

---

## 4. Architecture (Medallion)

```
┌─────────────────────────────────────────────────────────────────┐
│                    DATA SOURCE (Public CSV)                     │
│         e.g., Kaggle Health Insurance Claims Dataset            │
└───────────────────────────────┬─────────────────────────────────┘
                                │  Python ingest.py
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  🥉 BRONZE LAYER  (raw, immutable, as-is)                       │
│  • bronze.raw_claims                                            │
│  • Loaded exactly as received — no cleaning                      │
└───────────────────────────────┬─────────────────────────────────┘
                                │  Python/SQL transform
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  🥈 SILVER LAYER  (cleaned, typed, deduplicated)                │
│  • silver.stg_claims                                            │
│  • silver.dim_patients                                          │
│  • silver.dim_providers                                         │
└───────────────────────────────┬─────────────────────────────────┘
                                │  SQL aggregations
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  🥇 GOLD LAYER  (business-ready, aggregated)                    │
│  • gold.fct_claims                                              │
│  • gold.agg_provider                                            │
│  • gold.fraud_flags (optional)                                  │
└───────────────────────────────┬─────────────────────────────────┘
                                │  SQL queries via SQLAlchemy
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  📊 STREAMLIT DASHBOARD  (KPIs, charts, filters)                │
└─────────────────────────────────────────────────────────────────┘
```

**Rules:**
- Bronze is **write-once** (append-only) — never modify source data.
- Silver is the **single source of truth** for cleaning logic.
- Gold is the **only layer** the dashboard queries.
- Every layer has its own PostgreSQL schema (`bronze`, `silver`, `gold`).

---

## 5. Schema Modeling

### 🥉 Bronze
```sql
-- bronze.raw_claims
claim_id            TEXT
patient_id          TEXT
provider_id         TEXT
diagnosis_code      TEXT
procedure_code      TEXT
claim_date          TEXT          -- kept as TEXT (raw)
claim_amount        TEXT          -- kept as TEXT (raw)
patient_age         TEXT
patient_gender      TEXT
region              TEXT
ingested_at         TIMESTAMP
```

### 🥈 Silver
```sql
-- silver.stg_claims
claim_id            TEXT PRIMARY KEY
patient_id          TEXT NOT NULL
provider_id         TEXT NOT NULL
diagnosis_code      TEXT
procedure_code      TEXT
claim_date          DATE
claim_amount        NUMERIC(12,2)
region              TEXT
loaded_at           TIMESTAMP

-- silver.dim_patients
patient_id          TEXT PRIMARY KEY
age                 INT
age_band            TEXT          -- e.g., '18-34', '35-54', '55+'
gender              TEXT
region              TEXT

-- silver.dim_providers
provider_id         TEXT PRIMARY KEY
provider_name       TEXT
specialty           TEXT
region              TEXT
```

### 🥇 Gold
```sql
-- gold.fct_claims  (one row per claim, enriched)
claim_id            TEXT PRIMARY KEY
patient_id          TEXT
provider_id         TEXT
claim_date          DATE
claim_month         DATE          -- truncated to month
claim_amount        NUMERIC(12,2)
diagnosis_code      TEXT
age_band            TEXT
region              TEXT

-- gold.agg_provider  (one row per provider)
provider_id         TEXT PRIMARY KEY
provider_name       TEXT
specialty           TEXT
total_claims        INT
total_claim_amount  NUMERIC(14,2)
avg_claim_amount    NUMERIC(12,2)
rank_by_cost        INT           -- window function

-- gold.fraud_flags (optional)
claim_id            TEXT PRIMARY KEY
anomaly_score       NUMERIC(6,4)
is_flagged          BOOLEAN
```

---

## 6. Feature Roadmap

| # | Feature | Layer | Owner | Priority |
| :--- | :--- | :--- | :--- | :--- |
| F1 | Raw claims ingestion | Bronze | Person A | Must |
| F2 | Claims cleaning & dedup | Silver | Person B | Must |
| F3 | Patient dimension (age bands) | Silver | Person B | Must |
| F4 | Provider dimension | Silver | Person A | Must |
| F5 | Claims fact table | Gold | Person B | Must |
| F6 | Provider aggregation & ranking | Gold | Person B | Must |
| F7 | KPI cards (Total Claims, Total Cost, Avg Cost, High-Risk Count) | Dashboard | Person A | Must |
| F8 | Claims over time (line chart) | Dashboard | Person A | Must |
| F9 | Claims by region (bar chart) | Dashboard | Person B | Must |
| F10 | Top 10 providers by cost (table/bar) | Dashboard | Person B | Must |
| F11 | Date range + region filters | Dashboard | Both | Must |
| F12 | Fraud/anomaly flags (Isolation Forest) | Gold | Person A | Nice |
| F13 | Diagnosis distribution (pie chart) | Dashboard | Person B | Nice |
| F14 | Data quality test suite (pytest) | Pipeline | Person A | Nice |
| F15 | Scheduled pipeline (cron/Task Scheduler) | Ops | Person A | Nice |

---

## 7. Repository Structure

```
health-insurance-de-project/
│
├── .github/
│   └── workflows/
│       └── ci.yml                  # (optional) lint + test on PR
│
├── data/
│   ├── raw/                        # downloaded CSV (gitignored)
│   └── .gitkeep
│
├── sql/
│   ├── 00_create_schemas.sql
│   ├── 01_bronze_tables.sql
│   ├── 02_silver_tables.sql
│   ├── 03_gold_tables.sql
│   └── 04_dashboard_queries.sql
│
├── src/
│   ├── __init__.py
│   ├── config.py                   # loads .env
│   ├── db.py                       # SQLAlchemy engine
│   ├── ingest.py                   # Bronze loader
│   ├── transform_silver.py         # Bronze → Silver
│   ├── transform_gold.py           # Silver → Gold
│   ├── quality_checks.py           # assertions
│   └── pipeline.py                 # orchestrates all steps
│
├── dashboard/
│   └── app.py                      # Streamlit app
│
├── tests/
│   ├── test_ingest.py
│   └── test_transforms.py
│
├── docs/
│   ├── architecture.md
│   ├── data_dictionary.md
│   └── screenshots/
│
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── PROJECT_PLAN.md                 # this file
```

---

## 8. GitHub Setup & Workflow

### Initial Setup (Day 1)
1. Create a **GitHub Organization** (or use one account with collaborator access).
2. Create a new **private repository** `health-insurance-de-project`.
3. Add both team members as collaborators with **write** access.
4. Enable **branch protection** on `main`: require PR + 1 approval.
5. Create a **GitHub Project** (Kanban) with columns:
   - `Backlog` → `In Progress` → `In Review` → `Done`
6. Create **labels**: `bronze`, `silver`, `gold`, `dashboard`, `bug`, `docs`.
7. Add a `.gitignore` (include `.env`, `data/raw/`, `__pycache__/`, `venv/`).
8. Create `.env.example` with placeholder credentials.

### Daily Workflow
- **Morning (10 min standup):** Review the Project board. Pick today's issues. Assign owners.
- **Create a branch per task:** `feat/bronze-ingest`, `feat/silver-claims`, `fix/dashboard-filter`.
- **Commit often** with clear messages: `feat(silver): add stg_claims dedup logic`.
- **Open a PR** when done. The other person reviews within the same day.
- **Merge to `main`** only after review. Update the Project board to `Done`.

### Issue Template (suggested)
```
## Task
<short description>

## Layer
Bronze / Silver / Gold / Dashboard

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Owner
@person-a / @person-b

## Day
Day X
```

---

## 9. Day-by-Day Execution Plan (20 Working Days)

### 🗓️ WEEK 1 — Foundations, Setup & Bronze Layer

| Day | Person A (Data Engineer) | Person B (Analytics Engineer) | Shared / Checkpoint |
| :--- | :--- | :--- | :--- |
| **1** | Create GitHub org/repo, `.gitignore`, `.env.example`, `requirements.txt`, Python venv | Create GitHub Project board, issues for Week 1, labels | Agree on schema (Section 5), commit `PROJECT_PLAN.md` |
| **2** | Download public health insurance CSV to `data/raw/`. Write `src/config.py` and `src/db.py` | Install PostgreSQL, create `bronze`/`silver`/`gold` schemas via `sql/00_create_schemas.sql` | Profile raw CSV: row count, columns, nulls |
| **3** | Write `src/ingest.py` — load raw CSV → `bronze.raw_claims` using SQLAlchemy | Write `sql/01_bronze_tables.sql` (verify column types). Write profiling queries | Run ingestion end-to-end. Verify row counts match |
| **4** | Draft `src/transform_silver.py` — clean dates, cast amounts, drop duplicates | Write `sql/02_silver_tables.sql` for `stg_claims`, `dim_patients`, `dim_providers` | PR review: Person A reviews SQL, Person B reviews Python |
| **5** | Finish Silver transform for `stg_claims` and load into DB | Write SQL logic to build `dim_patients` (age bands) and `dim_providers` | Merge Bronze + Silver PRs to `main`. Update board |

**Week 1 Checkpoint:** Bronze layer fully loaded. Silver `stg_claims` populated. Dimensions designed.

---

### 🗓️ WEEK 2 — Silver & Gold Layers

| Day | Person A | Person B | Shared / Checkpoint |
| :--- | :--- | :--- | :--- |
| **6** | Write `src/pipeline.py` to orchestrate ingest → silver in one command | Write `sql/03_gold_tables.sql` for `fct_claims` | Run `python src/pipeline.py` — full Bronze→Silver works |
| **7** | Implement `src/transform_gold.py` to build `fct_claims` | Write window-function SQL for `gold.agg_provider` (rank_by_cost) | PR review both gold scripts |
| **8** | Write `src/quality_checks.py` — assert non-null IDs, positive amounts, unique claim_id | Add data quality checks for dim tables (valid age_band, no orphan patient_ids) | Merge gold layer to `main`. Update board |
| **9** | Write `docs/architecture.md`, update `README.md` with setup instructions | Write `docs/data_dictionary.md` (every column, type, description) | Full pipeline runs end-to-end in < 5 min |
| **10** | (Optional) Set up cron / Task Scheduler to run `pipeline.py` daily | (Optional) Start `scikit-learn` anomaly detection notebook | **Week 2 review:** All Medallion layers populated |

**Week 2 Checkpoint:** Bronze → Silver → Gold pipeline runs end-to-end. Documentation exists.

---

### 🗓️ WEEK 3 — Analytics, Dashboard Build

| Day | Person A | Person B | Shared / Checkpoint |
| :--- | :--- | :--- | :--- |
| **11** | (Optional) Add `gold.fraud_flags` via Isolation Forest. Write `sql/04_dashboard_queries.sql` | Write dashboard SQL queries: KPIs, region agg, provider top-10, time series | Agree on exact dashboard layout |
| **12** | Streamlit skeleton: `dashboard/app.py`, DB connection via `@st.cache_data` | Streamlit layout: sidebar filters (date range, region multiselect) | First dashboard page loads locally |
| **13** | Build KPI row (4 `st.metric` cards) driven by filtered query | Build line chart (claims over time) + bar chart (claims by region) | Filters update KPIs + charts |
| **14** | Build "Top 10 Providers by Cost" table/bar chart | Build "Recent High-Cost Claims" table + diagnosis pie chart | All 3+ charts working |
| **15** | Handle empty states (no data message), add titles/descriptions | Add `@st.cache_data` to all queries; tune query performance | **Week 3 review:** Dashboard functional locally |

**Week 3 Checkpoint:** Dashboard runs locally with KPIs, charts, and working filters.

---

### 🗓️ WEEK 4 — Polish, Deploy, Demo

| Day | Person A | Person B | Shared / Checkpoint |
| :--- | :--- | :--- | :--- |
| **16** | Dashboard polish: consistent colors, number formatting, layout spacing | Update `README.md` with dashboard screenshots (`docs/screenshots/`) | Screenshots added to repo |
| **17** | Deployment prep: `requirements.txt` final, `st.secrets` for DB credentials | Final code review: check all PRs merged, `main` clean | All branches merged |
| **18** | Deploy dashboard to Streamlit Community Cloud (or local + tunnel) | Write `docs/data_dictionary.md` final pass; add demo script | Public (or shareable) dashboard URL |
| **19** | Record 5-min demo walkthrough (architecture + code + dashboard) | Prepare demo talking points; finalize `README.md` | Dry-run presentation |
| **20** | Buffer: fix last-minute bugs, tag `v1.0.0` release on GitHub | Buffer: retrospective notes, list of stretch goals | **Final demo + retrospective** |

**Week 4 Checkpoint:** Dashboard deployed. Repo tagged `v1.0.0`. Demo delivered.

---

## 10. Data Quality & Testing

Implement these checks in `src/quality_checks.py` (run at the end of `pipeline.py`):

| Check | Layer | Rule |
| :--- | :--- | :--- |
| Non-null keys | Bronze | `claim_id`, `patient_id`, `provider_id` not null |
| Unique claims | Silver | `COUNT(claim_id) = COUNT(DISTINCT claim_id)` |
| Positive amounts | Silver | `claim_amount > 0` |
| Valid dates | Silver | `claim_date` between 2010-01-01 and today |
| Referential integrity | Gold | Every `patient_id` in `fct_claims` exists in `dim_patients` |
| Aggregation sanity | Gold | `SUM(total_claim_amount)` in `agg_provider` ≈ `SUM(claim_amount)` in `fct_claims` |

**Behavior on failure:** raise an exception, log the row counts, and halt the pipeline. Never load bad data downstream.

**Optional:** wrap each check in `pytest` tests under `tests/`.

---

## 11. Dashboard Specification

### Page 1 — Executive Overview
| Element | Type | Data Source |
| :--- | :--- | :--- |
| Total Claims | KPI card | `gold.fct_claims` |
| Total Claim Amount | KPI card | `gold.fct_claims` |
| Avg Claim Cost | KPI card | `gold.fct_claims` |
| High-Risk Provider Count | KPI card | `gold.agg_provider` (rank_by_cost ≤ 10) |
| Claims over Time | Line chart | `gold.fct_claims` grouped by `claim_month` |
| Claims by Region | Bar chart | `gold.fct_claims` grouped by `region` |
| Top 10 Providers by Cost | Table | `gold.agg_provider` ordered by `total_claim_amount` |
| Diagnosis Distribution | Pie chart | `gold.fct_claims` grouped by `diagnosis_code` (top 8) |

### Global Filters (sidebar)
- **Date range picker** → filters `claim_date`
- **Region multiselect** → filters `region`
- **Age band multiselect** → filters `age_band`

All filters must update *every* chart and KPI on the page.

### UX Rules
- Every chart has a title and axis labels.
- Empty filter result → show `"No data for the selected filters"` (no crash).
- All DB queries wrapped in `@st.cache_data(ttl=600)`.
- No dashboard query touches Bronze or Silver directly — **Gold only**.

---

## 12. Deployment Plan

### Local (Days 1–17)
```bash
# Setup
python -m venv venv
source venv/bin/activate      # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Configure .env (copy from .env.example)
cp .env.example .env
# edit .env with DB credentials

# Run pipeline
python src/pipeline.py

# Launch dashboard
streamlit run dashboard/app.py
```

### Cloud (Day 18) — Streamlit Community Cloud
1. Push final code to `main`.
2. Create a free **Neon** or **Supabase** PostgreSQL instance (if not local).
3. Run `pipeline.py` against the cloud DB once.
4. Connect the GitHub repo to Streamlit Community Cloud.
5. Add DB credentials to Streamlit **Secrets** (`st.secrets["DB_URL"]`).
6. Deploy `dashboard/app.py` as the entry point.
7. Share the public URL in `README.md`.

### Alternative
- **Local only:** run Streamlit locally and screen-share during the demo. Acceptable if time runs short.

---

## 13. Definition of Done

A task is "Done" when:
- [ ] Code is merged to `main` via reviewed PR.
- [ ] The pipeline runs end-to-end without errors.
- [ ] Data quality checks pass.
- [ ] Documentation in `README.md` or `docs/` is updated.
- [ ] GitHub Project card is moved to `Done`.

The **project** is Done when:
- [ ] All 11 "Must" features (Section 6) are complete.
- [ ] Dashboard deployed or demo-ready locally.
- [ ] `README.md` contains setup, architecture diagram, and screenshots.
- [ ] Git tag `v1.0.0` created.
- [ ] 5-minute demo recorded or delivered live.

---

## 14. Risks & Mitigations

| Risk | Likelihood | Mitigation |
| :--- | :--- | :--- |
| No suitable public dataset found | Low | Pre-select 3 candidate Kaggle datasets on Day 1 |
| PostgreSQL setup issues | Medium | Person B owns DB setup; use Docker as fallback |
| Dashboard filters slow / stale | Medium | `@st.cache_data` + single filtered query pattern |
| Scope creep (too many charts) | High | Cap dashboard at 4 KPIs + 3 charts for MVP |
| Missed merge conflicts | Medium | Small PRs, daily merges, branch protection |
| Person unavailable | Medium | Cross-review ensures both know both layers |
| Deployment blocked | Low | Fallback to local demo — documented in plan |

---

## 15. Stretch Goals (Post-MVP)

Only attempt after all "Must" features are done:

1. **dbt integration** — migrate Silver/Gold SQL into dbt models with tests and lineage.
2. **Airflow orchestration** — replace cron with a DAG.
3. **ML fraud detection** — Isolation Forest with precision/recall reporting.
4. **CI/CD** — GitHub Actions to lint (`ruff`, `sqlfluff`) and run `pytest` on every PR.
5. **Data catalog** — generate a data dictionary from DB metadata automatically.
6. **Multi-page dashboard** — add a "Provider Deep-Dive" page.
7. **Alerting** — email/Slack alert when a quality check fails.

---

## 16. Final Deliverables Checklist

- [ ] GitHub repository with branch protection and clean `main`
- [ ] `PROJECT_PLAN.md` (this file)
- [ ] `README.md` with setup, architecture, screenshots
- [ ] `requirements.txt` and `.env.example`
- [ ] `sql/` folder with all schema and dashboard queries
- [ ] `src/` folder with ingest, transform, quality, pipeline scripts
- [ ] `dashboard/app.py` — deployed or demo-ready
- [ ] `docs/architecture.md` and `docs/data_dictionary.md`
- [ ] `docs/screenshots/` with dashboard images
- [ ] GitHub Project board fully closed out
- [ ] Git tag `v1.0.0`
- [ ] 5-minute demo recording or live demo

---

**Good luck — ship it! 🚀**

---END PROJECT_PLAN.md---
```

## How to download this as a file

Since I can't directly send you a file download, use one of these methods:

**Option 1 — Copy & save (easiest):**
1. Copy everything between `---BEGIN PROJECT_PLAN.md---` and `---END PROJECT_PLAN.md---`
2. Paste into any text editor (VS Code, Notepad, etc.)
3. Save as `PROJECT_PLAN.md`
4. Drop it into your project root on Day 1

**Option 2 — GitHub (recommended):**
1. Create the repo first
2. On GitHub, click **Add file → Create new file**
3. Name it `PROJECT_PLAN.md`
4. Paste the content and commit

**Option 3 — Terminal one-liner (Linux/Mac):**
Paste the content into `nano PROJECT_PLAN.md` in your terminal and save.

The file is self-contained — it includes the architecture, schema, day-by-day plan, GitHub workflow, testing strategy, dashboard spec, deployment steps, and a deliverables checklist. Your team can work directly from it on Day 1.