import pandas as pd

df = pd.read_csv("amazon_ecommerce_1M.csv")

print("Total rows:")
print(len(df))

print("\nUnique users:")
print(df["user_id"].nunique())

print("\nFirst users:")
print(df["user_id"].head())