# kmeans.py
import numpy as np

class KMeans:
    def __init__(self, K=3, max_iter=100):
        self.K = K
        self.max_iter = max_iter

    def fit(self, X):
        n = X.shape[0]

        # random init
        idx = np.random.choice(n, self.K, replace=False)
        centroids = X[idx]

        labels = np.zeros(n)

        for _ in range(self.max_iter):

            # assign step
            for i in range(n):
                distances = np.sum((X[i] - centroids) ** 2, axis=1)
                labels[i] = np.argmin(distances)

            # update step
            new_centroids = np.zeros_like(centroids)

            for k in range(self.K):
                points = X[labels == k]
                if len(points) > 0:
                    new_centroids[k] = np.mean(points, axis=0)
                else:
                    new_centroids[k] = centroids[k]

            # convergence check
            if np.allclose(centroids, new_centroids):
                break

            centroids = new_centroids

        self.centroids = centroids
        self.labels = labels