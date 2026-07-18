#ifndef KMEANS_HPP
#define KMEANS_HPP

#include <vector>

class KMeans
{
private:
    int K;
    int max_iter;
    double tol;

public:
    std::vector<std::vector<double>> centroids;
    std::vector<int> labels;

    KMeans(int K, int max_iter = 100, double tol = 1e-6);

    void fit(const std::vector<std::vector<double>>& X);

};

#endif