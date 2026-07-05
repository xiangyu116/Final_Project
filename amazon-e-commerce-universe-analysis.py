#!/usr/bin/env python
# coding: utf-8

import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
total_start = time.time()


df = pd.read_csv('amazon_ecommerce_1M.csv')
df.head(10)


df.info()


# 

df.describe()


df.isnull().sum()


df.duplicated().sum()


df['category'].value_counts()


df['subcategory'].value_counts()


df['brand'].value_counts()


df['price'].value_counts()


df['discount'].value_counts()


df['final_price'].value_counts()


df['rating'].value_counts()


df['review_count'].value_counts()


df['stock'].value_counts()


df['seller_rating'].value_counts()


df['shipping_time_days'].value_counts()


df['location'].value_counts()


df['device'].value_counts()


df['payment_method'].value_counts()


df['is_returned'].value_counts()


df['delivery_status'].value_counts()


df['product_id'].value_counts().sort_values(ascending=False).idxmin()


df['category'].value_counts().sort_values(ascending=False).idxmin()


df['subcategory'].value_counts().sort_values(ascending=False).idxmin()


df['brand'].value_counts().sort_values(ascending=False).idxmin()


df['final_price'].value_counts().sort_values(ascending=False).idxmin()


df['rating'].value_counts().sort_values(ascending=False).idxmin()


df['review_count'].value_counts().sort_values(ascending=False).idxmin()


df['stock'].value_counts().sort_values(ascending=False).idxmin()


df['shipping_time_days'].value_counts().sort_values(ascending=False).idxmin()


df['location'].value_counts().sort_values(ascending=False).idxmin()


df['device'].value_counts().sort_values(ascending=False).idxmin()


df['payment_method'].value_counts().sort_values(ascending=False).idxmin()


df['is_returned'].value_counts().sort_values(ascending=False).idxmin()


df['delivery_status'].value_counts().sort_values(ascending=False).idxmin()


df.groupby('category')['subcategory'].max().sort_values(ascending=False)


df.groupby('category')['brand'].max().sort_values(ascending=False)


df.groupby('category')['price'].max().sort_values(ascending=False)


df.groupby('category')['discount'].max().sort_values(ascending=False)


df.groupby('category')['final_price'].max().sort_values(ascending=False)


df.groupby('category')['rating'].max().sort_values(ascending=False)


df.groupby('category')['review_count'].max().sort_values(ascending=False)


df.groupby('category')['stock'].max().sort_values(ascending=False)


df.groupby('category')['shipping_time_days'].max().sort_values(ascending=False)


df.groupby('category')['location'].max().sort_values(ascending=False)


df.groupby('category')['device'].max().sort_values(ascending=False)


df.groupby('category')['payment_method'].max().sort_values(ascending=False)


df.groupby('category')['is_returned'].max().sort_values(ascending=False)


df.groupby('category')['delivery_status'].max().sort_values(ascending=False)


df.groupby('subcategory')['brand'].max().sort_values(ascending=False)


sns.set_style('darkgrid', {"grid.color": "0.6", "grid.linestyle": ":"})

category = df['category'].value_counts().head(10)

category = category.sort_values()

plt.figure(figsize=(10, 6))

category.plot(
    kind='barh',
    color='skyblue',
    edgecolor='black'
)

plt.title('Top 50 category')
plt.xlabel('subcategory')
plt.ylabel('category')

plt.tight_layout()
plt.show()


sns.set_style('darkgrid', {"grid.color": "0.6", "grid.linestyle": ":"})

brand = df['brand'].value_counts().head(10)

brand = brand.sort_values()

plt.figure(figsize=(10, 6))

brand.plot(
    kind='barh',
    color='skyblue',
    edgecolor='black'
)

plt.title('Top 50 Most artist_country')
plt.xlabel('category')
plt.ylabel('brand')

plt.tight_layout()
plt.show()


import matplotlib.pyplot as plt

top_brands = df['category'].value_counts().head(8)

