#include "kmeans.hpp"

#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <random>

KMeans::KMeans(int K, int max_iter = 100, double tol = 1e-6)
    : K(K), max_iter(max_iter), tol(tol) 
{

}


void KMeans::fit(const std::vector<std::vector<double>>& X) 
{
    int n= X.size();
    int dim= X[0].size();

    labels.assign(n,0);

    std::vector<int> idx(n);
    for (int i=0; i<n; i++)
    {
      idx[i]= i;
    }

    std::mt19937 gen(42);
    std::shuffle(idx.begin(), idx.end(), gen);
    
    centroids.clear();

    for(int k=0; k<K; k++)
    {
      centroids.push_back(X[idx[k]]);
    }

    for (int iter = 0; iter < max_iter; iter++) {

            // assign step
            for (int i = 0; i < n; i++) {
                double best_dist = 1e18;
                int best_k = 0;

                for (int k = 0; k < K; k++) {
                    double dist = 0.0;

                    for (int d = 0; d < dim; d++) {
                        double diff = X[i][d] - centroids[k][d];
                        dist += diff * diff;
                    }

                    if (dist < best_dist) {
                        best_dist = dist;
                        best_k = k;
                    }
                }

                labels[i] = best_k;
            }

            // update step
            std::vector<std::vector<double>> new_centroids(
                K, std::vector<double>(dim, 0.0)
            );
            std::vector<int> counts(K, 0);

            for (int i = 0; i < n; i++) {
                int k = labels[i];
                counts[k]++;

                for (int d = 0; d < dim; d++) {
                    new_centroids[k][d] += X[i][d];
                }
            }

            for (int k = 0; k < K; k++) {
                if (counts[k] > 0) {
                    for (int d = 0; d < dim; d++) {
                        new_centroids[k][d] /= counts[k];
                    }
                } else {
                    new_centroids[k] = centroids[k];
                }
            }

            // convergence check
            double shift = 0.0;

            for (int k = 0; k < K; k++) {
                for (int d = 0; d < dim; d++) {
                    double diff = centroids[k][d] - new_centroids[k][d];
                    shift += diff * diff;
                }
            }

            centroids = new_centroids;

            if (std::sqrt(shift) < tol) {
                break;
            }
        }
}
