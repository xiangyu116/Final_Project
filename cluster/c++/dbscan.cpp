#include "dbscan.hpp"

#include <iostream>
#include <vector>
#include <cmath>
#include <omp.h>

#include <set>



// Function declarations
std::vector<int> regionQuery(const Dataset& D,int P,double eps);

void growCluster(const Dataset& D,std::vector<int>& labels,int P,std::vector<int> NeighborPts,int C,double eps,int MinPts);

std::vector<int> MyDBSCAN(const Dataset& D,double eps,int MinPts);


// DBSCAN main function
std::vector<int> MyDBSCAN(const Dataset& D,double eps,int MinPts) 
{
    int n = static_cast<int>(D.size());
    std::vector<int> labels(n, 0);

    int C = 0;

    for (int P = 0; P < n; P++) 
    {
        if (labels[P] != 0) 
        {
            continue;
        }

        std::vector<int> NeighborPts = regionQuery(D, P, eps);

        if (static_cast<int>(NeighborPts.size()) < MinPts) {
            labels[P] = -1;
        }
        else 
        {
            C++;
            growCluster(D,labels,P,NeighborPts,C,eps,MinPts);
        }
    }

    return labels;
}


// Expand one cluster
void growCluster(const Dataset& D,std::vector<int>& labels,int P,std::vector<int> NeighborPts,int C,double eps,int MinPts) 
{
    // Assign the seed point to cluster C
    labels[P] = C;

    std::size_t i = 0;

    while (i < NeighborPts.size()) {

        // Get the next neighbor point
        int Pn = NeighborPts[i];

        if (labels[Pn] == -1) 
        {
            labels[Pn] = C;
        }

        else if (labels[Pn] == 0) 
        {
            labels[Pn] = C;

            std::vector<int> PnNeighborPts=regionQuery(D, Pn, eps);
            if (static_cast<int>(PnNeighborPts.size())>= MinPts)
            {
                NeighborPts.insert(NeighborPts.end(),PnNeighborPts.begin(),PnNeighborPts.end());
            }
        }
        i++;
    }
}


// omp
std::vector<int> regionQuery(const Dataset& D,int P,double eps) 
{
    std::vector<int> neighbors;

    int n = D.size();
    int dimensions =D[P].size();

    #pragma omp parallel
    {
        std::vector<int> local_neighbors;

        #pragma omp for
        for (int Pn = 0; Pn < n; Pn++) 
        {
            double squaredDistance = 0.0;

            // Calculate squared Euclidean distance
            for (int d = 0; d < dimensions; d++) 
            {
                double difference = D[P][d] - D[Pn][d];
                squaredDistance += difference * difference;
            }

            if(std::sqrt(squaredDistance) < eps)
            {
                local_neighbors.push_back(Pn);
            }
        }

        #pragma omp critical
        {
            neighbors.insert(neighbors.end(),local_neighbors.begin(),local_neighbors.end());
        }

        
    }
    return neighbors;

}








int getClusterNumber(const std::vector<int>& labels)
{
    std::set<int> clusters;
    for(int i = 0; i < labels.size(); i++)
    {
        if(labels[i]!=-1)
        {
            clusters.insert(labels[i]);
        }
    }
    return clusters.size();
}