plt.figure(figsize=(8, 8))

top_brands.plot(
    kind='pie',
    autopct='%1.1f%%',
    startangle=90,   # بيخلي الرسم أوضح
    wedgeprops={'edgecolor': 'black'}
)

plt.title('Top 8 Brands category')

plt.ylabel('')  # لإزالة كلمة "brand" من النص
plt.show()


import matplotlib.pyplot as plt

top_brands = df['subcategory'].value_counts().head(8)

plt.figure(figsize=(8, 8))

top_brands.plot(
    kind='pie',
    autopct='%1.1f%%',
    startangle=90,   # بيخلي الرسم أوضح
    wedgeprops={'edgecolor': 'black'}
)

plt.title('Top 8 Brands subcategory')

plt.ylabel('')  # لإزالة كلمة "brand" من النص
plt.show()


import matplotlib.pyplot as plt

top_brands = df['brand'].value_counts().head(8)

plt.figure(figsize=(8, 8))

top_brands.plot(
    kind='pie',
    autopct='%1.1f%%',
    startangle=90,   # بيخلي الرسم أوضح
    wedgeprops={'edgecolor': 'black'}
)

plt.title('Top 8 Brands brand')

plt.ylabel('')  # لإزالة كلمة "brand" من النص
plt.show()


import matplotlib.pyplot as plt

top_brands = df['price'].value_counts().head(8)

plt.figure(figsize=(8, 8))

top_brands.plot(
    kind='pie',
    autopct='%1.1f%%',
    startangle=90,   # بيخلي الرسم أوضح
    wedgeprops={'edgecolor': 'black'}
)

plt.title('Top 8 Brands price')

plt.ylabel('')  # لإزالة كلمة "brand" من النص
plt.show()


import matplotlib.pyplot as plt

top_brands = df['discount'].value_counts().head(8)

plt.figure(figsize=(8, 8))

top_brands.plot(
    kind='pie',
    autopct='%1.1f%%',
    startangle=90,   # بيخلي الرسم أوضح
    wedgeprops={'edgecolor': 'black'}
)

plt.title('Top 8 Brands discount')

plt.ylabel('')  # لإزالة كلمة "brand" من النص
plt.show()


import matplotlib.pyplot as plt

top_brands = df['final_price'].value_counts().head(8)

plt.figure(figsize=(8, 8))

top_brands.plot(
    kind='pie',
    autopct='%1.1f%%',
    startangle=90,   # بيخلي الرسم أوضح
    wedgeprops={'edgecolor': 'black'}
)

plt.title('Top 8 Brands final_price')

plt.ylabel('')  # لإزالة كلمة "brand" من النص
plt.show()


import matplotlib.pyplot as plt

top_brands = df['rating'].value_counts().head(8)

plt.figure(figsize=(8, 8))

top_brands.plot(
    kind='pie',
    autopct='%1.1f%%',
    startangle=90,   # بيخلي الرسم أوضح
    wedgeprops={'edgecolor': 'black'}
)

plt.title('Top 8 Brands rating')

plt.ylabel('')  # لإزالة كلمة "brand" من النص
plt.show()


import matplotlib.pyplot as plt

top_brands = df['review_count'].value_counts().head(8)

plt.figure(figsize=(8, 8))

top_brands.plot(
    kind='pie',
    autopct='%1.1f%%',
    startangle=90,   # بيخلي الرسم أوضح
    wedgeprops={'edgecolor': 'black'}
)

plt.title('Top 8 Brands review_count')

plt.ylabel('')  # لإزالة كلمة "brand" من النص
plt.show()


import matplotlib.pyplot as plt

top_brands = df['seller_rating'].value_counts().head(8)

plt.figure(figsize=(8, 8))

top_brands.plot(
    kind='pie',
    autopct='%1.1f%%',
    startangle=90,   # بيخلي الرسم أوضح
    wedgeprops={'edgecolor': 'black'}
)

