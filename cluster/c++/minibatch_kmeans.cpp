#include "minibatch_kmeans.hpp"

#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <random>
#include <limits>
#include <stdexcept>

MiniBatchKMeans::MiniBatchKMeans(int K,int batch_size,int max_iter,double tol)
    : K(K),batch_size(batch_size),max_iter(max_iter),tol(tol)
{
}

double MiniBatchKMeans::calculate_distance(const std::vector<double>& point,const std::vector<double>& centroid) const
{
    double distance = 0.0;

    for (int d = 0;d < static_cast<int>(point.size());d++)
    {
        double difference=point[d]-centroid[d];

        distance += difference * difference;
    }

    return distance;
}

int MiniBatchKMeans::find_closest_centroid(const std::vector<double>& point) const
{
    double best_distance =std::numeric_limits<double>::max();

    int best_cluster = 0;

    for (int k = 0; k < K; k++)
    {
        double distance=calculate_distance(point,centroids[k]);
        if (distance<best_distance)
        {
            best_distance=distance;
            best_cluster=k;
        }
    }

    return best_cluster;
}

void MiniBatchKMeans::fit(const std::vector<std::vector<double>>& X)
{
    if (X.empty())
    {
        throw std::invalid_argument(
            "The dataset is empty."
        );
    }

    int n=static_cast<int>(X.size());

    int dim=static_cast<int>(X[0].size());

    if (K<=0)
    {
        throw std::invalid_argument(
            "K must be greater than zero."
        );
    }

    if (K>n)
    {
        throw std::invalid_argument(
            "K cannot be larger than the dataset size."
        );
    }

    if (batch_size<=0)
    {
        throw std::invalid_argument(
            "Batch size must be greater than zero."
        );
    }

    std::vector<int> indices(n);

    for (int i=0; i<n; i++)
    {
        indices[i]=i;
    }

    std::mt19937 generator(42);

    std::shuffle(indices.begin(),indices.end(),generator);

    centroids.clear();

    for (int k = 0; k < K; k++)
    {
        centroids.push_back(X[indices[k]]);
    }

    std::vector<int> update_counts(K,0);

    int actual_batch_size = std::min(batch_size, n);

    //Set threshold
    int stable_iterations = 0;
    
    
    const int required_stable_iterations = 5;
    for (int iter = 0;iter < max_iter;iter++)
    {
        std::shuffle(indices.begin(),indices.end(),generator);

        std::vector<std::vector<double>>
            old_centroids = centroids;

        for (int b = 0; b < actual_batch_size;b++)
        {
            int point_index =indices[b];

            int cluster = find_closest_centroid(X[point_index]);

            update_counts[cluster]++;

            double learning_rate =1.0 / static_cast<double>(update_counts[cluster]);

            for (int d = 0;d < dim;d++)
            {
                centroids[cluster][d] +=learning_rate*(X[point_index][d] - centroids[cluster][d]);
            }
        }

        double shift = 0.0;

        for (int k = 0;k < K;k++)
        {
            for (int d = 0;d < dim;d++)
            {
                double difference =old_centroids[k][d]-centroids[k][d];
                shift +=difference * difference;
            }
        }

        shift = std::sqrt(shift);

        std::cout<< "Iteration "<< iter + 1<< ", shift = "<< shift<< "\n";

        
        
        if(shift<tol)
        {
            stable_iterations++;
        }
        else
        {
            stable_iterations = 0;
        }

        if (stable_iterations >= required_stable_iterations)
        {
            std::cout<< "Mini-Batch K-Means converged.\n";
            break;
        }

    }

    labels.resize(n);

    for (int i = 0;i < n;i++)
    {
        labels[i] =find_closest_centroid(X[i]);
    }
    for (const auto& point : X)
    {
        if (static_cast<int>(point.size())!=dim)
        {
            throw std::invalid_argument(
                "All data points must have the same dimension."
            );
        }
    }
}

void MiniBatchKMeans::print_result() const
{
    std::cout<< "\nMini-Batch K-Means Centroids:\n";

    for (int k = 0;k < static_cast<int>(centroids.size());k++)
    {
        std::cout<< "Cluster "<< k<< ": ";

        for (double value : centroids[k])
        {
            std::cout<< value<< " ";
        }

        std::cout << "\n";
    }

    std::cout << "\nLabels:\n";

    for (int i = 0;i < static_cast<int>(labels.size());i++)
    {
        std::cout<< "Point "<< i << " -> Cluster " << labels[i]<< "\n";
    }
}