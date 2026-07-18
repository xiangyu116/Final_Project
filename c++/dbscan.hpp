#ifndef DBSCAN_HPP
#define DBSCAN_HPP

#include <vector>

using Dataset=std::vector<std::vector<double>>;

std::vector<int> MyDBSCAN(const Dataset& D,double eps,int MinPts);

int getClusterNumber(const std::vector<int>& labels);

#endif