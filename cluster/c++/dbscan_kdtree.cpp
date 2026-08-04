#include "dbscan_kdtree.hpp"
#include "kdtree.hpp"

#include <vector>
#include <set>

KDTree* kd_tree=nullptr;

std::vector<int> regionQuery(const Dataset& D,int P,double eps)
{
    return kd_tree->radiusSearch(D[P],eps);
}

void growCluster(const Dataset& D,std::vector<int>& labels,int P,std::vector<int> neighbors, int C,double eps, int MinPts)
{
    labels[P]=C;

    std::size_t i=0;

    while(i<neighbors.size())
    {
        int point=neighbors[i];
        if(labels[point]==-1)
        {
            labels[point]=C;
        }
        else if(labels[point]==0)
        {
            labels[point]=C;
            std::vector<int> pointNeighbors=regionQuery(D, point,eps);
            if(pointNeighbors.size()>=MinPts)
            {
                neighbors.insert(neighbors.end(),pointNeighbors.begin(),pointNeighbors.end());
            }
        }
        i++;
    }
}



std::vector<int> MyDBSCAN(const Dataset& D,double eps,int MinPts)
{
    if(kd_tree==nullptr)
    {
        kd_tree=new KDTree(D);
    }

    int n=D.size();
    std::vector<int> labels(n,0);
    int cluster=0;

    for(int i=0;i<n;i++)
    {

        if(labels[i]!=0)
        {
            continue;
        }

        std::vector<int> neighbors=regionQuery(D,i,eps);

        if(neighbors.size()<MinPts)
        {
            labels[i]=-1;
        }
        else
        {
            cluster++;
            growCluster(D,labels,i,neighbors,cluster,eps,MinPts);
        }
    }

    return labels;
}




int getClusterNumber(const std::vector<int>& labels)
{
    std::set<int> clusters;
    for(int i=0;i<labels.size();i++)
    {
        if(labels[i]!=-1)
        {
            clusters.insert(labels[i]);
        }
    }
    return clusters.size();

}