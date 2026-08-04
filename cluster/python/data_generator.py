import numpy as np
import pandas as pd


class DataDrivenGenerator:

    def __init__(self, input_csv):
        self.df = pd.read_csv(input_csv)
        self.prepare_statistics()

    # 1. Learning statistical distributions
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


        self.location_values = self.locations.index.to_numpy()
        self.location_probs = self.locations.values

        self.device_values = self.devices.index.to_numpy()
        self.device_probs = self.devices.values

        self.payment_values = self.payments.index.to_numpy()
        self.payment_probs = self.payments.values
        #user behavior learning
        # self.user_profile={}
        # for user,group in self.df.groupby("user_id"):
        #     avg_price=group["final_price"].mean()
        #     if avg_price<100:
        #         spending_level="low"
        #     elif avg_price<1000:
        #         spending_level="medium"
        #     else:
        #         spending_level="high"

        #     self.user_profile[user]={
        #         "purchase_count": len(group),
        #         "spending_level":spending_level,
        #         "avg_discount": group["discount"].mean(),
        #         "return_rate": group["is_returned"].mean(),
        #         "category_distribution":group["category"].value_counts(normalize=True).to_dict()
        #     }


        user_stats = (self.df.groupby("user_id")
                      .agg(
                          purchase_count=("product_id","count"),
                          avg_price=("final_price","mean"),
                          avg_discount=("discount","mean"),
                          return_rate=("is_returned","mean")
                          )
                     )

        user_category_distribution = {}

        for user, group in self.df.groupby("user_id"):
            user_category_distribution[user] = (
                group["category"]
                .value_counts(normalize=True)
                .to_dict()
            )

        self.user_profile={}


        for user,row in user_stats.iterrows():

            avg_price=row["avg_price"]

            if avg_price < 100:
                spending_level="low"

            elif avg_price < 1000:
                spending_level="medium"

            else:
                spending_level="high"


            # categories = (self.df[self.df["user_id"]==user]["category"].value_counts(normalize=True).to_dict())
            categories = user_category_distribution[user]
            self.user_profile[user]={

                "purchase_count":
                int(row["purchase_count"]),

                "spending_level":
                spending_level,

                "avg_discount":
                row["avg_discount"],

                "return_rate":row["return_rate"],

                "category_distribution":categories,

                "category_values":list(categories.keys()),

                "category_probs":list(categories.values())
                }

        self.product_profile={}
        product_group = self.df.groupby("product_id")
        # for product,group in product_group:
        #     seller_dist = (group["seller_id"].value_counts(normalize=True))


        #     category_dist = (group["category"].value_counts(normalize=True))


        #     brand_dist = (group["brand"].value_counts(normalize=True))


        #     subcategory_dist = (group["subcategory"].value_counts(normalize=True))
        #     self.product_profile[product]={
        #         "purchase_count": len(group),
        #         "category_distribution": {
        #                 "values": list(category_dist.index),
        #                 "probabilities": list(category_dist.values)},
        #         "subcategory_distribution":{
        #                 "values": list(subcategory_dist.index),
        #                 "probabilities": list(subcategory_dist.values)},
        #         "brand_distribution":{
        #                 "values": list(brand_dist.index),
        #                 "probabilities": list(brand_dist.values)},
        #         "seller_distribution":{
        #                 "values": list(seller_dist.index),
        #                 "probabilities": list(seller_dist.values)},
        #         "price_mean": group["price"].mean(),
        #         "discount_mean": group["discount"].mean(),
        #         "rating_mean": group["rating"].mean(),
        #         "review_mean": group["review_count"].mean(),
        #         "stock_mean": group["stock"].mean(),
        #         "seller_rating_mean":group["seller_rating"].mean(),
        #         "unique_users":group["user_id"].nunique()
        #     }

        for product, group in product_group:
            seller_dist = (group["seller_id"].value_counts(normalize=True))
            category_dist = (group["category"].value_counts(normalize=True))
            brand_dist = (group["brand"].value_counts(normalize=True))
            subcategory_dist = (group["subcategory"].value_counts(normalize=True))

            self.product_profile[product] = {
                "purchase_count":len(group),
                "category_distribution": {"values":category_dist.index.to_numpy(),"probabilities":category_dist.values},
                "subcategory_distribution": {"values":subcategory_dist.index.to_numpy(),"probabilities": subcategory_dist.values},
                "brand_distribution": {"values":brand_dist.index.to_numpy(),"probabilities": brand_dist.values},
                "seller_distribution": {"values":seller_dist.index.to_numpy(),"probabilities":seller_dist.values},
                "price_mean":group["price"].mean(),
                "discount_mean":group["discount"].mean(),
                "rating_mean":group["rating"].mean(),
                "review_mean":group["review_count"].mean(),
                "stock_mean":group["stock"].mean(),
                "seller_rating_mean":group["seller_rating"].mean(),
                "unique_users":group["user_id"].nunique()
    }

        # check = (self.df.groupby("product_id")["category"].nunique())
        # if len(check[check > 1]) > 0:
        #     print("Warning: product has multiple categories")

        # seller_check = (self.df.groupby("product_id")["seller_id"].nunique())

        # if len(seller_check[seller_check > 1]) > 0:
        #     print("Warning: product has multiple sellers")

        # self.category_products = {}
        # for category, group in self.df.groupby("category"):
        #     product_dist = (group["product_id"].value_counts(normalize=True))
        #     self.category_products[category] = {

        #         "values":
        #             list(product_dist.index),

        #         "probabilities":
        #             list(product_dist.values)
        #     }
        self.category_products = {}
        for category, group in self.df.groupby("category"):
            product_dist = (group["product_id"].value_counts(normalize=True))
            self.category_products[category] = {"values":product_dist.index.to_numpy(),"probabilities":product_dist.values}



        # user-product interaction learning
        # self.user_purchase_history={}
        # for user,group in self.df.groupby("user_id"):
        #     self.user_purchase_history[user]={
        #         "products":list(group["product_id"].unique()),
        #         "categories": list(group["category"].unique())
        #     }
        self.user_purchase_history = (
            self.df.groupby("user_id")
            .agg(products=("product_id",lambda x:list(x.unique())),categories=("category",lambda x:list(x.unique()))).to_dict("index"))

        self.user_behavior_model={}
        user_purchase_counts=[]
        user_spending_levels=[]
        user_return_rates = []
        user_category_distributions=[]

        for user, profile in self.user_profile.items():
            user_purchase_counts.append(profile["purchase_count"])
            user_spending_levels.append(profile["spending_level"])
            user_return_rates.append(profile["return_rate"])
            user_category_distributions.append(profile["category_distribution"])

        self.user_behavior_model={
            "purchase_count_values":user_purchase_counts,
            
            "spending_level_values":user_spending_levels,
            "category_distribution_values":user_category_distributions,
            #Return rate distribution of users
            "return_rate_mean":np.mean(user_return_rates),
            "return_rate_std":np.std(user_return_rates)
        }

        self.category_price_mean = {}

        for category, group in self.df.groupby("category"):
            self.category_price_mean[category] = (group["final_price"].mean())

        self.global_category_distribution = (self.df["category"].value_counts(normalize=True).to_dict())

        self.global_categories = list(self.global_category_distribution.keys())
        self.global_category_probs = list(self.global_category_distribution.values())


        # self.user_ids = list(self.user_profile.keys())
        self.user_ids = np.array(list(self.user_profile.keys()))
        self.user_profiles_array = list(self.user_profile.values())

    def sample_from_distribution(self, distribution):
        # keys = list(distribution.keys())
        # probs = list(distribution.values())
        return np.random.choice(distribution["values"],p=distribution["probabilities"])

    # 2. ID generator
    def random_id(self, prefix):
        return prefix + str(np.random.randint(100000, 999999))

    # generate new user
    def generate_new_user(self):

        user_id = self.random_id("U")

        purchase_count = np.random.choice(self.user_behavior_model["purchase_count_values"])
        spending_level=np.random.choice(self.user_behavior_model["spending_level_values"])
        # category_preference = np.random.choice(self.user_behavior_model["category_distribution_values"])
        category_list = (self.user_behavior_model["category_distribution_values"])
        category_preference = category_list[np.random.randint(len(category_list))]
        return {
            "user_id": user_id,
            "purchase_count": int(purchase_count),
            "spending_level": spending_level,
            "category_preference":category_preference,
            "category_values":list(category_preference.keys()),
            "category_probs":list(category_preference.values())
            }

    def choose_existing_user(self):

        idx = np.random.randint(len(self.user_profiles_array))
        profile=self.user_profiles_array[idx]

        return {
            "user_id": self.user_ids[idx],
            "purchase_count":profile["purchase_count"],
            "spending_level":profile["spending_level"],
            "category_preference":profile["category_distribution"],
            "category_values":profile["category_values"],
            "category_probs":profile["category_probs"]
    }


    def generate_user(self):

        probability = np.random.random()
        if probability < 0.7:
            # keep old users
            return self.choose_existing_user()
        else:
            # create new users
            return self.generate_new_user()

    def choose_category(self, user):
        explore_prob = 0.2
        if np.random.random() < explore_prob:

         # explore new category
            # categories = list(self.global_category_distribution.keys())

            # probabilities = list(self.global_category_distribution.values())

            # return np.random.choice(categories,p=probabilities)
            return np.random.choice(self.global_categories,p=self.global_category_probs)


        else:

            # follow user preference
            # categories = list(user["category_preference"].keys())
            # probabilities = list(user["category_preference"].values())
            categories = user["category_values"]
            probabilities = user["category_probs"]

        return np.random.choice(
            categories,
            p=probabilities)





    
    def choose_product(self, category):
        # products = list(self.category_products[category].keys())

        # probabilities = list(self.category_products[category].values())

        return np.random.choice(
        self.category_products[category]["values"],
        p=self.category_products[category]["probabilities"])

    # 3. sample category
    def sample_category(self):
        return np.random.choice(
            self.category_prob.index,
            p=self.category_prob.values
        )

    # 4. generate one sample
    def generate_one(self):

        # 1. generate user
        user = self.generate_user()

        category = self.choose_category(user)
        product_id = self.choose_product(category)
        product_info = self.product_profile[product_id]

    

        # subcategory / brand
        subcategory = self.sample_from_distribution(product_info["subcategory_distribution"])
        brand = self.sample_from_distribution(product_info["brand_distribution"])
        seller_id = self.sample_from_distribution(product_info["seller_distribution"])
        # numeric generation (learned distributions)
        price = np.random.normal(product_info["price_mean"], product_info["price_mean"] * 0.1)
        discount = np.random.normal(product_info["discount_mean"], product_info["discount_mean"] * 0.1)
        rating = np.random.normal(product_info["rating_mean"], 0.2)
        shipping = np.random.normal(self.category_stats[category]["shipping_mean"], self.category_stats[category]["shipping_std"])

        # clip values
        price = max(price, product_info["price_mean"]*0.1)
        discount = np.clip(discount, 0, 80)
        rating = np.clip(rating, 1, 5)
        shipping = max(1, int(abs(shipping)))

        final_price = price * (1 - discount / 100)

        # global categorical
        # location = np.random.choice(self.locations.index, p=self.locations.values)
        # device = np.random.choice(self.devices.index, p=self.devices.values)
        # payment = np.random.choice(self.payments.index, p=self.payments.values)

        location = np.random.choice(self.location_values,p=self.location_probs)
        device = np.random.choice(self.device_values,p=self.device_probs)
        payment = np.random.choice(self.payment_values,p=self.payment_probs)


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
            "user_id": user["user_id"],
            "product_id": product_id,
            "seller_id": seller_id,

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
    # 5. generate dataset
    def generate(self, n=1000):
        data = []
        for _ in range(n):
            data.append(self.generate_one())

        return pd.DataFrame(data)