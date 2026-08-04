import numpy as np
import pandas as pd
import pickle

class DataDrivenGenerator:
    def __init__(self,input_csv=None,model_file=None):
        if model_file is not None:
            self.load_model(model_file)
        else:
            self.df=pd.read_csv(input_csv)
            self.df=self.df.sample(frac=0.2,random_state=42).reset_index(drop=True)
            self.prepare_statistics()

    def save_model(self,filename):
        data=self.__dict__.copy()
        if "df" in data:
            del data["df"]
        with open(filename,"wb") as f:
            pickle.dump(data,f)
        print("Model saved:",filename)

    def load_model(self,filename):
        with open(filename,"rb") as f:
            data=pickle.load(f)
        self.__dict__.update(data)
        print("Model loaded:",filename)

    def prepare_statistics(self):
        self.category_prob=self.df["category"].value_counts(normalize=True)
        self.category_stats={}
        for cat in self.df["category"].unique():
            sub=self.df[self.df["category"]==cat]
            self.category_stats[cat]={
                "price_mean":sub["price"].mean(),
                "discount_mean":sub["discount"].mean(),
                "rating_mean":sub["rating"].mean(),
                "shipping_mean":sub["shipping_time_days"].mean(),
                "shipping_std":sub["shipping_time_days"].std()
            }

        self.locations=self.df["location"].value_counts(normalize=True)
        self.devices=self.df["device"].value_counts(normalize=True)
        self.payments=self.df["payment_method"].value_counts(normalize=True)

        self.location_values=self.locations.index.to_numpy()
        self.location_probs=self.locations.values
        self.device_values=self.devices.index.to_numpy()
        self.device_probs=self.devices.values
        self.payment_values=self.payments.index.to_numpy()
        self.payment_probs=self.payments.values

        user_stats=self.df.groupby("user_id").agg(
            purchase_count=("product_id","count"),
            avg_price=("final_price","mean"),
            avg_discount=("discount","mean"),
            return_rate=("is_returned","mean")
        )

        user_category_distribution={}
        for user,group in self.df.groupby("user_id"):
            user_category_distribution[user]=group["category"].value_counts(normalize=True).to_dict()

        self.user_profile={}

        for user,row in user_stats.iterrows():
            avg_price=row["avg_price"]
            if avg_price<100:
                level="low"
            elif avg_price<1000:
                level="medium"
            else:
                level="high"

            categories=user_category_distribution[user]

            self.user_profile[user]={
                "purchase_count":int(row["purchase_count"]),
                "spending_level":level,
                "category_distribution":categories,
                "category_values":list(categories.keys()),
                "category_probs":list(categories.values())
            }

        self.user_ids=np.array(list(self.user_profile.keys()))
        self.user_profiles_array=list(self.user_profile.values())

        user_purchase_counts=[]
        user_spending_levels=[]
        user_category_distributions=[]

        for user,profile in self.user_profile.items():
            user_purchase_counts.append(profile["purchase_count"])
            user_spending_levels.append(profile["spending_level"])
            user_category_distributions.append(profile["category_distribution"])

        self.user_behavior_model={
            "purchase_count_values":user_purchase_counts,
            "spending_level_values":user_spending_levels,
            "category_distribution_values":user_category_distributions
        }

        self.prepare_product_statistics()



    def prepare_product_statistics(self):
        self.product_profile={}
        for (category,product),group in self.df.groupby(["category","product_id"]):
            seller_dist=group["seller_id"].value_counts(normalize=True)
            subcategory_dist=group["subcategory"].value_counts(normalize=True)
            brand_dist=group["brand"].value_counts(normalize=True)
            self.product_profile[(category,product)]={
                "subcategory_distribution":{
                    "values":subcategory_dist.index.to_numpy(),
                    "probabilities":subcategory_dist.values
                },
                "brand_distribution":{
                    "values":brand_dist.index.to_numpy(),
                    "probabilities":brand_dist.values
                },
                "seller_distribution":{
                    "values":seller_dist.index.to_numpy(),
                    "probabilities":seller_dist.values
                },
                "price_mean":group["price"].mean(),
                "discount_mean":group["discount"].mean(),
                "rating_mean":group["rating"].mean(),
                "review_mean":group["review_count"].mean(),
                "stock_mean":group["stock"].mean(),
                "seller_rating_mean":group["seller_rating"].mean()
            }

        self.category_products={}

        for category,group in self.df.groupby("category"):
            product_dist=group["product_id"].value_counts(normalize=True)
            self.category_products[category]={
                "values":product_dist.index.to_numpy(),
                "probabilities":product_dist.values
            }

        self.global_category_distribution=self.df["category"].value_counts(normalize=True).to_dict()
        self.global_categories=list(self.global_category_distribution.keys())
        self.global_category_probs=list(self.global_category_distribution.values())



    def sample_from_distribution(self,distribution):
        return np.random.choice(
            distribution["values"],
            p=distribution["probabilities"]
        )

    def random_id(self,prefix):
        return prefix+str(np.random.randint(100000,999999))

    def choose_existing_user(self):
        idx=np.random.randint(len(self.user_profiles_array))
        profile=self.user_profiles_array[idx]
        return {
            "user_id":self.user_ids[idx],
            "category_values":profile["category_values"],
            "category_probs":profile["category_probs"]
        }

    def generate_new_user(self):
        user_id=self.random_id("U")
        category_list=self.user_behavior_model["category_distribution_values"]
        category_preference=category_list[np.random.randint(len(category_list))]
        return {
            "user_id":user_id,
            "category_values":list(category_preference.keys()),
            "category_probs":list(category_preference.values())
        }

    def generate_user(self):
        if np.random.random()<0.7:
            return self.choose_existing_user()
        else:
            return self.generate_new_user()

    def choose_category(self,user):
        if np.random.random()<0.2:
            return np.random.choice(
                self.global_categories,
                p=self.global_category_probs
            )
        return np.random.choice(
            user["category_values"],
            p=user["category_probs"]
        )

    def choose_product(self,category):
        return np.random.choice(
            self.category_products[category]["values"],
            p=self.category_products[category]["probabilities"]
        )

    def generate_one(self):
        user=self.generate_user()
        category=self.choose_category(user)
        product_id=self.choose_product(category)

        product_info=self.product_profile[
            (category,product_id)
        ]

        subcategory=self.sample_from_distribution(
            product_info["subcategory_distribution"]
        )

        brand=self.sample_from_distribution(
            product_info["brand_distribution"]
        )

        seller_id=self.sample_from_distribution(
            product_info["seller_distribution"]
        )

        price=np.random.normal(
            product_info["price_mean"],
            product_info["price_mean"]*0.1
        )

        discount=np.random.normal(
            product_info["discount_mean"],
            product_info["discount_mean"]*0.1
        )

        rating=np.random.normal(
            product_info["rating_mean"],
            0.2
        )

        review_count=np.random.normal(
            product_info["review_mean"],
            product_info["review_mean"]*0.2
        )

        stock=np.random.normal(
            product_info["stock_mean"],
            product_info["stock_mean"]*0.2
        )

        seller_rating=np.random.normal(
            product_info["seller_rating_mean"],
            0.2
        )

        shipping=np.random.normal(
            self.category_stats[category]["shipping_mean"],
            self.category_stats[category]["shipping_std"]
        )

        price=max(price,0)

        discount=np.clip(
            discount,
            0,
            80
        )

        rating=np.clip(
            rating,
            1,
            5
        )

        review_count=max(
            0,
            int(review_count)
        )

        stock=max(
            0,
            int(stock)
        )

        seller_rating=np.clip(
            seller_rating,
            1,
            5
        )

        shipping=max(
            1,
            int(abs(shipping))
        )

        final_price=price*(1-discount/100)

        location=np.random.choice(
            self.location_values,
            p=self.location_probs
        )

        device=np.random.choice(
            self.device_values,
            p=self.device_probs
        )

        payment=np.random.choice(
            self.payment_values,
            p=self.payment_probs
        )

        purchase_date=(
            pd.Timestamp.today()
            -
            pd.Timedelta(
                days=np.random.randint(0,365)
            )
        ).strftime("%Y-%m-%d")

        return_prob=1/(1+np.exp(-(-1.5*rating+0.4*shipping)))

        is_returned=np.random.rand()<return_prob

        if is_returned:
            delivery_status="Returned"
        elif shipping>=5:
            delivery_status="Delayed"
        else:
            delivery_status=np.random.choice(
                [
                    "Delivered",
                    "In Transit"
                ],
                p=[
                    0.5,
                    0.5
                ]
            )

        return {
            "user_id":user["user_id"],
            "product_id":product_id,
            "category":category,
            "subcategory":subcategory,
            "brand":brand,
            "price":round(price,2),
            "discount":round(discount,2),
            "final_price":round(final_price,2),
            "rating":round(rating,2),
            "review_count":review_count,
            "stock":stock,
            "seller_id":seller_id,
            "seller_rating":round(seller_rating,2),
            "purchase_date":purchase_date,
            "shipping_time_days":shipping,
            "location":location,
            "device":device,
            "payment_method":payment,
            "is_returned":bool(is_returned),
            "delivery_status":delivery_status
        }

    def generate(self,n=1000):
        data=[]
        for _ in range(n):
            data.append(
                self.generate_one()
            )
        return pd.DataFrame(data)