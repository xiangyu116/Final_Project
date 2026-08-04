# import time

# from data_generator import DataDrivenGenerator


# generator = DataDrivenGenerator(
#     "amazon_ecommerce_1M.csv"
# )


# N = 10000


# # =====================
# # Test generate_user
# # =====================

# users = []

# start = time.time()

# for _ in range(N):
#     user = generator.generate_user()
#     users.append(user)

# end = time.time()


# print("generate_user:")
# print(end-start)
# print("per sample:")
# print((end-start)/N)



# # =====================
# # Test choose_category only
# # =====================

# start = time.time()

# for i in range(N):

#     generator.choose_category(
#         users[i]
#     )

# end = time.time()


# print("\nchoose_category only:")
# print(end-start)
# print("per sample:")
# print((end-start)/N)


import time

from data_generator import DataDrivenGenerator


generator = DataDrivenGenerator(
    "amazon_ecommerce_1M.csv"
)


N = 10000


# =========================
# Test existing user
# =========================

start = time.time()

for _ in range(N):

    generator.choose_existing_user()


end = time.time()


print("choose_existing_user:")
print(end-start)

print("per sample:")
print((end-start)/N)



# =========================
# Test new user
# =========================

start = time.time()

for _ in range(N):

    generator.generate_new_user()


end = time.time()


print("\ngenerate_new_user:")
print(end-start)

print("per sample:")
print((end-start)/N)