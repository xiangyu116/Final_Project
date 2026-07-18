#include "dbscan.hpp"

#include <iostream>
#include <vector>
#include <cmath>

#include <set>



// Function declarations
std::vector<int> regionQuery(const Dataset& D,int P,double eps);

void growCluster(const Dataset& D,std::vector<int>& labels,int P,std::vector<int> NeighborPts,int C,double eps,int MinPts);

std::vector<int> MyDBSCAN(const Dataset& D,double eps,int MinPts);


// DBSCAN main function
std::vector<int> MyDBSCAN(const Dataset& D,double eps,int MinPts) 
{
    int n = static_cast<int>(D.size());

    /*
     * labels:
     *  0  means the point has not been visited.
     * -1  means the point is noise.
     *  1, 2, 3... are cluster IDs.
     */
    std::vector<int> labels(n, 0);

    // Current cluster ID
    int C = 0;

    // Visit every point in the dataset
    for (int P = 0; P < n; P++) {

        // Skip this point if it has already been processed
        if (labels[P] != 0) {
            continue;
        }

        // Find all neighbors of point P
        std::vector<int> NeighborPts = regionQuery(D, P, eps);

        // If there are not enough neighbors, mark P as noise
        if (static_cast<int>(NeighborPts.size()) < MinPts) {
            labels[P] = -1;
        }
        else {
            // Create a new cluster
            C++;

            // Expand the new cluster
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

    /*
     * NeighborPts is used as a queue.
     * New neighboring points can be appended to this vector.
     */
    std::size_t i = 0;

    while (i < NeighborPts.size()) {

        // Get the next neighbor point
        int Pn = NeighborPts[i];

        /*
         * If this point was previously marked as noise,
         * it can still become a boundary point of this cluster.
         */
        if (labels[Pn] == -1) 
        {
            labels[Pn] = C;
        }

        /*
         * If this point has not been visited,
         * add it to the current cluster.
         */
        else if (labels[Pn] == 0) 
        {
            labels[Pn] = C;

            // Find the neighbors of Pn
            std::vector<int> PnNeighborPts=regionQuery(D, Pn, eps);

            /*
             * If Pn has enough neighbors, it is a core point.
             * Add all its neighbors to the search queue.
             */
            if (
                static_cast<int>(PnNeighborPts.size())>= MinPts
            ) {
                NeighborPts.insert(NeighborPts.end(),PnNeighborPts.begin(),PnNeighborPts.end());
            }
        }

        // Move to the next point in the queue
        i++;
    }
}


// Find all points within eps of point P
std::vector<int> regionQuery(const Dataset& D,int P,double eps) 
{
    std::vector<int> neighbors;

    int n = static_cast<int>(D.size());
    int dimensions = static_cast<int>(D[P].size());

    // Compare point P with every point Pn
    for (int Pn = 0; Pn < n; Pn++) {

        double squaredDistance = 0.0;

        // Calculate squared Euclidean distance
        for (int d = 0; d < dimensions; d++) 
        {
            double difference = D[P][d] - D[Pn][d];
            squaredDistance += difference * difference;
        }

        // Euclidean distance
        double distance = std::sqrt(squaredDistance);

        // Add Pn if it is inside the eps neighborhood
        if (distance < eps) 
        {
            neighbors.push_back(Pn);
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