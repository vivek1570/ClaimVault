# ClaimVault

Health insurance claims pipeline: Kaggle → Python → PostgreSQL (Bronze) → clean views → KPIs → Streamlit dashboard.

Data: Kaggle "Healthcare Provider Fraud Detection Analysis" (rohitrox). The `PotentialFraud` column is a dataset label, not a proven finding.

## Setup

1. Install Python 3.10+, PostgreSQL and Git.
2. Create the database: `CREATE DATABASE health_insurance;`
3. Copy `.env.example` to `.env` and set `DB_PASSWORD`.
4. Install packages: `pip install -r requirements.txt`

## Run order

```
python src/ingest.py                          # Bronze: downloads from Kaggle, loads 4 tables
psql -U postgres -d health_insurance -f sql/clean_views.sql
psql -U postgres -d health_insurance -f sql/ref_state.sql
python -m streamlit run app/dashboard.py      # dashboard at http://localhost:8501
```

## Daily updates (incremental loading)

Put new CSVs in `data/incoming/` (named `inpatient_*.csv` or `outpatient_*.csv`) and run:

```
python src/ingest_incremental.py
```

It inserts only new `ClaimID`s and records every file in `bronze.ingestion_log`, so re-running is safe. `src/make_daily_files.py` creates test files by splitting the Kaggle data.

## Layout

| Path | Purpose |
|---|---|
| `src/` | loaders and database connection |
| `sql/clean_views.sql` | cleaned views (`clean.claims`, `clean.patients`, `clean.providers`) |
| `sql/ref_state.sql` | state code lookup |
| `sql/kpis.sql` | 8 KPI queries |
| `app/dashboard.py` | Streamlit dashboard |
| `Docs/PROJECT_PLAN.md` | original project plan |

## Notes

- Bronze keeps raw text plus `ingested_at`, `source_file`, `batch_id`.
- `ingest.py` replaces Bronze tables, so drop the `clean` schema first (`DROP SCHEMA clean CASCADE;`) and rerun `clean_views.sql` afterwards.
- Claim dates run from Nov 2008 to Dec 2009.