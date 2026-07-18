#include "minibatch_kmeans_mpi.hpp"
#include "dbscan.hpp"
#include "csv_reader.hpp"
#include "normalize.hpp"

#include <mpi.h>
#include <iostream>
#include <vector>
#include <algorithm>

int main(int argc,char** argv)
{

    MPI_Init(&argc, &argv);

    int rank,size;


    MPI_Comm_rank(MPI_COMM_WORLD,&rank);

    MPI_Comm_size(MPI_COMM_WORLD,&size);

    std::vector<double> global_X;
    std::vector<std::vector<double>> data;


    int total_points=0;
    int dimension=0;
    int K=0;


    //temporary test data
    if(rank==0)
    {
        
        data=readCSV("amazon_ecommerce_1M.csv");

        normalize(data);

        total_points=data.size();
        dimension=data[0].size();

        // sampletest

        // K=10
        int sample_size=std::min(5000,(int)data.size());

        // K=30
        //int sample_size=std::min(10000,(int)data.size());

        // K=11
        //int sample_size=std::min(20000,(int)data.size());

        //Testing explosion
        //int sample_size=std::min(50000,(int)data.size());

        std::vector<std::vector<double>> sample;
        
        for(int i=0;i<sample_size;i++)
        {
            sample.push_back(data[i]);
        }

        std::vector<int> labels=MyDBSCAN(sample,1.0,5);

        //std::cout<<"Loaded "<<total_points<<" points, dimension "<<dimension<<std::endl;

        //total_points=temp.size();
        //std::vector<int> labels=MyDBSCAN(temp,5.0,2);
        std::cout<<"DBSCAN finished\n";
        for(int i=0;i<5;i++)
        {
            std::cout<<"label "<<labels[i]<<std::endl;
        }
        K=getClusterNumber(labels);

        if(K==0)
        {
            K=5;
            std::cout<<"DBSCAN failed, use default K="<<K<<std::endl;  
        }

        std::cout<< "DBSCAN found "<< K<< " clusters\n"; 


        global_X.resize(total_points*dimension);

        int index=0;

        for(int i=0;i<total_points;i++)
        {
            for(int j=0;j<dimension;j++)
            {
                global_X[index]=data[i][j];
                index++;
            }
        }
    
    }

    MPI_Bcast(&total_points, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(&dimension, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(&K,1,MPI_INT,0,MPI_COMM_WORLD);


    int local_points=total_points/size;

    std::vector<double> local_flat(local_points*dimension);

    MPI_Scatter(global_X.data(),local_points * dimension,MPI_DOUBLE,local_flat.data(),local_points * dimension,MPI_DOUBLE,0,MPI_COMM_WORLD);

    std::vector<std::vector<double>> local_X(
        local_points,
        std::vector<double>(dimension)
    );

    int index = 0;
    for(int i = 0; i < local_points; i++)
    {
        for(int d = 0; d < dimension; d++)
        {
            local_X[i][d] = local_flat[index++];
        }
    }

    std::cout << "Rank "<< rank<< " received "<< local_X.size()<< " points\n";

    MiniBatchKMeansMPI model(K,2,10,1e-4);

    model.fit(local_X);

    if(rank==0)
    {
        model.print_centroids();
    }

    MPI_Finalize();


    return 0;
}