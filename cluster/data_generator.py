import numpy as np

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