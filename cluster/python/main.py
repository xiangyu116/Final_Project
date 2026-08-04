# # # main.py
# # import time
# # from kmeans import KMeans
# # # from visualization import plot_data
# # ### DBSCAN
# # from visualization import plot_dbscan
# # from dbscan import MyDBSCAN



# # ### amazon
# # from data_generator import DataDrivenGenerator



# # ###v3 study/generatre data

# # def main():

# #     ## amazon
# #     generator = DataDrivenGenerator("amazon_ecommerce_1M.csv")

# #     #df_new = generator.generate(n=5000)

# #     #print(df_new.head())

# #     #df_new.to_csv("generated_v3_data.csv", index=False)


# #     #test
# #     # print(len(generator.user_profile))
# #     # print(len(generator.product_profile))

# #     print("Finishing learning")
    
# #     generated_df = generator.generate(n=10000)
# #     start = time.time()

# #     end = time.time()


# #     print("Generated:",len(generated_df))

# #     print("Time:",end-start)

# #     print(generated_df.head())



# #     generated_df.to_csv("generated_test_10000.csv",index=False)


# #     print("\nSaved: generated_test_10000.csv")


# #     old_users = set(generator.user_profile.keys())


# #     old_ratio = (
# #     generated_df["user_id"]
# #     .isin(old_users)
# #     .mean()
# #     )


# #     print("\nOld user ratio:")
# #     print(old_ratio)
# #     # =========================
# # # Test 2:
# # # category distribution
# # # =========================

# #     print("\nGenerated category distribution:")
# #     print(generated_df["category"].value_counts(normalize=True))


# #     print("\nOriginal category distribution:")
# #     print(generator.df["category"].value_counts(normalize=True))


# # # =========================
# # # Test 3:
# # # product-category consistency
# # # =========================

# #     wrong_count = 0


# #     for _, row in generated_df.iterrows():

# #         product = row["product_id"]
# #         category = row["category"]


# #         if category not in generator.product_profile[product]["category_distribution"]:
# #             wrong_count += 1


# #     print("\nProduct-category mismatch:")
# #     print(wrong_count)


# # # =========================
# # # Test 4:
# # # seller consistency
# # # =========================

# #     seller_missing = 0


# #     for _, row in generated_df.iterrows():

# #         product = row["product_id"]
# #         seller = row["seller_id"]


# #         if seller not in generator.product_profile[product]["seller_distribution"]:
# #             seller_missing += 1


# #     print("\nProduct-seller mismatch:")
# #     print(seller_missing)





# #     # ##3D/nd
# #     # #X, true_labels = generate_simple_data(n=300, k=3, dim=3)

# #     # labels= MyDBSCAN(D=X, eps=1.5, MinPts=5)


# #     # # 2. run K-means
# #     # model = KMeans(K=3)
# #     # model.fit(X)

# #     # # 3. visualize result
# #     # #plot_data(X, model.labels, model.centroids, title="Sequential K-means")

# #     # plot_dbscan(X, labels)
    
# # if __name__ == "__main__":
# #     main()




# import time
# from data_generator import DataDrivenGenerator


# def main():

#     # =========================
#     # 1. Load and learn dataset
#     # =========================

#     print("Start loading")

#     generator = DataDrivenGenerator(
#         "amazon_ecommerce_1M.csv"
#     )

#     print("Finishing learning")


#     # =========================
#     # 2. Generate synthetic data
#     # =========================

#     print("\nStart generating")

#     start = time.time()

#     generated_df = generator.generate(
#         n=10000
#     )

#     end = time.time()


#     print("\nGenerated samples:")
#     print(len(generated_df))


#     print("\nGeneration time:")
#     print(end - start, "seconds")


#     print("\nGenerated data preview:")
#     print(generated_df.head())


#     # save result

#     generated_df.to_csv(
#         "generated_test_10000.csv",
#         index=False
#     )

#     print("\nSaved: generated_test_10000.csv")


#     # =========================
#     # 3. Existing user ratio
#     # =========================

#     old_users = set(
#         generator.user_profile.keys()
#     )


#     old_ratio = (
#         generated_df["user_id"]
#         .isin(old_users)
#         .mean()
#     )


#     print("\nOld user ratio:")
#     print(old_ratio)


#     # =========================
#     # 4. Category distribution
#     # =========================

#     print("\nGenerated category distribution:")

#     print(
#         generated_df["category"]
#         .value_counts(normalize=True)
#     )


#     print("\nOriginal category distribution:")

#     print(
#         generator.df["category"]
#         .value_counts(normalize=True)
#     )


#     # =========================
#     # 5. Product-category consistency
#     # =========================

#     wrong_category = 0


#     for _, row in generated_df.iterrows():

#         product = row["product_id"]
#         category = row["category"]


#         product_categories = (
#             generator
#             .product_profile[product]
#             ["category_distribution"]
#             ["values"]
#         )


#         if category not in product_categories:
#             wrong_category += 1



#     print("\nProduct-category mismatch:")
#     print(wrong_category)



#     # =========================
#     # 6. Product-seller consistency
#     # =========================

#     wrong_seller = 0


#     for _, row in generated_df.iterrows():

#         product = row["product_id"]
#         seller = row["seller_id"]


#         product_sellers = (
#             generator
#             .product_profile[product]
#             ["seller_distribution"]
#             ["values"]
#         )


#         if seller not in product_sellers:
#             wrong_seller += 1



#     print("\nProduct-seller mismatch:")
#     print(wrong_seller)



#     # =========================
#     # 7. Price distribution
#     # =========================

#     print("\nGenerated final price statistics:")

#     print(
#         generated_df["final_price"]
#         .describe()
#     )


#     print("\nOriginal final price statistics:")

#     print(
#         generator.df["final_price"]
#         .describe()
#     )



# if __name__ == "__main__":
#     main()




# import time

# from data_generator_v4mini_model import DataDrivenGenerator

#First run
# generator = DataDrivenGenerator(
#     input_csv="amazon_ecommerce_1M.csv"
# )

# generator.save_model(
#     "generator_model.pkl"
# )

#Then run


# N = 10000


# tests = {

#     "generate_user":
#         generator.generate_user,

#     "choose_category":
#         lambda: generator.choose_category(
#             generator.generate_user()
#         ),

#     "generate_one":
#         generator.generate_one
# }



# for name, func in tests.items():

#     start = time.time()

#     for _ in range(N):
#         func()

#     end = time.time()


#     print(
#         name,
#         ":",
#         end-start,
#         "seconds"
#     )

#     print(
#         "per sample:",
#         (end-start)/N
#     )





