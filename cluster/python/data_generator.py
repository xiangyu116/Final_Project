import numpy as np
import pandas as pd



def generate_simple_data(n=300, k=3, dim=2):
    np.random.seed(42)

    data = []
    labels = []

    points_per_cluster = n // k

    for i in range(k):
        center = np.random.uniform(-10, 10, dim)

        cluster = np.random.randn(points_per_cluster, dim) + center

        data.append(cluster)
        labels += [i] * points_per_cluster

    data = np.vstack(data)
    labels = np.array(labels)

    return data, labels






###simple
# def generate_amazon_like_data(n=1000, random_state=42):
#     np.random.seed(random_state)

#     categories = ["Electronics", "Clothing", "Beauty", "Home", "Sports"]

#     subcategories = {
#         "Electronics": ["Mobile", "Laptop", "Camera"],
#         "Clothing": ["Men", "Women", "Kids"],
#         "Beauty": ["Makeup", "Skincare"],
#         "Home": ["Furniture", "Decor"],
#         "Sports": ["Fitness", "Outdoor", "Cycling"]
#     }

#     brands = ["Apple", "Samsung", "Sony", "HP", "Nike", "Adidas", "H&M", "Zara", "Boat", "LG"]
#     locations = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Hyderabad"]
#     devices = ["Web", "Mobile App", "Tablet"]
#     payments = ["UPI", "Credit Card", "Debit Card", "Cash on Delivery"]

#     rows = []

#     for i in range(n):
#         category = np.random.choice(categories)
#         subcategory = np.random.choice(subcategories[category])
#         brand = np.random.choice(brands)

#         # category-based price
#         if category == "Electronics":
#             price = np.random.uniform(10000, 80000)
#             discount = np.random.uniform(5, 20)
#         elif category == "Clothing":
#             price = np.random.uniform(500, 5000)
#             discount = np.random.uniform(20, 70)
#         elif category == "Beauty":
#             price = np.random.uniform(300, 6000)
#             discount = np.random.uniform(5, 30)
#         elif category == "Home":
#             price = np.random.uniform(1000, 30000)
#             discount = np.random.uniform(10, 50)
#         else:  # Sports
#             price = np.random.uniform(1000, 20000)
#             discount = np.random.uniform(5, 40)

#         final_price = price * (1 - discount / 100)

#         rating = np.clip(np.random.normal(4.0, 0.5), 1.0, 5.0)
#         review_count = np.random.randint(1, 100)
#         stock = np.random.randint(1, 500)
#         seller_rating = np.clip(np.random.normal(4.0, 0.6), 1.0, 5.0)

#         location = np.random.choice(locations)
#         device = np.random.choice(devices)
#         payment = np.random.choice(payments)

#         # simple shipping rule
#         if location in ["Delhi", "Mumbai"]:
#             shipping_time_days = np.random.randint(1, 4)
#         else:
#             shipping_time_days = np.random.randint(2, 7)

#         # return probability rule
#         return_prob = 0.1
#         if rating < 3.5:
#             return_prob += 0.2
#         if shipping_time_days >= 5:
#             return_prob += 0.15

#         is_returned = np.random.rand() < return_prob

#         if is_returned:
#             delivery_status = "Returned"
#         elif shipping_time_days >= 5:
#             delivery_status = np.random.choice(["Delayed", "In Transit"])
#         else:
#             delivery_status = np.random.choice(["Delivered", "In Transit"])

#         row = {
#             "user_id": f"U{100000 + i}",
#             "product_id": f"P{20000 + i}",
#             "category": category,
#             "subcategory": subcategory,
#             "brand": brand,
#             "price": round(price, 2),
#             "discount": round(discount, 2),
#             "final_price": round(final_price, 2),
#             "rating": round(rating, 1),
#             "review_count": review_count,
#             "stock": stock,
#             "seller_id": f"S{3000 + np.random.randint(0, 9000)}",
#             "seller_rating": round(seller_rating, 1),
#             "shipping_time_days": shipping_time_days,
#             "location": location,
#             "device": device,
#             "payment_method": payment,
#             "is_returned": is_returned,
#             "delivery_status": delivery_status
#         }

