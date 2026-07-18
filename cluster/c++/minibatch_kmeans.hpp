#ifndef MINIBATCH_KMEANS_HPP
#define MINIBATCH_KMEANS_HPP 

#include <vector>
class MiniBatchKMeans 
{ 
   public:
    std::vector<std::vector<double>> centroids;
    std::vector<int> labels;

    MiniBatchKMeans(int K, int batch_size, int max_iter, double tol);

    void fit(const std::vector<std::vector<double>>& X);

    void print_result() const;

    private:
     int K;
     int batch_size;
     int max_iter;
     double tol;

     double calculate_distance(const std::vector<double>& point, const std::vector<double>& centroid)const;

     int find_closest_centroid(const std::vector<double>& point)const;
};







#endif