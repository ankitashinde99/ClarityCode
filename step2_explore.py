import pandas as pd

df = pd.read_excel("ehr_raw_data.xlsx",
                   sheet_name="Raw Visit Data")

# How many visits per service line?
print("=== VISITS BY SERVICE LINE ===")
print(df["Service_Line"].value_counts())
print()

# What CPT codes are submitted most often?
print("=== TOP CPT CODES SUBMITTED ===")
print(df["CPT_Code_Submitted"].value_counts().head(10))
print()

# Average visit duration by visit type
print("=== AVERAGE VISIT DURATION (minutes) ===")
print(df.groupby("Visit_Type")["Visit_Duration_Min"]
        .mean().round(1).sort_values(ascending=False))