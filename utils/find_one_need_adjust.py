import pandas as pd

df = pd.read_csv('check_factors.csv')
for col in df.columns:
    if df[col].iloc[0] != df[col].iloc[-1]:
        print(f"Column '{col}' has different first and last values.")