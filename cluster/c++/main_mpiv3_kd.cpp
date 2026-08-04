#include "minibatch_kmeans_mpi.hpp"
#include "dbscan_kdtree.hpp"
#include "csv_reader.hpp"
#include "normalize.hpp"

#include <algorithm>
#include <iomanip>
#include <iostream>
#include <mpi.h>
#include <sstream>
#include <vector>
#include <cmath>
#include <random>

int main(int argc,char** argv)
{
    MPI_Init(&argc,&argv);
    double total_start=MPI_Wtime();

    int rank,size;
    MPI_Comm_rank(MPI_COMM_WORLD,&rank);
    MPI_Comm_size(MPI_COMM_WORLD,&size);

    std::vector<std::vector<double>> data;
    int K=0;

    if(rank==0)
    {
        std::cout<<"Loading generated data for DBSCAN..."<<std::endl;
        for(int r=0;r<8;r++)
        {
            std::ostringstream filename;
            filename<<"data/generated_batches/batch_001/generated_rank_"<<r<<".csv";
            auto temp=readCSV(filename.str());
            data.insert(data.end(),temp.begin(),temp.end());
        }
        std::cout<<"DBSCAN data size: "<<data.size()<<std::endl;
        std::vector<double> mean=computeMean(data);
        std::vector<double> stddev=computeStd(data,mean);

        normalizeWithStats(data,mean,stddev);
        int sample_size=std::min(50000,(int)data.size());
        std::shuffle(data.begin(), data.end(),std::mt19937(42));

        std::vector<std::vector<double>> sample;
        for(int i=0;i<sample_size;i++)
        {
            sample.push_back(data[i]);
        }

        std::cout<<"DBSCAN sample size: "<<sample.size()<<std::endl;
        double dbscan_start=MPI_Wtime();
        std::vector<int> labels=MyDBSCAN(sample,1.0,5);

        double dbscan_end=MPI_Wtime();

        std::cout<<"DBSCAN finished\n";

        std::cout<<"DBSCAN time: "<<dbscan_end-dbscan_start<<" seconds"<<std::endl;

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

        std::cout<<"DBSCAN found "<<K<<" clusters\n";

        data.clear();
        data.shrink_to_fit();
      
    }

    MPI_Bcast(&K,1,MPI_INT,0,MPI_COMM_WORLD);

    double kmeans_start=MPI_Wtime();

    int dim=0;
    if(rank==0)
    {
        auto temp=readCSV("data/generated_batches/batch_001/generated_rank_0.csv");
        if(!temp.empty())
        {
            dim=temp[0].size();
        }
    }
    MPI_Bcast(&dim,1,MPI_INT,0,MPI_COMM_WORLD);

    int total_files=8;

    std::vector<double> global_mean(dim);
    std::vector<double> global_std(dim);

    std::vector<double> local_sum(dim,0.0);
    std::vector<double> local_sq_sum(dim,0.0);

    double local_count=0;


    int files_per_rank=total_files/size;
    int start_file=rank*files_per_rank;
    int end_file=start_file+files_per_rank;


    for(int r=start_file;r<end_file;r++)
    {
        std::ostringstream filename;

        filename<<"data/generated_batches/batch_001/generated_rank_"<<r<<".csv";

        auto temp=readCSV(filename.str());

        for(auto &row:temp)
        {
            for(int j=0;j<dim;j++)
            {
                local_sum[j]+=row[j];
                local_sq_sum[j]+=row[j]*row[j];
            }

            local_count++;
        }
    }


    std::vector<double> global_sum(dim,0.0);
    std::vector<double> global_sq_sum(dim,0.0);

    double global_count=0;

    MPI_Allreduce(local_sum.data(),global_sum.data(),dim, MPI_DOUBLE,MPI_SUM,MPI_COMM_WORLD);
    MPI_Allreduce(local_sq_sum.data(), global_sq_sum.data(),dim,MPI_DOUBLE,MPI_SUM, MPI_COMM_WORLD);
    MPI_Allreduce(&local_count, &global_count, 1,MPI_DOUBLE, MPI_SUM,MPI_COMM_WORLD);

    for(int i=0;i<dim;i++)
    {
        global_mean[i]=global_sum[i]/global_count;

        global_std[i]=sqrt(
            global_sq_sum[i]/global_count-
            global_mean[i]*global_mean[i]
        );
    }


    if(rank==0)
    {
        std::cout<<"Global normalization finished\n";
    }
    MiniBatchKMeansMPI model(K,10000,1,1e-4);


    for(int batch=1;batch<=10;batch++)
    {
        std::vector<std::vector<double>> local_X;

        files_per_rank=total_files/size;

        start_file=rank*files_per_rank;
        end_file=start_file+files_per_rank;


        for(int r=start_file;r<end_file;r++)
        {
            std::ostringstream filename;

            filename<<"data/generated_batches/batch_" <<std::setw(3)<<std::setfill('0')<<batch<<"/generated_rank_"<<r<<".csv";

            auto temp=readCSV(filename.str());
            local_X.insert(local_X.end(),temp.begin(),temp.end());
        }

        if(local_X.empty())
        {
            std::cout<<"Rank "<<rank<<" failed loading batch "<<batch<<std::endl;
            continue;
        }

        normalizeWithStats(local_X,global_mean,global_std);
        std::cout<<"Rank "<<rank<<" processing batch "<<batch<<" size "<<local_X.size()<<std::endl;
        model.partial_fit(local_X);

        local_X.clear();
    }

    if(rank==0)
    {
        model.print_centroids();
        double kmeans_end=MPI_Wtime();
        std::cout<<"MiniBatch Kmeans time: "<<kmeans_end-kmeans_start<<" seconds"<<std::endl;
    }

    double total_end=MPI_Wtime();
    if(rank==0)
    {
        std::cout<<"Total pipeline time: "<<total_end-total_start<<" seconds"<<std::endl;
    }

    MPI_Finalize();

    return 0;
}