#         rows.append(row)

#     return pd.DataFrame(rows)






class DataDrivenGenerator:

    def __init__(self, input_csv):
        self.df = pd.read_csv(input_csv)
        self.prepare_statistics()

    # -------------------------
    # 1. Learning statistical distributions
    # -------------------------
    def prepare_statistics(self):

        # category probability
        self.category_prob = self.df["category"].value_counts(normalize=True)

        # subcategory mapping
        self.subcategory_map = self.df.groupby("category")["subcategory"].apply(list)

        # brand mapping
        self.brand_map = self.df.groupby("category")["brand"].apply(list)

        # numeric distributions per category
        self.category_stats = {}

        for cat in self.df["category"].unique():
            sub = self.df[self.df["category"] == cat]

            self.category_stats[cat] = {
                "price_mean": sub["price"].mean(),
                "price_std": sub["price"].std(),

                "discount_mean": sub["discount"].mean(),
                "discount_std": sub["discount"].std(),

                "rating_mean": sub["rating"].mean(),
                "rating_std": sub["rating"].std(),

                "shipping_mean": sub["shipping_time_days"].mean(),
                "shipping_std": sub["shipping_time_days"].std(),
            }

        # global distributions
        self.locations = self.df["location"].value_counts(normalize=True)
        self.devices = self.df["device"].value_counts(normalize=True)
        self.payments = self.df["payment_method"].value_counts(normalize=True)

    # -------------------------
    # 2. ID generator
    # -------------------------
    def random_id(self, prefix):
        return prefix + str(np.random.randint(100000, 999999))

    # -------------------------
    # 3. sample category
    # -------------------------
    def sample_category(self):
        return np.random.choice(
            self.category_prob.index,
            p=self.category_prob.values
        )

    # -------------------------
    # 4. generate one sample
    # -------------------------
    def generate_one(self):

        category = self.sample_category()

        stats = self.category_stats[category]

        # subcategory / brand
        subcategory = np.random.choice(self.subcategory_map[category])
        brand = np.random.choice(self.brand_map[category])

        # numeric generation (learned distributions)
        price = np.random.normal(stats["price_mean"], stats["price_std"])
        discount = np.random.normal(stats["discount_mean"], stats["discount_std"])
        rating = np.random.normal(stats["rating_mean"], stats["rating_std"])
        shipping = np.random.normal(stats["shipping_mean"], stats["shipping_std"])

        # clip values
        price = max(price, 100)
        discount = np.clip(discount, 0, 80)
        rating = np.clip(rating, 1, 5)
        shipping = max(1, int(abs(shipping)))

        final_price = price * (1 - discount / 100)

        # global categorical
        location = np.random.choice(self.locations.index, p=self.locations.values)
        device = np.random.choice(self.devices.index, p=self.devices.values)
        payment = np.random.choice(self.payments.index, p=self.payments.values)

        # return probability model
        return_prob = 1 / (1 + np.exp(
            -(-1.5 * rating + 0.4 * shipping)
        ))

        is_returned = np.random.rand() < return_prob

        if is_returned:
            delivery_status = "Returned"
        elif shipping >= 5:
            delivery_status = "Delayed"
        else:
            delivery_status = "Delivered"

        return {
            "user_id": self.random_id("U"),
            "product_id": self.random_id("P"),
            "seller_id": self.random_id("S"),

            "category": category,
            "subcategory": subcategory,
            "brand": brand,

            "price": round(price, 2),
            "discount": round(discount, 2),
            "final_price": round(final_price, 2),

            "rating": round(rating, 2),
            "shipping_time_days": shipping,

            "location": location,
            "device": device,
            "payment_method": payment,

            "is_returned": bool(is_returned),
            "delivery_status": delivery_status
        }

    # -------------------------
    # 5. generate dataset
    # -------------------------
    def generate(self, n=1000):
        data = []
        for _ in range(n):
            data.append(self.generate_one())

        return pd.DataFrame(data)
