# main.py

from data_generator import generate_simple_data
from kmeans import KMeans
# from visualization import plot_data
### DBSCAN
from visualization import plot_dbscan
from dbscan import MyDBSCAN

def main():

    # 1. generate dataset
    X, true_labels = generate_simple_data(n=300, k=3, dim=2)

    labels= MyDBSCAN(D=X, eps=1.5, MinPts=5)


    # 2. run K-means
    model = KMeans(K=3)
    model.fit(X)

    # 3. visualize result
    #plot_data(X, model.labels, model.centroids, title="Sequential K-means")

    plot_dbscan(X, labels)
if __name__ == "__main__":
    main()