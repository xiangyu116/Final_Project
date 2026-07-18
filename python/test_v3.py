from data_generator import DataDrivenGenerator

generator = DataDrivenGenerator("amazon_ecommerce_1M.csv")

df_new = generator.generate(n=5000)

print(df_new.head())

df_new.to_csv("generated_v3_data.csv", index=False)