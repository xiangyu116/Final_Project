#ifndef NORMALIZE_HPP
#define NORMALIZE_HPP

#include <vector>
// original code
// void normalize(std::vector<std::vector<double>>& data);

//update
std::vector<double> computeMean(const std::vector<std::vector<double>> &data);
std::vector<double> computeStd(const std::vector<std::vector<double>>& data,const std::vector<double>& mean);

void normalizeWithStats(std::vector<std::vector<double>>& data,const std::vector<double>& mean,const std::vector<double>& stddev);



#endif