# visualization.py
import matplotlib.pyplot as plt
import numpy as np

# def plot_data(X, labels, centroids=None, title="K-means Result"):
#     plt.figure(figsize=(6,6))

#     for k in np.unique(labels):
#         cluster = X[labels == k]
#         plt.scatter(cluster[:,0], cluster[:,1], s=10, label=f"Cluster {int(k)}")

#     if centroids is not None:
#         plt.scatter(
#             centroids[:,0],
#             centroids[:,1],
#             c="black",
#             marker="x",
#             s=200,
#             label="Centroids"
#         )

#     plt.legend()
#     plt.title(title)
#     plt.show()


###DBscan plot
def plot_dbscan(X, labels):
    plt.figure(figsize=(6,6))

    unique_labels = set(labels)

    for l in unique_labels:
        cluster = X[np.array(labels) == l]

        if l == -1:
            plt.scatter(cluster[:,0], cluster[:,1], c='black', label="noise")
        else:
            plt.scatter(cluster[:,0], cluster[:,1], label=f"cluster {l}")

    plt.legend()
    plt.title("DBSCAN result")
    plt.show()