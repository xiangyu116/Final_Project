#ifndef MINIBATCH_KMEANS_MPI_HPP
#define MINIBATCH_KMEANS_MPI_HPP

#include <vector>


class MiniBatchKMeansMPI
{

public:

    MiniBatchKMeansMPI(int K,int batch_size,int max_iter,double tol);


    void fit(std::vector<std::vector<double>>& local_X);

    void print_centroids();


private:

    int K;
    int batch_size;
    int max_iter;
    double tol;


    std::vector<std::vector<double>> centroids;


    double calculate_distance(const std::vector<double>& a,const std::vector<double>& b);


    int find_closest_centroid(const std::vector<double>& point);

};

#endif