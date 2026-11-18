import glob, os
import pandas as pd
import kagglehub

path = kagglehub.dataset_download("rohitrox/healthcare-provider-fraud-detection-analysis")
os.makedirs("data/incoming", exist_ok=True)

for name, pattern in [("inpatient", "Train_Inpatientdata-*.csv"),
                      ("outpatient", "Train_Outpatientdata-*.csv")]:
    df = pd.read_csv(glob.glob(os.path.join(path, pattern))[0], dtype=str)
    n = len(df)
    for i in range(3):
        part = df.iloc[(i * n) // 3 : ((i + 1) * n) // 3]
        part.to_csv(f"data/incoming/{name}_day{i + 1}.csv", index=False)
        print(f"{name}_day{i + 1}.csv: {len(part)} rows")