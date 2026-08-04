from mpi4py import MPI
from data_generator import DataDrivenGenerator
import pandas as pd
import time


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


TOTAL_DATA = 10000


local_n = TOTAL_DATA // size


if rank < TOTAL_DATA % size:
    local_n += 1


print(f"[Rank {rank}] Start generating {local_n} samples",flush=True)


generator = DataDrivenGenerator("amazon_ecommerce_1M.csv")

print(f"[Rank {rank}] Generator ready",flush=True)

data = []


start_time = time.time()


for i in range(local_n):

    if i == 0:
        print(
            f"[Rank {rank}] Start first generate_one",
            flush=True
        )

    data.append(
        generator.generate_one()
    )


df = pd.DataFrame(data)
df.to_csv(f"generated_part_{rank}.csv",index=False)
print(f"[Rank {rank}] Finished",flush=True)