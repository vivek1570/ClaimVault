import kagglehub, os
import pandas as pd
path = kagglehub.dataset_download("rohitrox/healthcare-provider-fraud-detection-analysis")
print(os.listdir(path))



claims_in = pd.read_csv(os.path.join(path, "Train_Inpatientdata-1542865627584.csv"))
provider = pd.read_csv(os.path.join(path, "Train-1542865627584.csv"))
patients = pd.read_csv(os.path.join(path, "Train_Beneficiarydata-1542865627584.csv"))
inpatient = pd.read_csv(os.path.join(path, "Train_Inpatientdata-1542865627584.csv"))
outpatient = pd.read_csv(os.path.join(path, "Train_Outpatientdata-1542865627584.csv"))
print(claims_in.shape)
print(claims_in.head())
for name, df in [("provider", provider), ("patients", patients),
                 ("inpatient", inpatient), ("outpatient", outpatient)]:
    print(name, df.shape)