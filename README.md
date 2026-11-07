# 🏥 Health Insurance Data Engineering Project

## Medallion Architecture | Python + SQL + Streamlit | 1-Month Execution Plan

---

> [!NOTE]
> This document serves as the **single source of truth** for the entire project lifecycle. Every architectural decision, task assignment, quality gate, and deployment step is captured here. Both team members should reference this plan daily.

---

## 📌 Table of Contents

| # | Section | Purpose |
|---|---------|---------|
| 1 | [Project Overview](#1-project-overview) | Vision, scope, success criteria |
| 2 | [Team & Roles](#2-team--roles) | Ownership matrix & collaboration rules |
| 3 | [Tech Stack Deep-Dive](#3-tech-stack-deep-dive) | Every tool, why it was chosen, and how it fits |
| 4 | [Architecture — Medallion Pattern](#4-architecture--medallion-pattern) | End-to-end data flow with layer contracts |
| 5 | [Schema Modeling — Full DDL](#5-schema-modeling--full-ddl) | Bronze → Silver → Gold table definitions |
| 6 | [Feature Roadmap & Prioritization](#6-feature-roadmap--prioritization) | MoSCoW-prioritized feature backlog |
| 7 | [Repository Structure](#7-repository-structure) | File-by-file project layout |
| 8 | [GitHub Setup & Workflow](#8-github-setup--workflow) | Branching strategy, PR rules, board setup |
| 9 | [Day-by-Day Execution Plan](#9-day-by-day-execution-plan-20-working-days) | 20-day sprint breakdown with checkpoints |
| 10 | [Data Quality & Testing](#10-data-quality--testing) | Validation rules, test strategy, failure behavior |
| 11 | [Dashboard Specification](#11-dashboard-specification) | Wireframe, component spec, UX rules |
| 12 | [Deployment Plan](#12-deployment-plan) | Local → Cloud deployment path |
| 13 | [Definition of Done](#13-definition-of-done) | Task-level and project-level completion criteria |
| 14 | [Risks & Mitigations](#14-risks--mitigations) | Risk register with contingency plans |
| 15 | [Stretch Goals](#15-stretch-goals-post-mvp) | Post-MVP enhancement roadmap |
| 16 | [Final Deliverables Checklist](#16-final-deliverables-checklist) | Ship-readiness verification |

---

## 1. Project Overview

### 1.1 Vision Statement

Build a **production-grade, end-to-end data engineering project** from scratch using publicly available health insurance claims data. The project demonstrates mastery of the **Medallion Architecture** (Bronze → Silver → Gold), **Python-based data ingestion**, **SQL-based data modeling**, **version-controlled collaboration via GitHub**, and **interactive business intelligence via Streamlit**.

### 1.2 Scope Definition

```mermaid
mindmap
  root((Health Insurance<br/>DE Project))
    Data Ingestion
      CSV Download
      Bronze Loading
      Audit Columns
    Data Modeling
      Silver Cleaning
      Dimension Tables
      Gold Aggregations
    Data Quality
      Null Checks
      Uniqueness
      Referential Integrity
    Dashboard
      KPI Cards
      Time Series
      Regional Analysis
      Provider Rankings
    DevOps
      GitHub Workflow
      Branch Protection
      CI/CD Pipeline
```

### 1.3 Key Parameters

| Parameter | Value |
|-----------|-------|
| **Duration** | 1 month (~20 working days) |
| **Team Size** | 2 people |
| **Domain** | Health Insurance Claims — patients, providers, diagnoses, claim amounts |
| **Data Source** | Public CSV (e.g., Kaggle Health Insurance Claims Dataset) |
| **Architecture** | Medallion (Bronze → Silver → Gold) |
| **Database** | PostgreSQL 15+ |
| **Dashboard** | Streamlit |

### 1.4 Success Criteria

| # | Criterion | Measurement |
|---|-----------|-------------|
| SC-1 | **Reproducible Pipeline** | A single command (`python src/pipeline.py`) ingests raw data → Bronze → Silver → Gold without manual intervention |
| SC-2 | **Live Dashboard** | Shows ≥ 4 KPIs and ≥ 3 charts, filterable by date range, region, and age band |
| SC-3 | **Data Quality Gates** | All quality checks pass (nulls, uniqueness, referential integrity, aggregation sanity) |
| SC-4 | **Documentation** | README with setup instructions, architecture diagram, data dictionary, and screenshots |
| SC-5 | **Demo-Ready Repository** | Clean `main` branch, tagged `v1.0.0`, GitHub Project board fully closed |
| SC-6 | **Presentation** | 5-minute demo walkthrough covering architecture, code, and dashboard |

---

## 2. Team & Roles

### 2.1 Role Assignment

| Role | Person | Primary Focus Areas |
|------|--------|-------------------|
| **Data Engineer** | Person A | Python ingestion scripts, pipeline orchestration, deployment, infrastructure |
| **Analytics Engineer** | Person B | SQL modeling (Silver/Gold layers), data quality rules, dashboard data queries |

### 2.2 Shared Responsibilities

Both team members jointly own:
- Schema design decisions
- GitHub repository management (issues, PRs, board)
- Dashboard UI/UX design
- Documentation and README
- Final presentation / demo

### 2.3 Collaboration Rules

> [!IMPORTANT]
> These rules are non-negotiable for the duration of the project.

1. **No direct pushes to `main`** — all changes go through Pull Requests
2. **Cross-review required** — Person A reviews Person B's PRs and vice versa
3. **Daily standup** — 10 minutes each morning to sync on the Project board
4. **Same-day PR review** — open PRs must be reviewed within the same working day
5. **Commit messages follow conventional commits** — e.g., `feat(silver): add stg_claims dedup logic`

### 2.4 Communication Protocol

```mermaid
flowchart LR
    A[Morning Standup<br/>10 min] --> B[Independent Work<br/>~3 hrs]
    B --> C[PR Review<br/>~30 min]
    C --> D[Independent Work<br/>~3 hrs]
    D --> E[End-of-Day Sync<br/>10 min]
    E --> F[Board Update<br/>5 min]
```

---

## 3. Tech Stack Deep-Dive

### 3.1 Core Stack

| Layer | Tool | Version | Purpose | Why This Tool? |
|-------|------|---------|---------|----------------|
| **Language** | Python | 3.11+ | Ingestion, transformations, orchestration | Industry standard for data engineering; rich library ecosystem |
| **Database** | PostgreSQL | 15+ | Storage for all Medallion layers | Open-source, supports schemas, window functions, CTEs; industry standard |
| **Data Handling** | `pandas` | Latest | DataFrame operations for CSV → DB loading | De facto standard for tabular data manipulation in Python |
| **DB Connection** | `sqlalchemy` | 2.0+ | ORM and connection pooling | Database-agnostic abstraction; works with `pandas.to_sql()` |
| **DB Driver** | `psycopg2-binary` | Latest | PostgreSQL wire protocol | Fastest pure-Python PostgreSQL adapter |
| **Config** | `python-dotenv` | Latest | Load `.env` file into `os.environ` | Keeps secrets out of code; standard 12-factor app practice |
| **Dashboard** | Streamlit | Latest | Interactive BI layer | Fastest path from Python script to deployed web app |
| **Version Control** | Git + GitHub | — | Collaboration, tracking, CI/CD | Industry standard; Projects & Issues for task management |
| **Environment** | `venv` + `.env` | — | Isolated dependencies & secrets | Zero-cost, built into Python; prevents dependency conflicts |

### 3.2 Optional / Stretch Stack

| Tool | Purpose | When to Add |
|------|---------|-------------|
| `scikit-learn` | Fraud/anomaly detection (Isolation Forest) | After all "Must" features are done |
| `dbt` | SQL transformation framework with testing & lineage | Post-MVP if team wants declarative SQL |
| `pytest` | Automated data quality test suite | Week 2+ for regression safety |
| `ruff` | Python linter & formatter | Day 1 for code consistency |
| `sqlfluff` | SQL linter | Day 1 for SQL consistency |
| Docker | Containerized PostgreSQL | Fallback if local PostgreSQL setup fails |

### 3.3 Dependency Map

```mermaid
graph TD
    subgraph "Python Runtime"
        A[pandas] --> B[sqlalchemy]
        B --> C[psycopg2-binary]
        D[python-dotenv] --> E[os.environ]
        F[streamlit] --> B
    end

    subgraph "Database"
        C --> G[(PostgreSQL 15+)]
        G --> H[bronze schema]
        G --> I[silver schema]
        G --> J[gold schema]
    end

    subgraph "Optional"
        K[scikit-learn] -.-> A
        L[pytest] -.-> B
        M[dbt] -.-> G
    end

    style H fill:#cd7f32,color:#fff
    style I fill:#c0c0c0,color:#000
    style J fill:#ffd700,color:#000
```

### 3.4 `requirements.txt` (Baseline)

```text
pandas>=2.0.0
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0
python-dotenv>=1.0.0
streamlit>=1.30.0
```

### 3.5 `.env.example`

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=health_insurance
DB_USER=your_username
DB_PASSWORD=your_password
DB_URL=postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}

# Optional: Streamlit Secrets (for cloud deployment)
# STREAMLIT_DB_URL=postgresql://user:pass@cloud-host:5432/health_insurance
```

---

## 4. Architecture — Medallion Pattern

### 4.1 What is the Medallion Architecture?

The **Medallion Architecture** (also called Multi-Hop Architecture) is a data design pattern that organizes data into layers of increasing quality and business value. Each layer has a distinct purpose:

| Layer | Metaphor | Data State | Audience |
|-------|----------|------------|----------|
| 🥉 **Bronze** | Raw ore | As-is from source, immutable | Data Engineers (debugging, auditing) |
| 🥈 **Silver** | Refined metal | Cleaned, typed, deduplicated, conformed | Analytics Engineers, Data Analysts |
| 🥇 **Gold** | Pure gold | Aggregated, enriched, business-ready | Business Users, Dashboard, Reports |

### 4.2 End-to-End Data Flow

```mermaid
flowchart TB
    subgraph SOURCE ["📁 DATA SOURCE"]
        CSV["Public CSV File<br/>(Kaggle Health Insurance Claims)"]
    end

    subgraph BRONZE ["🥉 BRONZE LAYER — Raw, Immutable"]
        direction TB
        B1["bronze.raw_claims"]
        B_RULE["Rules:<br/>• Write-once (append-only)<br/>• Never modify source data<br/>• All columns stored as TEXT<br/>• ingested_at timestamp added"]
    end

    subgraph SILVER ["🥈 SILVER LAYER — Cleaned, Typed, Deduplicated"]
        direction TB
        S1["silver.stg_claims"]
        S2["silver.dim_patients"]
        S3["silver.dim_providers"]
        S_RULE["Rules:<br/>• Single source of truth for cleaning<br/>• Proper data types enforced<br/>• Duplicates removed<br/>• Null handling applied"]
    end

    subgraph GOLD ["🥇 GOLD LAYER — Business-Ready, Aggregated"]
        direction TB
        G1["gold.fct_claims"]
        G2["gold.agg_provider"]
        G3["gold.fraud_flags (optional)"]
        G_RULE["Rules:<br/>• Only layer queried by dashboard<br/>• Pre-aggregated for performance<br/>• Window functions for rankings<br/>• Business logic applied"]
    end

    subgraph DASHBOARD ["📊 STREAMLIT DASHBOARD"]
        D1["KPI Cards"]
        D2["Line Charts"]
        D3["Bar Charts"]
        D4["Data Tables"]
    end

    CSV -->|"python src/ingest.py<br/>(pandas + sqlalchemy)"| B1
    B1 -->|"python src/transform_silver.py<br/>(clean, cast, dedup)"| S1
    S1 --> S2
    S1 --> S3
    S1 -->|"python src/transform_gold.py<br/>(SQL aggregations)"| G1
    S2 --> G1
    S3 --> G2
    G1 --> G3
    G1 -->|"SQL via SQLAlchemy<br/>(@st.cache_data)"| D1
    G1 --> D2
    G1 --> D3
    G2 --> D4

    style BRONZE fill:#8B4513,color:#fff,stroke:#cd7f32,stroke-width:3px
    style SILVER fill:#708090,color:#fff,stroke:#c0c0c0,stroke-width:3px
    style GOLD fill:#B8860B,color:#fff,stroke:#ffd700,stroke-width:3px
    style DASHBOARD fill:#1a1a2e,color:#fff,stroke:#e94560,stroke-width:3px
```

### 4.3 Layer Contracts

Each layer has strict rules that must never be violated:

#### 🥉 Bronze Contract

| Rule | Description |
|------|-------------|
| **Immutability** | Data is write-once, append-only. Never update or delete rows. |
| **Fidelity** | Store exactly what the source provides — no cleaning, no casting. |
| **All TEXT** | Every column is stored as `TEXT` to prevent ingestion failures from type mismatches. |
| **Audit Trail** | Every row gets an `ingested_at` timestamp automatically. |
| **Schema** | Lives in the `bronze` PostgreSQL schema. |

#### 🥈 Silver Contract

| Rule | Description |
|------|-------------|
| **Single Source of Truth** | All cleaning logic lives here — not in Bronze, not in Gold. |
| **Typed** | Columns cast to proper types: `DATE`, `NUMERIC`, `INT`, etc. |
| **Deduplicated** | `claim_id` is unique. Duplicate rows are removed. |
| **Conformed** | Dimension tables (patients, providers) are normalized. |
| **Schema** | Lives in the `silver` PostgreSQL schema. |

#### 🥇 Gold Contract

| Rule | Description |
|------|-------------|
| **Business-Ready** | Every table is designed for a specific business question. |
| **Pre-Aggregated** | Aggregations computed here, not in the dashboard. |
| **Dashboard-Only Source** | The dashboard queries ONLY Gold tables. |
| **Enriched** | Fact tables joined with dimensions; derived columns added. |
| **Schema** | Lives in the `gold` PostgreSQL schema. |

### 4.4 Pipeline Orchestration Flow

```mermaid
sequenceDiagram
    participant User
    participant Pipeline as pipeline.py
    participant Ingest as ingest.py
    participant Silver as transform_silver.py
    participant Gold as transform_gold.py
    participant QC as quality_checks.py
    participant DB as PostgreSQL

    User->>Pipeline: python src/pipeline.py
    
    Note over Pipeline: Step 1: Bronze Ingestion
    Pipeline->>Ingest: load_raw_claims()
    Ingest->>Ingest: Read CSV with pandas
    Ingest->>DB: INSERT INTO bronze.raw_claims
    DB-->>Ingest: ✅ Rows loaded
    Ingest-->>Pipeline: ✅ Bronze complete

    Note over Pipeline: Step 2: Silver Transformation
    Pipeline->>Silver: transform_to_silver()
    Silver->>DB: SELECT FROM bronze.raw_claims
    Silver->>Silver: Clean dates, cast amounts, dedup
    Silver->>DB: INSERT INTO silver.stg_claims
    Silver->>DB: INSERT INTO silver.dim_patients
    Silver->>DB: INSERT INTO silver.dim_providers
    DB-->>Silver: ✅ Tables loaded
    Silver-->>Pipeline: ✅ Silver complete

    Note over Pipeline: Step 3: Gold Transformation
    Pipeline->>Gold: transform_to_gold()
    Gold->>DB: JOIN silver tables → fct_claims
    Gold->>DB: Aggregate → agg_provider
    Gold->>DB: (Optional) Anomaly → fraud_flags
    DB-->>Gold: ✅ Tables loaded
    Gold-->>Pipeline: ✅ Gold complete

    Note over Pipeline: Step 4: Quality Checks
    Pipeline->>QC: run_all_checks()
    QC->>DB: Validate nulls, uniqueness, integrity
    alt All checks pass
        QC-->>Pipeline: ✅ All quality checks passed
        Pipeline-->>User: ✅ Pipeline complete
    else Any check fails
        QC-->>Pipeline: ❌ Quality check failed
        Pipeline-->>User: ❌ Pipeline halted — fix data issues
    end
```

---

## 5. Schema Modeling — Full DDL

### 5.1 Schema Creation

```sql
-- 00_create_schemas.sql
-- Run this ONCE to set up the three Medallion schemas

CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;

-- Grant usage to the application role (adjust as needed)
-- GRANT USAGE ON SCHEMA bronze, silver, gold TO app_user;
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA bronze, silver, gold TO app_user;
```

### 5.2 🥉 Bronze Tables

```sql
-- 01_bronze_tables.sql

DROP TABLE IF EXISTS bronze.raw_claims;

CREATE TABLE bronze.raw_claims (
    claim_id        TEXT,           -- kept as TEXT (raw, no validation)
    patient_id      TEXT,
    provider_id     TEXT,
    diagnosis_code  TEXT,
    procedure_code  TEXT,
    claim_date      TEXT,           -- raw date string, not parsed
    claim_amount    TEXT,           -- raw amount string, not cast
    patient_age     TEXT,
    patient_gender  TEXT,
    region          TEXT,
    ingested_at     TIMESTAMP DEFAULT NOW()  -- audit column
);

-- Index for debugging lookups (optional)
CREATE INDEX IF NOT EXISTS idx_bronze_claims_ingested 
    ON bronze.raw_claims (ingested_at);

COMMENT ON TABLE bronze.raw_claims IS 
    'Raw claims data loaded exactly as received from the CSV source. No cleaning applied.';
```

> [!TIP]
> **Why all TEXT?** Storing everything as TEXT in Bronze prevents ingestion failures from unexpected data formats (e.g., dates like "2024/01/15" vs "01-15-2024", amounts with commas or currency symbols). Cleaning happens in Silver.

### 5.3 🥈 Silver Tables

```sql
-- 02_silver_tables.sql

-- Staging Claims (cleaned, typed, deduplicated)
DROP TABLE IF EXISTS silver.stg_claims;

CREATE TABLE silver.stg_claims (
    claim_id        TEXT PRIMARY KEY,
    patient_id      TEXT NOT NULL,
    provider_id     TEXT NOT NULL,
    diagnosis_code  TEXT,
    procedure_code  TEXT,
    claim_date      DATE NOT NULL,
    claim_amount    NUMERIC(12, 2) NOT NULL CHECK (claim_amount > 0),
    region          TEXT,
    loaded_at       TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE silver.stg_claims IS 
    'Cleaned and deduplicated claims. Dates parsed, amounts cast, nulls handled.';


-- Patient Dimension
DROP TABLE IF EXISTS silver.dim_patients;

CREATE TABLE silver.dim_patients (
    patient_id      TEXT PRIMARY KEY,
    age             INT CHECK (age BETWEEN 0 AND 120),
    age_band        TEXT,           -- '18-34', '35-54', '55+'
    gender          TEXT,
    region          TEXT
);

COMMENT ON TABLE silver.dim_patients IS 
    'One row per unique patient with derived age_band.';
COMMENT ON COLUMN silver.dim_patients.age_band IS 
    'Derived: 0-17, 18-34, 35-54, 55+';


-- Provider Dimension
DROP TABLE IF EXISTS silver.dim_providers;

CREATE TABLE silver.dim_providers (
    provider_id     TEXT PRIMARY KEY,
    provider_name   TEXT,
    specialty       TEXT,
    region          TEXT
);

COMMENT ON TABLE silver.dim_providers IS 
    'One row per unique provider with specialty and region.';
```

### 5.4 🥇 Gold Tables

```sql
-- 03_gold_tables.sql

-- Fact Claims (one row per claim, enriched with dimensions)
DROP TABLE IF EXISTS gold.fct_claims;

CREATE TABLE gold.fct_claims (
    claim_id        TEXT PRIMARY KEY,
    patient_id      TEXT NOT NULL,
    provider_id     TEXT NOT NULL,
    claim_date      DATE NOT NULL,
    claim_month     DATE NOT NULL,           -- DATE_TRUNC('month', claim_date)
    claim_amount    NUMERIC(12, 2) NOT NULL,
    diagnosis_code  TEXT,
    age_band        TEXT,
    region          TEXT
);

CREATE INDEX IF NOT EXISTS idx_gold_fct_claims_month 
    ON gold.fct_claims (claim_month);
CREATE INDEX IF NOT EXISTS idx_gold_fct_claims_region 
    ON gold.fct_claims (region);

COMMENT ON TABLE gold.fct_claims IS 
    'Enriched fact table: one row per claim with dimension attributes denormalized.';


-- Provider Aggregation (one row per provider)
DROP TABLE IF EXISTS gold.agg_provider;

CREATE TABLE gold.agg_provider (
    provider_id         TEXT PRIMARY KEY,
    provider_name       TEXT,
    specialty           TEXT,
    total_claims        INT NOT NULL,
    total_claim_amount  NUMERIC(14, 2) NOT NULL,
    avg_claim_amount    NUMERIC(12, 2) NOT NULL,
    rank_by_cost        INT NOT NULL           -- RANK() OVER (ORDER BY total_claim_amount DESC)
);

COMMENT ON TABLE gold.agg_provider IS 
    'Pre-aggregated provider metrics with cost ranking via window function.';


-- Fraud Flags (optional, ML-driven)
DROP TABLE IF EXISTS gold.fraud_flags;

CREATE TABLE gold.fraud_flags (
    claim_id        TEXT PRIMARY KEY,
    anomaly_score   NUMERIC(6, 4),
    is_flagged      BOOLEAN DEFAULT FALSE
);

COMMENT ON TABLE gold.fraud_flags IS 
    'Optional: Isolation Forest anomaly scores. is_flagged = TRUE when score > threshold.';
```

### 5.5 Entity Relationship Diagram

```mermaid
erDiagram
    BRONZE_RAW_CLAIMS {
        TEXT claim_id
        TEXT patient_id
        TEXT provider_id
        TEXT diagnosis_code
        TEXT procedure_code
        TEXT claim_date
        TEXT claim_amount
        TEXT patient_age
        TEXT patient_gender
        TEXT region
        TIMESTAMP ingested_at
    }

    SILVER_STG_CLAIMS {
        TEXT claim_id PK
        TEXT patient_id FK
        TEXT provider_id FK
        TEXT diagnosis_code
        TEXT procedure_code
        DATE claim_date
        NUMERIC claim_amount
        TEXT region
        TIMESTAMP loaded_at
    }

    SILVER_DIM_PATIENTS {
        TEXT patient_id PK
        INT age
        TEXT age_band
        TEXT gender
        TEXT region
    }

    SILVER_DIM_PROVIDERS {
        TEXT provider_id PK
        TEXT provider_name
        TEXT specialty
        TEXT region
    }

    GOLD_FCT_CLAIMS {
        TEXT claim_id PK
        TEXT patient_id FK
        TEXT provider_id FK
        DATE claim_date
        DATE claim_month
        NUMERIC claim_amount
        TEXT diagnosis_code
        TEXT age_band
        TEXT region
    }

    GOLD_AGG_PROVIDER {
        TEXT provider_id PK
        TEXT provider_name
        TEXT specialty
        INT total_claims
        NUMERIC total_claim_amount
        NUMERIC avg_claim_amount
        INT rank_by_cost
    }

    GOLD_FRAUD_FLAGS {
        TEXT claim_id PK
        NUMERIC anomaly_score
        BOOLEAN is_flagged
    }

    BRONZE_RAW_CLAIMS ||--o{ SILVER_STG_CLAIMS : "cleaned into"
    SILVER_STG_CLAIMS }o--|| SILVER_DIM_PATIENTS : "patient_id"
    SILVER_STG_CLAIMS }o--|| SILVER_DIM_PROVIDERS : "provider_id"
    SILVER_STG_CLAIMS ||--o{ GOLD_FCT_CLAIMS : "enriched into"
    SILVER_DIM_PROVIDERS ||--o{ GOLD_AGG_PROVIDER : "aggregated into"
    GOLD_FCT_CLAIMS ||--o| GOLD_FRAUD_FLAGS : "scored"
```

---

## 6. Feature Roadmap & Prioritization

### 6.1 MoSCoW Prioritization

Features are categorized using the **MoSCoW method**:
- 🔴 **Must** — Required for MVP. Project fails without these.
- 🟡 **Should** — Important but not blocking. Add if time permits within the sprint.
- 🟢 **Nice** — Stretch goals. Only after all Must + Should features are done.

### 6.2 Feature Backlog

| ID | Feature | Layer | Owner | Priority | Sprint |
|----|---------|-------|-------|----------|--------|
| **F1** | Raw claims CSV ingestion into `bronze.raw_claims` | Bronze | Person A | 🔴 Must | Week 1 |
| **F2** | Claims cleaning, type casting & deduplication → `silver.stg_claims` | Silver | Person B | 🔴 Must | Week 1 |
| **F3** | Patient dimension with age bands → `silver.dim_patients` | Silver | Person B | 🔴 Must | Week 1 |
| **F4** | Provider dimension → `silver.dim_providers` | Silver | Person A | 🔴 Must | Week 1 |
| **F5** | Enriched claims fact table → `gold.fct_claims` | Gold | Person B | 🔴 Must | Week 2 |
| **F6** | Provider aggregation with cost ranking → `gold.agg_provider` | Gold | Person B | 🔴 Must | Week 2 |
| **F7** | KPI cards (Total Claims, Total Cost, Avg Cost, High-Risk Providers) | Dashboard | Person A | 🔴 Must | Week 3 |
| **F8** | Claims over time — line chart by `claim_month` | Dashboard | Person A | 🔴 Must | Week 3 |
| **F9** | Claims by region — horizontal bar chart | Dashboard | Person B | 🔴 Must | Week 3 |
| **F10** | Top 10 providers by cost — sortable table + bar chart | Dashboard | Person B | 🔴 Must | Week 3 |
| **F11** | Global sidebar filters (date range, region, age band) | Dashboard | Both | 🔴 Must | Week 3 |
| **F12** | Fraud/anomaly flags via Isolation Forest → `gold.fraud_flags` | Gold | Person A | 🟢 Nice | Week 3 |
| **F13** | Diagnosis distribution — pie/donut chart (top 8 codes) | Dashboard | Person B | 🟢 Nice | Week 3 |
| **F14** | Data quality test suite via `pytest` | Pipeline | Person A | 🟡 Should | Week 2 |
| **F15** | Scheduled pipeline execution (cron / Task Scheduler) | Ops | Person A | 🟢 Nice | Week 4 |

### 6.3 Feature Dependency Graph

```mermaid
graph LR
    F1["F1: Bronze Ingestion"] --> F2["F2: Silver Claims"]
    F1 --> F4["F4: Dim Providers"]
    F2 --> F3["F3: Dim Patients"]
    F2 --> F5["F5: Gold Fact Claims"]
    F4 --> F6["F6: Gold Agg Provider"]
    F3 --> F5
    F5 --> F7["F7: KPI Cards"]
    F5 --> F8["F8: Line Chart"]
    F5 --> F9["F9: Bar Chart"]
    F6 --> F10["F10: Top Providers"]
    F7 --> F11["F11: Sidebar Filters"]
    F8 --> F11
    F9 --> F11
    F10 --> F11
    F5 --> F12["F12: Fraud Flags"]
    F5 --> F13["F13: Diagnosis Pie"]
    F2 --> F14["F14: pytest Suite"]

    style F1 fill:#cd7f32,color:#fff
    style F2 fill:#c0c0c0,color:#000
    style F3 fill:#c0c0c0,color:#000
    style F4 fill:#c0c0c0,color:#000
    style F5 fill:#ffd700,color:#000
    style F6 fill:#ffd700,color:#000
    style F7 fill:#e94560,color:#fff
    style F8 fill:#e94560,color:#fff
    style F9 fill:#e94560,color:#fff
    style F10 fill:#e94560,color:#fff
    style F11 fill:#e94560,color:#fff
    style F12 fill:#2ecc71,color:#fff
    style F13 fill:#2ecc71,color:#fff
    style F14 fill:#f39c12,color:#000
```

---

## 7. Repository Structure

```
health-insurance-de-project/
│
├── .github/
│   └── workflows/
│       └── ci.yml                    # (Optional) Lint + test on PR
│
├── data/
│   ├── raw/                          # Downloaded CSV files (⚠️ GITIGNORED)
│   │   └── .gitkeep                  # Ensures directory exists in git
│   └── sample/                       # Small sample for testing (committed)
│       └── sample_claims_100.csv
│
├── sql/
│   ├── 00_create_schemas.sql         # CREATE SCHEMA bronze, silver, gold
│   ├── 01_bronze_tables.sql          # Bronze DDL
│   ├── 02_silver_tables.sql          # Silver DDL (stg_claims, dim_patients, dim_providers)
│   ├── 03_gold_tables.sql            # Gold DDL (fct_claims, agg_provider, fraud_flags)
│   └── 04_dashboard_queries.sql      # All queries used by the Streamlit app
│
├── src/
│   ├── __init__.py                   # Makes src a Python package
│   ├── config.py                     # Loads .env, exports DB_URL and settings
│   ├── db.py                         # SQLAlchemy engine factory, connection helper
│   ├── ingest.py                     # Bronze loader: CSV → bronze.raw_claims
│   ├── transform_silver.py           # Bronze → Silver (clean, cast, dedup, dimensions)
│   ├── transform_gold.py             # Silver → Gold (fct_claims, agg_provider)
│   ├── quality_checks.py             # Data quality assertions (runs after each layer)
│   └── pipeline.py                   # Orchestrator: calls ingest → silver → gold → checks
│
├── dashboard/
│   └── app.py                        # Streamlit application (queries Gold layer only)
│
├── tests/
│   ├── conftest.py                   # pytest fixtures (DB connection, test data)
│   ├── test_ingest.py                # Tests for Bronze ingestion
│   └── test_transforms.py            # Tests for Silver/Gold transformations
│
├── docs/
│   ├── architecture.md               # Architecture overview with diagrams
│   ├── data_dictionary.md            # Every column: name, type, description, source
│   └── screenshots/                  # Dashboard screenshots for README
│       ├── dashboard_overview.png
│       └── kpi_cards.png
│
├── .env.example                      # Template for environment variables
├── .gitignore                        # Ignore: .env, data/raw/, __pycache__/, venv/
├── requirements.txt                  # Python dependencies
├── README.md                         # Setup instructions, architecture, screenshots
└── PROJECT_PLAN.md                   # This file
```

### Key Principles

- **`data/raw/`** is gitignored — raw CSV files never enter version control
- **`data/sample/`** contains a small (100-row) sample for testing and CI
- **`sql/`** files are numbered for execution order
- **`src/`** is a Python package — all imports are relative to `src`
- **`dashboard/`** is isolated — it only imports from `src.db` and queries Gold
- **`docs/`** is always up-to-date — documentation is a deliverable, not an afterthought

---

## 8. GitHub Setup & Workflow

### 8.1 Day 1 Setup Checklist

| Step | Action | Owner |
|------|--------|-------|
| 1 | Create GitHub repository `health-insurance-de-project` (private) | Person A |
| 2 | Add Person B as collaborator with **Write** access | Person A |
| 3 | Enable **branch protection** on `main`: require PR + 1 approval | Person A |
| 4 | Create **GitHub Project** (Kanban board) | Person B |
| 5 | Set up board columns: `Backlog` → `In Progress` → `In Review` → `Done` | Person B |
| 6 | Create **labels**: `bronze`, `silver`, `gold`, `dashboard`, `bug`, `docs`, `infra` | Person B |
| 7 | Commit initial files: `.gitignore`, `.env.example`, `requirements.txt`, `README.md` | Person A |
| 8 | Create all Week 1 issues from the Feature Roadmap | Person B |

### 8.2 `.gitignore`

```gitignore
# Environment
.env
venv/
.venv/

# Data (never commit raw data)
data/raw/*.csv
data/raw/*.zip

# Python
__pycache__/
*.pyc
*.pyo
*.egg-info/
dist/
build/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Streamlit
.streamlit/secrets.toml
```

### 8.3 Branching Strategy

```mermaid
gitgraph
    commit id: "initial commit"
    branch feat/bronze-ingest
    commit id: "feat: add ingest.py"
    commit id: "feat: add bronze DDL"
    checkout main
    merge feat/bronze-ingest id: "PR #1 merged"
    branch feat/silver-claims
    commit id: "feat: add stg_claims transform"
    commit id: "feat: add dim_patients"
    checkout main
    branch feat/silver-providers
    commit id: "feat: add dim_providers"
    checkout main
    merge feat/silver-providers id: "PR #2 merged"
    merge feat/silver-claims id: "PR #3 merged"
    branch feat/gold-facts
    commit id: "feat: add fct_claims"
    commit id: "feat: add agg_provider"
    checkout main
    merge feat/gold-facts id: "PR #4 merged"
    branch feat/dashboard-v1
    commit id: "feat: streamlit skeleton"
    commit id: "feat: KPI cards + charts"
    checkout main
    merge feat/dashboard-v1 id: "PR #5 merged"
    commit id: "tag: v1.0.0" type: HIGHLIGHT
```

### 8.4 Branch Naming Convention

| Prefix | Use Case | Example |
|--------|----------|---------|
| `feat/` | New feature | `feat/bronze-ingest`, `feat/dashboard-filters` |
| `fix/` | Bug fix | `fix/null-claim-amounts`, `fix/date-parsing` |
| `docs/` | Documentation only | `docs/architecture-diagram`, `docs/readme-update` |
| `refactor/` | Code restructure (no behavior change) | `refactor/config-module` |
| `test/` | Adding or fixing tests | `test/quality-checks` |

### 8.5 Commit Message Convention

Follow **Conventional Commits** format:

```
<type>(<scope>): <description>

[optional body]
[optional footer]
```

**Examples:**
```
feat(bronze): add raw claims ingestion from CSV
fix(silver): handle null claim_amount in stg_claims transform
docs(readme): add architecture diagram and setup instructions
test(quality): add referential integrity check for fct_claims
refactor(db): extract engine creation into factory function
```

### 8.6 Issue Template

```markdown
## 📋 Task
<Short description of what needs to be done>

## 🏷️ Layer
Bronze / Silver / Gold / Dashboard / Pipeline / Docs

## ✅ Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## 👤 Owner
@person-a / @person-b

## 📅 Target Day
Day X (Week Y)

## 🔗 Dependencies
- Depends on #<issue-number>
```

### 8.7 PR Review Checklist

When reviewing a PR, verify:
- [ ] Code runs without errors
- [ ] SQL follows naming conventions (`snake_case`, schema-qualified)
- [ ] Python follows PEP 8 (or passes `ruff` if set up)
- [ ] New tables have `COMMENT ON TABLE` and `COMMENT ON COLUMN`
- [ ] Quality checks cover the new data
- [ ] README or docs updated if user-facing behavior changed

---

## 9. Day-by-Day Execution Plan (20 Working Days)

### 🗓️ Week 1 — Foundations, Setup & Bronze Layer

```mermaid
gantt
    title Week 1 — Foundations & Bronze
    dateFormat  YYYY-MM-DD
    axisFormat  %a

    section Person A
    GitHub repo + env setup           :a1, 2024-01-01, 1d
    Download CSV + config.py + db.py  :a2, after a1, 1d
    Write ingest.py (Bronze loader)   :a3, after a2, 1d
    Draft transform_silver.py         :a4, after a3, 1d
    Finish Silver stg_claims load     :a5, after a4, 1d

    section Person B
    GitHub board + issues + labels    :b1, 2024-01-01, 1d
    PostgreSQL + schemas + bronze DDL :b2, after b1, 1d
    Profiling queries + silver DDL    :b3, after b2, 1d
    dim_patients + dim_providers SQL  :b4, after b3, 1d
    Merge Bronze + Silver PRs         :b5, after b4, 1d

    section Checkpoints
    Schema agreement                  :milestone, m1, 2024-01-01, 0d
    Bronze loaded                     :milestone, m2, 2024-01-03, 0d
    Week 1 review                     :milestone, m3, 2024-01-05, 0d
```

| Day | Person A (Data Engineer) | Person B (Analytics Engineer) | Shared / Checkpoint |
|-----|-------------------------|-------------------------------|---------------------|
| **1** | Create GitHub repo, `.gitignore`, `.env.example`, `requirements.txt`, set up Python `venv` | Create GitHub Project board (Kanban), create all Week 1 issues, add labels | ✅ **Agree on schema** (Section 5), commit `PROJECT_PLAN.md` to repo |
| **2** | Download public health insurance CSV to `data/raw/`. Write `src/config.py` (loads `.env`) and `src/db.py` (SQLAlchemy engine) | Install PostgreSQL, create database `health_insurance`, run `sql/00_create_schemas.sql` to create `bronze`/`silver`/`gold` schemas | ✅ **Profile raw CSV**: row count, column count, null percentages, sample values |
| **3** | Write `src/ingest.py` — load raw CSV → `bronze.raw_claims` using `pandas.to_sql()` via SQLAlchemy | Write `sql/01_bronze_tables.sql` (CREATE TABLE with all TEXT columns). Write profiling queries against `bronze.raw_claims` | ✅ **Run ingestion end-to-end**. Verify: row count in DB matches CSV row count |
| **4** | Draft `src/transform_silver.py` — parse dates (`pd.to_datetime`), cast amounts (`pd.to_numeric`), drop duplicates on `claim_id` | Write `sql/02_silver_tables.sql` for `stg_claims`, `dim_patients`, `dim_providers` with constraints and comments | ✅ **PR review**: Person A reviews SQL DDL, Person B reviews Python ingestion |
| **5** | Finish Silver transform for `stg_claims` and load into PostgreSQL | Write SQL logic to build `dim_patients` (derive `age_band`) and `dim_providers` | ✅ **Merge Bronze + Silver PRs** to `main`. Update board. |

> [!IMPORTANT]
> **Week 1 Checkpoint:** Bronze layer fully loaded. Silver `stg_claims` populated. `dim_patients` and `dim_providers` designed and partially loaded.

---

### 🗓️ Week 2 — Silver Completion & Gold Layer

```mermaid
gantt
    title Week 2 — Silver & Gold
    dateFormat  YYYY-MM-DD
    axisFormat  %a

    section Person A
    pipeline.py orchestrator          :a6, 2024-01-08, 1d
    transform_gold.py (fct_claims)    :a7, after a6, 1d
    quality_checks.py                 :a8, after a7, 1d
    docs/architecture.md + README     :a9, after a8, 1d
    Optional: cron scheduling         :a10, after a9, 1d

    section Person B
    Gold DDL (fct_claims)             :b6, 2024-01-08, 1d
    Window SQL (agg_provider)         :b7, after b6, 1d
    Quality checks for dims           :b8, after b7, 1d
    docs/data_dictionary.md           :b9, after b8, 1d
    Optional: anomaly notebook        :b10, after b9, 1d

    section Checkpoints
    Full pipeline works               :milestone, m4, 2024-01-08, 0d
    Gold merged                       :milestone, m5, 2024-01-10, 0d
    Week 2 review                     :milestone, m6, 2024-01-12, 0d
```

| Day | Person A | Person B | Shared / Checkpoint |
|-----|----------|----------|---------------------|
| **6** | Write `src/pipeline.py` — orchestrate: `ingest → silver → gold → quality_checks` in one command | Write `sql/03_gold_tables.sql` for `fct_claims` (DDL + INSERT query with JOINs) | ✅ Run `python src/pipeline.py` — full Bronze → Silver works end-to-end |
| **7** | Implement Gold logic in `src/transform_gold.py` to build `fct_claims` | Write window-function SQL for `gold.agg_provider` (`RANK() OVER (ORDER BY total_claim_amount DESC)`) | ✅ **PR review**: both Gold scripts |
| **8** | Write `src/quality_checks.py` — assertions for non-null IDs, positive amounts, unique `claim_id` | Add quality checks for dimension tables: valid `age_band` values, no orphan `patient_id`s | ✅ **Merge Gold layer** to `main`. Update board |
| **9** | Write `docs/architecture.md` with diagrams. Update `README.md` with setup instructions | Write `docs/data_dictionary.md` — every column, type, description, source table | ✅ **Full pipeline** runs end-to-end in < 5 minutes |
| **10** | *(Optional)* Set up cron / Task Scheduler to run `pipeline.py` daily | *(Optional)* Start `scikit-learn` anomaly detection notebook | ✅ **Week 2 review**: all three Medallion layers populated |

> [!IMPORTANT]
> **Week 2 Checkpoint:** Bronze → Silver → Gold pipeline runs end-to-end with `python src/pipeline.py`. Data quality checks pass. Documentation exists.

---

### 🗓️ Week 3 — Analytics & Dashboard Build

```mermaid
gantt
    title Week 3 — Dashboard
    dateFormat  YYYY-MM-DD
    axisFormat  %a

    section Person A
    Optional: fraud_flags + queries   :a11, 2024-01-15, 1d
    Streamlit skeleton + DB conn      :a12, after a11, 1d
    KPI row (4 metric cards)          :a13, after a12, 1d
    Top 10 providers table/bar        :a14, after a13, 1d
    Empty states + polish             :a15, after a14, 1d

    section Person B
    Dashboard SQL queries             :b11, 2024-01-15, 1d
    Sidebar filters (date, region)    :b12, after b11, 1d
    Line chart + bar chart            :b13, after b12, 1d
    Recent claims + diagnosis pie     :b14, after b13, 1d
    Cache tuning + performance        :b15, after b14, 1d

    section Checkpoints
    Dashboard layout agreed           :milestone, m7, 2024-01-15, 0d
    First page loads                  :milestone, m8, 2024-01-17, 0d
    Week 3 review                     :milestone, m9, 2024-01-19, 0d
```

| Day | Person A | Person B | Shared / Checkpoint |
|-----|----------|----------|---------------------|
| **11** | *(Optional)* Add `gold.fraud_flags` via Isolation Forest. Write `sql/04_dashboard_queries.sql` | Write all dashboard SQL queries: KPI aggregations, region grouping, provider top-10, time series | ✅ **Agree on exact dashboard layout** (see Section 11) |
| **12** | Streamlit skeleton: `dashboard/app.py`, DB connection via `@st.cache_data`, page config | Streamlit layout: sidebar with date range picker + region multiselect + age band multiselect | ✅ **First dashboard page loads** locally without errors |
| **13** | Build KPI row — 4 `st.metric` cards driven by filtered Gold query | Build line chart (claims over time by `claim_month`) + bar chart (claims by region) | ✅ Filters update KPIs + charts correctly |
| **14** | Build "Top 10 Providers by Cost" — sortable `st.dataframe` + horizontal bar chart | Build "Recent High-Cost Claims" table + diagnosis distribution pie/donut chart | ✅ All 3+ charts working and responsive |
| **15** | Handle empty states ("No data for selected filters" message), add titles and descriptions | Add `@st.cache_data(ttl=600)` to all queries; tune query performance with `EXPLAIN ANALYZE` | ✅ **Week 3 review**: Dashboard functional locally |

> [!IMPORTANT]
> **Week 3 Checkpoint:** Dashboard runs locally with KPIs, charts, and working filters. All queries hit Gold layer only.

---

### 🗓️ Week 4 — Polish, Deploy & Demo

```mermaid
gantt
    title Week 4 — Ship It!
    dateFormat  YYYY-MM-DD
    axisFormat  %a

    section Person A
    Dashboard polish + formatting     :a16, 2024-01-22, 1d
    Deployment prep                   :a17, after a16, 1d
    Deploy to Streamlit Cloud         :a18, after a17, 1d
    Record demo walkthrough           :a19, after a18, 1d
    Buffer + tag v1.0.0               :a20, after a19, 1d

    section Person B
    README + screenshots              :b16, 2024-01-22, 1d
    Final code review                 :b17, after b16, 1d
    Data dictionary final pass        :b18, after b17, 1d
    Demo talking points               :b19, after b18, 1d
    Retrospective + stretch list      :b20, after b19, 1d

    section Checkpoints
    Screenshots in repo               :milestone, m10, 2024-01-22, 0d
    Deployed                          :milestone, m11, 2024-01-24, 0d
    Demo delivered                    :milestone, m12, 2024-01-26, 0d
```

| Day | Person A | Person B | Shared / Checkpoint |
|-----|----------|----------|---------------------|
| **16** | Dashboard polish: consistent color scheme, number formatting (`$1,234.56`), layout spacing, responsive design | Update `README.md` with dashboard screenshots. Capture screenshots to `docs/screenshots/` | ✅ Screenshots committed to repo |
| **17** | Deployment prep: finalize `requirements.txt`, configure `st.secrets` for DB credentials | Final code review: verify all PRs merged, `main` is clean, no orphan branches | ✅ All branches merged to `main` |
| **18** | Deploy dashboard to **Streamlit Community Cloud** (or local + ngrok tunnel) | Write `docs/data_dictionary.md` final pass. Add demo script/outline | ✅ **Public (or shareable) dashboard URL** working |
| **19** | Record 5-minute demo walkthrough: architecture → code walkthrough → live dashboard | Prepare demo talking points. Finalize `README.md` with deployment URL | ✅ **Dry-run presentation** |
| **20** | **Buffer**: fix last-minute bugs, create git tag `v1.0.0` | **Buffer**: write retrospective notes, list stretch goals for future sprints | ✅ **Final demo + retrospective** |

> [!IMPORTANT]
> **Week 4 Checkpoint:** Dashboard deployed (or demo-ready locally). Repository tagged `v1.0.0`. 5-minute demo delivered.

---

## 10. Data Quality & Testing

### 10.1 Quality Check Framework

All checks are implemented in `src/quality_checks.py` and run automatically at the end of `pipeline.py`.

```mermaid
flowchart TD
    A[Pipeline Step Completes] --> B{Run Quality Checks}
    B --> C[Non-null Keys]
    B --> D[Unique Claims]
    B --> E[Positive Amounts]
    B --> F[Valid Dates]
    B --> G[Referential Integrity]
    B --> H[Aggregation Sanity]
    
    C --> I{All Pass?}
    D --> I
    E --> I
    F --> I
    G --> I
    H --> I
    
    I -->|Yes| J[✅ Pipeline Complete<br/>Log success]
    I -->|No| K[❌ Pipeline HALTED<br/>Log failures & row counts<br/>Raise exception]

    style J fill:#2ecc71,color:#fff
    style K fill:#e74c3c,color:#fff
```

### 10.2 Quality Rules

| # | Check | Layer | SQL/Python Logic | Failure Action |
|---|-------|-------|-----------------|----------------|
| QC-1 | **Non-null keys** | Bronze | `WHERE claim_id IS NULL OR patient_id IS NULL OR provider_id IS NULL` → count must be 0 | HALT pipeline, log failing rows |
| QC-2 | **Unique claims** | Silver | `COUNT(claim_id) = COUNT(DISTINCT claim_id)` in `stg_claims` | HALT pipeline, log duplicate `claim_id`s |
| QC-3 | **Positive amounts** | Silver | `WHERE claim_amount <= 0` → count must be 0 | HALT pipeline, log negative/zero amounts |
| QC-4 | **Valid dates** | Silver | `WHERE claim_date < '2010-01-01' OR claim_date > CURRENT_DATE` → count must be 0 | HALT pipeline, log out-of-range dates |
| QC-5 | **Referential integrity** | Gold | Every `patient_id` in `fct_claims` must exist in `dim_patients` | HALT pipeline, log orphan IDs |
| QC-6 | **Aggregation sanity** | Gold | `SUM(total_claim_amount)` in `agg_provider` ≈ `SUM(claim_amount)` in `fct_claims` (within 0.01%) | WARNING (soft fail), log discrepancy |

### 10.3 Failure Behavior

> [!CAUTION]
> **Never load bad data downstream.** If any quality check fails, the pipeline halts immediately. The failing check logs:
> 1. Which check failed
> 2. How many rows violated the rule
> 3. Sample of failing rows (up to 10)
> 4. Timestamp of the failure
>
> The downstream layer is NOT populated until the issue is fixed and the pipeline re-runs successfully.

### 10.4 pytest Test Structure (Optional)

```python
# tests/test_ingest.py
def test_bronze_row_count_matches_csv(db_engine, sample_csv):
    """After ingestion, bronze.raw_claims row count should match CSV row count."""
    ...

def test_bronze_all_columns_are_text(db_engine):
    """Every column in bronze.raw_claims (except ingested_at) should be TEXT."""
    ...

# tests/test_transforms.py
def test_silver_no_duplicate_claims(db_engine):
    """silver.stg_claims should have no duplicate claim_ids."""
    ...

def test_silver_amounts_are_positive(db_engine):
    """All claim_amount values in silver.stg_claims should be > 0."""
    ...

def test_gold_referential_integrity(db_engine):
    """Every patient_id in gold.fct_claims should exist in silver.dim_patients."""
    ...

def test_gold_aggregation_sanity(db_engine):
    """Sum of agg_provider.total_claim_amount should match sum of fct_claims.claim_amount."""
    ...
```

---

## 11. Dashboard Specification

### 11.1 Dashboard Wireframe Layout

```mermaid
block-beta
    columns 4

    block:header:4
        title["🏥 Health Insurance Claims Dashboard"]
    end

    block:sidebar:1
        filters["🔍 FILTERS<br/>────────<br/>📅 Date Range<br/>[Start] → [End]<br/>────────<br/>🌍 Region<br/>[Multi-select]<br/>────────<br/>👤 Age Band<br/>[Multi-select]<br/>────────<br/>🔄 Reset"]
    end

    block:main:3
        block:kpis:3
            kpi1["📊 Total Claims<br/>42,857"]
            kpi2["💰 Total Cost<br/>$12.4M"]
            kpi3["📈 Avg Cost<br/>$289.45"]
        end
    end

    space:1
    block:charts:3
        chart1["📈 Claims Over Time<br/>(Line Chart)"]
        chart2["📊 Claims by Region<br/>(Bar Chart)"]
        chart3["🏆 Top 10 Providers<br/>(Table + Bar)"]
    end

    space:1
    block:bottom:3
        chart4["🔬 Diagnosis Distribution<br/>(Pie Chart — Top 8)"]
        chart5["⚠️ Recent High-Cost Claims<br/>(Data Table)"]
        chart6["🚩 Fraud Risk Summary<br/>(Optional)"]
    end
```

### 11.2 Component Specifications

#### KPI Cards (Row 1)

| Card | Label | Data Source | Format | Color Logic |
|------|-------|-------------|--------|-------------|
| KPI-1 | Total Claims | `SELECT COUNT(*) FROM gold.fct_claims WHERE <filters>` | `42,857` | Neutral |
| KPI-2 | Total Claim Amount | `SELECT SUM(claim_amount) FROM gold.fct_claims WHERE <filters>` | `$12,456,789` | Neutral |
| KPI-3 | Avg Claim Cost | `SELECT AVG(claim_amount) FROM gold.fct_claims WHERE <filters>` | `$289.45` | Neutral |
| KPI-4 | High-Risk Providers | `SELECT COUNT(*) FROM gold.agg_provider WHERE rank_by_cost <= 10` | `10` | 🔴 Red if > 5 |

#### Charts (Row 2–3)

| Chart | Type | X-Axis | Y-Axis | Data Source |
|-------|------|--------|--------|-------------|
| Claims Over Time | Line | `claim_month` | `COUNT(*)` | `gold.fct_claims GROUP BY claim_month` |
| Claims by Region | Horizontal Bar | `region` | `COUNT(*)` | `gold.fct_claims GROUP BY region` |
| Top 10 Providers | Table + Bar | `provider_name` | `total_claim_amount` | `gold.agg_provider ORDER BY total_claim_amount DESC LIMIT 10` |
| Diagnosis Distribution | Pie/Donut | `diagnosis_code` | `COUNT(*)` | `gold.fct_claims GROUP BY diagnosis_code` (top 8 + "Other") |
| Recent High-Cost Claims | `st.dataframe` | — | — | `gold.fct_claims ORDER BY claim_amount DESC LIMIT 20` |

### 11.3 Global Filters (Sidebar)

| Filter | Widget | Column Filtered | Default |
|--------|--------|-----------------|---------|
| Date Range | `st.date_input` (start + end) | `claim_date` | Full data range |
| Region | `st.multiselect` | `region` | All regions selected |
| Age Band | `st.multiselect` | `age_band` | All bands selected |

> [!WARNING]
> **All filters must update every chart and KPI on the page.** A single filtered query pattern is recommended to avoid inconsistencies.

### 11.4 UX Rules

1. Every chart has a **title** and **axis labels**
2. Empty filter results → show `"No data for the selected filters"` message (never crash)
3. All DB queries wrapped in `@st.cache_data(ttl=600)` (10-minute cache)
4. **No dashboard query touches Bronze or Silver directly** — Gold layer only
5. Numbers use proper formatting: `$1,234.56` for currency, `42,857` for counts
6. Color palette is consistent across all charts
7. Loading states use `st.spinner()` for long queries

---

## 12. Deployment Plan

### 12.1 Local Development (Days 1–17)

```bash
# 1. Clone the repository
git clone https://github.com/<org>/health-insurance-de-project.git
cd health-insurance-de-project

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate          # macOS/Linux
# venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your PostgreSQL credentials

# 5. Set up database schemas
psql -U your_user -d health_insurance -f sql/00_create_schemas.sql
psql -U your_user -d health_insurance -f sql/01_bronze_tables.sql
psql -U your_user -d health_insurance -f sql/02_silver_tables.sql
psql -U your_user -d health_insurance -f sql/03_gold_tables.sql

# 6. Run the full pipeline
python src/pipeline.py

# 7. Launch the dashboard
streamlit run dashboard/app.py
```

### 12.2 Cloud Deployment (Day 18)

```mermaid
flowchart LR
    A[GitHub Repo<br/>main branch] --> B[Streamlit<br/>Community Cloud]
    C[Cloud PostgreSQL<br/>Neon / Supabase] --> B
    
    subgraph "Setup Steps"
        D["1. Push code to main"]
        E["2. Create Neon/Supabase DB"]
        F["3. Run pipeline against cloud DB"]
        G["4. Connect repo to Streamlit Cloud"]
        H["5. Add DB creds to st.secrets"]
        I["6. Deploy dashboard/app.py"]
        J["7. Share public URL"]
    end

    D --> E --> F --> G --> H --> I --> J

    style B fill:#ff4b4b,color:#fff
    style C fill:#3ecf8e,color:#fff
```

#### Step-by-Step Cloud Deployment

| Step | Action | Details |
|------|--------|---------|
| 1 | **Push final code** | Ensure `main` is clean and all PRs merged |
| 2 | **Create cloud PostgreSQL** | Free tier on [Neon](https://neon.tech) or [Supabase](https://supabase.com). Copy connection string |
| 3 | **Run pipeline against cloud DB** | Update `.env` with cloud DB URL, run `python src/pipeline.py` |
| 4 | **Connect to Streamlit Cloud** | Go to [share.streamlit.io](https://share.streamlit.io), connect your GitHub repo |
| 5 | **Add secrets** | In Streamlit Cloud settings, add `DB_URL` to Secrets (TOML format) |
| 6 | **Deploy** | Set `dashboard/app.py` as the entry point. Click Deploy |
| 7 | **Share** | Copy the public URL, add it to `README.md` |

### 12.3 Fallback Plan

> [!TIP]
> If cloud deployment is blocked (time constraints, credit card requirement, etc.), the fallback is perfectly acceptable:
> - Run Streamlit locally: `streamlit run dashboard/app.py`
> - Screen-share during the demo
> - Document this decision in the README

---

## 13. Definition of Done

### 13.1 Task-Level "Done"

A task is **Done** when ALL of the following are true:

- [ ] Code is merged to `main` via a reviewed Pull Request
- [ ] The pipeline runs end-to-end without errors
- [ ] All relevant data quality checks pass
- [ ] Documentation in `README.md` or `docs/` is updated (if user-facing)
- [ ] GitHub Project card is moved to **Done** column

### 13.2 Project-Level "Done"

The project is **Done** when ALL of the following are true:

- [ ] All 11 **Must** features (F1–F11 in Section 6) are complete
- [ ] Dashboard is deployed to Streamlit Cloud (or demo-ready locally)
- [ ] `README.md` contains: setup instructions, architecture diagram, and dashboard screenshots
- [ ] `docs/architecture.md` and `docs/data_dictionary.md` are complete
- [ ] Git tag `v1.0.0` is created on `main`
- [ ] 5-minute demo is recorded or delivered live
- [ ] GitHub Project board is fully closed out (all cards in Done)

---

## 14. Risks & Mitigations

### 14.1 Risk Register

| # | Risk | Likelihood | Impact | Mitigation Strategy |
|---|------|-----------|--------|---------------------|
| R1 | **No suitable public dataset found** | 🟢 Low | 🔴 High | Pre-select 3 candidate Kaggle datasets on Day 1. Validate: ≥10K rows, has patient/provider/claim columns |
| R2 | **PostgreSQL setup issues** (permissions, version conflicts) | 🟡 Medium | 🟡 Medium | Person B owns DB setup. Fallback: use Docker (`docker run -e POSTGRES_PASSWORD=pass -p 5432:5432 postgres:15`) |
| R3 | **Dashboard filters slow / stale** | 🟡 Medium | 🟡 Medium | Use `@st.cache_data(ttl=600)`. Single filtered query pattern. Index `claim_month` and `region` columns |
| R4 | **Scope creep** (too many charts, features) | 🔴 High | 🟡 Medium | Hard cap: 4 KPIs + 3 charts for MVP. No "Nice" features until all "Must" are done |
| R5 | **Merge conflicts** on shared files | 🟡 Medium | 🟢 Low | Small PRs (< 200 lines), daily merges, branch protection enforced |
| R6 | **Team member unavailable** (sick, emergency) | 🟡 Medium | 🟡 Medium | Cross-review ensures both people understand both layers. Any task can be picked up by the other |
| R7 | **Cloud deployment blocked** (account issues, costs) | 🟢 Low | 🟢 Low | Fallback: local demo via screen-share. Documented in plan |
| R8 | **Data quality issues in source CSV** | 🟡 Medium | 🟡 Medium | Bronze layer stores raw data as-is. Silver cleaning handles: nulls, bad dates, negative amounts, duplicates |

### 14.2 Risk Heat Map

```mermaid
quadrantChart
    title Risk Heat Map
    x-axis Low Likelihood --> High Likelihood
    y-axis Low Impact --> High Impact
    quadrant-1 Monitor Closely
    quadrant-2 Mitigate Immediately
    quadrant-3 Accept
    quadrant-4 Watch & Plan
    R1 - No Dataset: [0.2, 0.85]
    R2 - DB Setup: [0.5, 0.5]
    R3 - Slow Filters: [0.5, 0.5]
    R4 - Scope Creep: [0.8, 0.5]
    R5 - Merge Conflicts: [0.5, 0.3]
    R6 - Unavailability: [0.5, 0.5]
    R7 - Deploy Blocked: [0.2, 0.2]
    R8 - Bad Source Data: [0.5, 0.5]
```

---

## 15. Stretch Goals (Post-MVP)

> [!NOTE]
> Only attempt these after **all 11 Must features** are complete and the MVP dashboard is deployed.

| # | Stretch Goal | Effort | Value | Description |
|---|-------------|--------|-------|-------------|
| S1 | **dbt Integration** | 🔴 High | 🔴 High | Migrate Silver/Gold SQL into dbt models with built-in tests, documentation, and lineage graphs |
| S2 | **Airflow Orchestration** | 🔴 High | 🟡 Medium | Replace cron with an Apache Airflow DAG for dependency-aware scheduling |
| S3 | **ML Fraud Detection** | 🟡 Medium | 🔴 High | Isolation Forest model with precision/recall metrics, visualized in dashboard |
| S4 | **CI/CD Pipeline** | 🟡 Medium | 🟡 Medium | GitHub Actions: lint (`ruff`, `sqlfluff`), run `pytest`, block merge on failure |
| S5 | **Auto Data Catalog** | 🟢 Low | 🟡 Medium | Generate data dictionary from DB metadata (`information_schema`) automatically |
| S6 | **Multi-Page Dashboard** | 🟡 Medium | 🟡 Medium | Add "Provider Deep-Dive" page with drill-down by individual provider |
| S7 | **Alerting** | 🟡 Medium | 🟢 Low | Email or Slack notification when a quality check fails |
| S8 | **Incremental Loading** | 🟡 Medium | 🔴 High | Load only new/changed rows instead of full refresh each run |

---

## 16. Final Deliverables Checklist

### Repository & Code

- [ ] GitHub repository with branch protection and clean `main`
- [ ] `PROJECT_PLAN.md` — this document
- [ ] `README.md` — setup instructions, architecture diagram, screenshots, deployment URL
- [ ] `requirements.txt` — all Python dependencies pinned
- [ ] `.env.example` — template for environment variables
- [ ] `.gitignore` — properly configured

### SQL

- [ ] `sql/00_create_schemas.sql` — schema creation
- [ ] `sql/01_bronze_tables.sql` — Bronze DDL
- [ ] `sql/02_silver_tables.sql` — Silver DDL (stg_claims, dim_patients, dim_providers)
- [ ] `sql/03_gold_tables.sql` — Gold DDL (fct_claims, agg_provider, fraud_flags)
- [ ] `sql/04_dashboard_queries.sql` — all dashboard queries

### Python

- [ ] `src/config.py` — configuration loader
- [ ] `src/db.py` — database connection
- [ ] `src/ingest.py` — Bronze ingestion
- [ ] `src/transform_silver.py` — Silver transformations
- [ ] `src/transform_gold.py` — Gold transformations
- [ ] `src/quality_checks.py` — data quality assertions
- [ ] `src/pipeline.py` — orchestrator

### Dashboard

- [ ] `dashboard/app.py` — Streamlit application (deployed or demo-ready)

### Documentation

- [ ] `docs/architecture.md` — architecture overview with diagrams
- [ ] `docs/data_dictionary.md` — every column documented
- [ ] `docs/screenshots/` — dashboard screenshots

### Project Management

- [ ] GitHub Project board fully closed out
- [ ] All issues closed, all PRs merged
- [ ] Git tag `v1.0.0` created on `main`
- [ ] 5-minute demo recording or live demo delivered

---

## 📊 Project Timeline Summary

```mermaid
timeline
    title Health Insurance DE Project — 4-Week Timeline
    
    section Week 1 - Foundations
        Day 1-2 : GitHub Setup
                 : Environment Config
                 : PostgreSQL + Schemas
        Day 3-4 : Bronze Ingestion
                 : Silver DDL
                 : CSV Profiling
        Day 5   : Silver Transform
                 : PR Reviews
                 : Week 1 Checkpoint ✅
    
    section Week 2 - Data Modeling
        Day 6-7 : Pipeline Orchestrator
                 : Gold Layer Build
                 : Window Functions
        Day 8-9 : Quality Checks
                 : Documentation
                 : Architecture Docs
        Day 10  : Full Pipeline Test
                 : Week 2 Checkpoint ✅
    
    section Week 3 - Dashboard
        Day 11-12 : Dashboard Queries
                   : Streamlit Skeleton
                   : Sidebar Filters
        Day 13-14 : KPI Cards
                   : Charts (Line, Bar, Pie)
                   : Provider Rankings
        Day 15    : Cache Tuning
                   : Empty States
                   : Week 3 Checkpoint ✅
    
    section Week 4 - Ship It!
        Day 16-17 : UI Polish
                   : Final Code Review
                   : Screenshots
        Day 18-19 : Cloud Deployment
                   : Demo Recording
                   : README Final
        Day 20    : Tag v1.0.0
                   : Retrospective
                   : 🚀 SHIPPED!
```

---

> **Ship it! 🚀**
>
> This plan is your roadmap. Follow it day by day, check off the boxes, and you'll have a production-grade data engineering project in your portfolio in 20 working days.

---

*Last updated: November 2026*
*Version: 1.0*
