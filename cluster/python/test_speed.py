import time
from data_generator_v3mini import DataDrivenGenerator


start = time.time()

print("Start loading")

generator = DataDrivenGenerator(
    "amazon_ecommerce_1M.csv"
)

print(
    "Learning finished",
    time.time()-start
)


start=time.time()

data = generator.generate_one()

print(
    "One sample generated",
    time.time()-start
)

print(data)

