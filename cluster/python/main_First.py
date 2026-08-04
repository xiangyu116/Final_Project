from data_generator_v5mini_model import DataDrivenGenerator
#First run
generator = DataDrivenGenerator(
    input_csv="amazon_ecommerce_1M.csv"
)

generator.save_model(
    "generator_model.pkl"
)
