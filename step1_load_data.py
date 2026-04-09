import pandas as pd

df = pd.read_excel("ehr_raw_data.xlsx",
                   sheet_name="Raw Visit Data")

print("Number of visits:", len(df))
print("Number of columns:", len(df.columns))
print()
print("All column names:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i}. {col}")