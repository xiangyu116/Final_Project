import time
import pandas as pd

from data_generator_v5mini_model import DataDrivenGenerator


def main():

    print("Loading model...")

    start_load = time.time()

    generator = DataDrivenGenerator(
        model_file="generator_model.pkl"
    )

    print(
        f"Model loaded in {time.time()-start_load:.3f}s"
    )


    N = 10000

    print()
    print("Start generating")
    print()


    start_generate = time.time()

    data = []


    for i in range(N):

        sample = generator.generate_one()

        data.append(sample)


        if (i + 1) % 1000 == 0:

            current_time = time.time() - start_generate

            print(
                f"Generated {i+1}/{N}, "
                f"time: {current_time:.3f}s"
            )


    generate_time = time.time() - start_generate


    print()
    print(
        f"Generation finished: {generate_time:.3f}s"
    )

    print(
        f"Average per sample: {generate_time/N:.6f}s"
    )


    print()
    print("Converting dataframe...")


    start_df = time.time()

    df = pd.DataFrame(data)

    print(
        f"DataFrame conversion: {time.time()-start_df:.3f}s"
    )


    print()
    print("Generated preview:")
    print(df.head())


    output = "generated_test_10000.csv"

    df.to_csv(
        output,
        index=False
    )


    print()
    print(
        "Saved:",
        output
    )


if __name__ == "__main__":
    main()