plt.title('Top 8 Brands seller_rating')

plt.ylabel('')  # لإزالة كلمة "brand" من النص
plt.show()


import matplotlib.pyplot as plt

top_brands = df['stock'].value_counts().head(8)

plt.figure(figsize=(8, 8))

top_brands.plot(
    kind='pie',
    autopct='%1.1f%%',
    startangle=90,   # بيخلي الرسم أوضح
    wedgeprops={'edgecolor': 'black'}
)

plt.title('Top 8 Brands stock')

plt.ylabel('')  # لإزالة كلمة "brand" من النص
plt.show()


import matplotlib.pyplot as plt

top_brands = df['shipping_time_days'].value_counts().head(8)

plt.figure(figsize=(8, 8))

top_brands.plot(
    kind='pie',
    autopct='%1.1f%%',
    startangle=90,   # بيخلي الرسم أوضح
    wedgeprops={'edgecolor': 'black'}
)

plt.title('Top 8 Brands shipping_time_days')

plt.ylabel('')  # لإزالة كلمة "brand" من النص
plt.show()


import matplotlib.pyplot as plt

top_brands = df['location'].value_counts().head(10)

plt.figure(figsize=(8, 8))

top_brands.plot(
    kind='pie',
    autopct='%1.1f%%',
    startangle=90,   # بيخلي الرسم أوضح
    wedgeprops={'edgecolor': 'black'}
)

plt.title('Top 10 Brands location')

plt.ylabel('')  # لإزالة كلمة "brand" من النص
plt.show()


import matplotlib.pyplot as plt

top_brands = df['device'].value_counts().head(8)

plt.figure(figsize=(8, 8))

top_brands.plot(
    kind='pie',
    autopct='%1.1f%%',
    startangle=90,   # بيخلي الرسم أوضح
    wedgeprops={'edgecolor': 'black'}
)

plt.title('Top 8 Brands device')

plt.ylabel('')  # لإزالة كلمة "brand" من النص
plt.show()


import matplotlib.pyplot as plt

top_brands = df['payment_method'].value_counts().head(8)

plt.figure(figsize=(8, 8))

top_brands.plot(
    kind='pie',
    autopct='%1.1f%%',
    startangle=90,   # بيخلي الرسم أوضح
    wedgeprops={'edgecolor': 'black'}
)

plt.title('Top 8 Brands payment_method')

plt.ylabel('')  # لإزالة كلمة "brand" من النص
plt.show()


import matplotlib.pyplot as plt

top_methods = df['is_returned'].value_counts().head(8)

plt.figure(figsize=(8, 8))

top_methods.plot(
    kind='pie',
    autopct='%1.1f%%',
    startangle=90,
    wedgeprops={'edgecolor': 'black'}
)

plt.title('Top Payment Methods is_returned')

plt.ylabel('')
plt.show()


import matplotlib.pyplot as plt

top_methods = df['delivery_status'].value_counts().head(8)

plt.figure(figsize=(8, 8))

top_methods.plot(
    kind='pie',
    autopct='%1.1f%%',
    startangle=90,
    wedgeprops={'edgecolor': 'black'}
)

plt.title('Top Payment Methods delivery_status')

plt.ylabel('')
plt.show()


top_countries = df['category'].value_counts().head(10)

top_countries.plot(kind='bar')
plt.title('Top 10 category')
plt.xticks(rotation=45)
plt.show()


top_categories = df['subcategory'].value_counts().head(10)

top_categories.plot(kind='bar')

plt.title('Top 10 subcategory')
plt.xlabel('Category')
plt.ylabel('Count')

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


top_categories = df['brand'].value_counts().head(10)

top_categories.plot(kind='bar')

plt.title('Top 10 subcategory')
plt.xlabel('Category')
plt.ylabel('Count')

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


