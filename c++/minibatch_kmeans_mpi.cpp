#include "minibatch_kmeans_mpi.hpp"

#include <mpi.h>
#include <iostream>
#include <cmath>
#include <random>
#include <algorithm>
#include <limits>


MiniBatchKMeansMPI::MiniBatchKMeansMPI(int K,int batch_size,int max_iter,double tol)
      :K(K),batch_size(batch_size),max_iter(max_iter),tol(tol)
      {

      }



double MiniBatchKMeansMPI::calculate_distance(const std::vector<double>& point,const std::vector<double>& centroid)
{
    double distance = 0.0;

    for (int d = 0;d < static_cast<int>(point.size());d++)
    {
        double difference=point[d]-centroid[d];

        distance += difference * difference;
    }

    return distance;
}



int MiniBatchKMeansMPI::find_closest_centroid(const std::vector<double>& point)
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





void MiniBatchKMeansMPI::fit(std::vector<std::vector<double>>& local_X)
{

    int rank,size;

    MPI_Comm_rank(MPI_COMM_WORLD,&rank);
    MPI_Comm_size(MPI_COMM_WORLD,&size);

    int dim =local_X[0].size();

    /*
        Step 1:
        Rank 0 initialize centroids
    */

    if(rank==0)
    {

        centroids.clear();
        std::vector<int> selected(K);

        for(int k=0;k<K;k++)
        {
            selected[k]=k%local_X.size();
        }

        for(int k=0;k<K;k++)
        {
            centroids.push_back(local_X[selected[k]]);
        }

    }


    else
    {
        centroids.resize(K);
        for(int k=0;k<K;k++)
        {
            centroids[k].resize(dim);
        }

    }

    /*
        Broadcast initial centroids
    */

    for(int k=0;k<K;k++)
    {
        MPI_Bcast(centroids[k].data(),dim,MPI_DOUBLE,0,MPI_COMM_WORLD);
    }

    std::vector<int> update_count(K,0);

    for(int iter=0;iter<max_iter;iter++)
    {
        std::vector<double> local_sum(K*dim,0.0);
        std::vector<int> local_count(K,0);
        int batch =std::min(batch_size,(int)local_X.size());
        for(int i=0;i<batch;i++)
        {
            int cluster =find_closest_centroid(local_X[i]);
            local_count[cluster]++;
            for(int d=0;d<dim;d++)
            {
                local_sum[cluster*dim+d]+= local_X[i][d];
            }
        }

        /*
            Combine all MPI processes
        */


        std::vector<double> global_sum(K*dim,0.0);

        std::vector<int> global_count(K,0);

        MPI_Allreduce(local_sum.data(),global_sum.data(),K*dim,MPI_DOUBLE,MPI_SUM,MPI_COMM_WORLD);

        MPI_Allreduce(local_count.data(),global_count.data(),K,MPI_INT,MPI_SUM,MPI_COMM_WORLD);

        /*
            Update centroid
        */
        for(int k=0;k<K;k++)
        {
            if(global_count[k]>0)
            {
                for(int d=0;d<dim;d++)
                {
                    centroids[k][d]=global_sum[k*dim+d]/global_count[k];
                }

            }

        }



        if(rank==0)
        {
            std::cout<<"Iteration "<<iter+1<<" finished\n";
        }


    }


}


void MiniBatchKMeansMPI::print_centroids()
{
    for(int k=0;k<K;k++)
    {
        std::cout<<"Cluster "<<k<<": ";

        for(double x: centroids[k])
        {
            std::cout<<x<<" ";
        }

        std::cout<<std::endl;
    }
}