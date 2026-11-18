import glob, os
import pandas as pd
from sqlalchemy import text
from db import get_engine

TABLES = {"inpatient": "raw_inpatient", "outpatient": "raw_outpatient"}
KEY = "ClaimID"

def main():
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS bronze.ingestion_log (
                file_name     TEXT PRIMARY KEY,
                target_table  TEXT,
                batch_id      TEXT,
                rows_read     INT,
                rows_inserted INT,
                loaded_at     TIMESTAMP DEFAULT NOW()
            )"""))

    for f in sorted(glob.glob("data/incoming/*.csv")):
        name = os.path.basename(f)
        with engine.connect() as conn:
            done = conn.execute(
                text("SELECT 1 FROM bronze.ingestion_log WHERE file_name = :n"),
                {"n": name}).scalar()
        if done:
            print(f"skip (already loaded): {name}")
            continue

        table = TABLES[name.split("_")[0]]
        batch_id = pd.Timestamp.now().strftime("%Y%m%d%H%M%S")
        df = pd.read_csv(f, dtype=str)
        df["ingested_at"] = pd.Timestamp.now()
        df["source_file"] = name
        df["batch_id"] = batch_id
        cols = ", ".join(f'"{c}"' for c in df.columns)

        with engine.begin() as conn:
            df.to_sql("_stg", conn, schema="bronze", if_exists="replace", index=False)
            result = conn.execute(text(f"""
                INSERT INTO bronze.{table} ({cols})
                SELECT {cols} FROM bronze._stg s
                WHERE NOT EXISTS (
                    SELECT 1 FROM bronze.{table} t WHERE t."{KEY}" = s."{KEY}")"""))
            inserted = result.rowcount
            conn.execute(text("DROP TABLE bronze._stg"))
            conn.execute(text("""
                INSERT INTO bronze.ingestion_log
                    (file_name, target_table, batch_id, rows_read, rows_inserted)
                VALUES (:f, :t, :b, :r, :i)"""),
                {"f": name, "t": table, "b": batch_id, "r": len(df), "i": inserted})
        print(f"{name}: read {len(df)}, inserted {inserted}")

if __name__ == "__main__":
    main()