seller_stats = df.groupby('seller_id').agg(
    total_orders  = ('user_id', 'count'),
    total_revenue = ('final_price', 'sum'),
    avg_rating    = ('rating', 'mean'),
    avg_seller_r  = ('seller_rating', 'mean'),
    return_rate   = ('is_returned', 'mean'),
    avg_ship_days = ('shipping_time_days', 'mean')
).reset_index()

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.patch.set_facecolor('white')
fig.suptitle('Seller Intelligence Dashboard', fontsize=16, fontweight='bold', color='#1e1b4b')

# Orders distribution
ax = axes[0,0]
ax.hist(seller_stats['total_orders'], bins=60, color='#7c3aed', edgecolor='white', linewidth=0.4, alpha=0.85)
ax.set_title('Orders per Seller Distribution', pad=10)
ax.set_xlabel('Total Orders')
ax.set_ylabel('Number of Sellers')
ax.axvline(seller_stats['total_orders'].median(), color='#db2777', linewidth=2, 
           linestyle='--', label=f"Median: {seller_stats['total_orders'].median():.0f}")
ax.legend()

# Seller rating vs return rate scatter
ax = axes[0,1]
sample = seller_stats.sample(min(2000, len(seller_stats)), random_state=42)
sc = ax.scatter(sample['avg_seller_r'], sample['return_rate']*100,
                c=sample['total_orders'], cmap='plasma', alpha=0.6, s=18, edgecolors='none')
plt.colorbar(sc, ax=ax, label='Total Orders')
ax.set_title('Seller Rating vs Return Rate', pad=10)
ax.set_xlabel('Avg Seller Rating')
ax.set_ylabel('Return Rate (%)')

# Seller revenue distribution
ax = axes[1,0]
ax.hist(seller_stats['total_revenue']/1e5, bins=60, color='#059669', edgecolor='white', linewidth=0.4, alpha=0.85)
ax.set_title('Revenue per Seller (₹ Lakh)', pad=10)
ax.set_xlabel('Revenue (₹ Lakh)')
ax.set_ylabel('Number of Sellers')
ax.axvline(seller_stats['total_revenue'].median()/1e5, color='#d97706', linewidth=2,
           linestyle='--', label=f"Median: ₹{seller_stats['total_revenue'].median()/1e5:.1f}L")
ax.legend()

# Avg shipping days distribution
ax = axes[1,1]
ship_dist = df['shipping_time_days'].value_counts().sort_index()
ax.bar(ship_dist.index.astype(str), ship_dist.values/1000, 
       color=['#7c3aed','#2563eb','#0891b2','#059669','#d97706','#db2777'],
       edgecolor='white', linewidth=1.5, width=0.65)
ax.set_title('Shipping Time Distribution', pad=10)
ax.set_xlabel('Days')
ax.set_ylabel('Orders (K)')

plt.tight_layout()
plt.savefig('fig_seller_intel.png', dpi=150, bbox_inches='tight')
plt.show()


from sklearn.preprocessing import LabelEncoder

data = df[['category', 'subcategory']].dropna()

cat_encoder = LabelEncoder()
subcat_encoder = LabelEncoder()

data['category_enc'] = cat_encoder.fit_transform(data['category'])
data['subcategory_enc'] = subcat_encoder.fit_transform(data['subcategory'])

X = data[['category_enc']]
y = data['subcategory_enc']


import pandas as pd

data = df[['category', 'subcategory', 'brand']].dropna()


from sklearn.preprocessing import LabelEncoder

cat_encoder = LabelEncoder()
subcat_encoder = LabelEncoder()
brand_encoder = LabelEncoder()

data['category_enc'] = cat_encoder.fit_transform(data['category'])
data['subcategory_enc'] = subcat_encoder.fit_transform(data['subcategory'])
data['brand_enc'] = brand_encoder.fit_transform(data['brand'])


X = data[['category_enc', 'brand_enc']]
y = data['subcategory_enc']


from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)


from sklearn.metrics import accuracy_score

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))


total_end = time.time()
print("Total runtime:", total_end - total_start, "seconds")







