from mpi4py import MPI
from data_generator_v5mini_model import DataDrivenGenerator
import pandas as pd
import time
import pickle


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


TOTAL_DATA = 10000


local_n = TOTAL_DATA // size

if rank < TOTAL_DATA % size:
    local_n += 1


if rank == 0:

    print("[Rank 0] Loading model", flush=True)

    start_load = time.time()

    generator = DataDrivenGenerator(
        model_file="generator_model.pkl"
    )

    print(
        f"[Rank 0] Model loaded: {time.time()-start_load:.3f}s",
        flush=True
    )


    model_data = pickle.dumps(
        generator.__dict__
    )

else:

    model_data = None



model_data = comm.bcast(
    model_data,
    root=0
)



if rank != 0:

    generator = DataDrivenGenerator.__new__(
        DataDrivenGenerator
    )

    generator.__dict__ = pickle.loads(
        model_data
    )



print(
    f"[Rank {rank}] Start generating {local_n} samples",
    flush=True
)



start_generate = time.time()


data = []


for i in range(local_n):

    data.append(
        generator.generate_one()
    )

    if (i+1) % 1000 == 0:

        print(
            f"[Rank {rank}] Generated {i+1}/{local_n}",
            flush=True
        )



df = pd.DataFrame(data)


df.to_csv(
    f"generated_part_{rank}.csv",
    index=False
)


generate_time = time.time()-start_generate


print(
    f"[Rank {rank}] Finished in {generate_time:.3f}s",
    flush=True
)