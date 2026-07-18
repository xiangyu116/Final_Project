from data_generator import generate_amazon_like_data

df = generate_amazon_like_data(n=1000)

print(df.head())
print(df.shape)

df.to_csv("generated_amazon_data.csv", index=False)