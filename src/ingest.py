import glob
import os
import pandas as pd
import kagglehub
from sqlalchemy import text
from db import get_engine

DATASET = "rohitrox/healthcare-provider-fraud-detection-analysis"

FILES = {
    "raw_providers":     "Train-*.csv",
    "raw_beneficiaries": "Train_Beneficiarydata-*.csv",
    "raw_inpatient":     "Train_Inpatientdata-*.csv",
    "raw_outpatient":    "Train_Outpatientdata-*.csv",
}

def main():
    path = kagglehub.dataset_download(DATASET)
    engine = get_engine()

    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS bronze"))

    for table, pattern in FILES.items():
        file_path = glob.glob(os.path.join(path, pattern))[0]
        df = pd.read_csv(file_path, dtype=str)      # everything as text
        df["ingested_at"] = pd.Timestamp.now()
        df.to_sql(table, engine, schema="bronze", if_exists="replace",
                  index=False, chunksize=50000)
        print(f"bronze.{table}: {len(df)} rows loaded")

if __name__ == "__main__":
    main()
