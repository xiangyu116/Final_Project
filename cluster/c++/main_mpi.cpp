#include "minibatch_kmeans_mpi.hpp"
#include "dbscan.hpp"
#include "csv_reader.hpp"
#include "normalize.hpp"

#include <algorithm>
#include <iomanip>
#include <iostream>
#include <mpi.h>
#include <sstream>
#include <vector>

int main(int argc,char** argv)
{

    MPI_Init(&argc, &argv);

    int rank,size;


    MPI_Comm_rank(MPI_COMM_WORLD,&rank);

    MPI_Comm_size(MPI_COMM_WORLD,&size);

    std::vector<std::vector<double>> data;
    int K=0;

    if(rank==0)
    {

        data = readCSV("data/amazon_ecommerce_1M.csv");

        normalize(data);

        // sampletest

        // K=10
        int sample_size=std::min(5000,(int)data.size());

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

        std::cout << "DBSCAN found " << K << " clusters\n";
        data.clear();
        data.shrink_to_fit();
    }

    MPI_Bcast(&K, 1, MPI_INT, 0, MPI_COMM_WORLD);

    double start_time = MPI_Wtime();

    std::vector<double> global_mean;
    std::vector<double> global_std;

    // MiniBatchKMeansMPI model(K, 10000, 1, 1e-4);

    int total_files = 8;
    for (int batch = 1; batch <= 10; batch++) {
        // std::ostringstream batch_name;
        // batch_name << "data/generated_batches/batch_" << std::setw(3)
        //            << std::setfill('0') << batch << "/generated_rank_" <<
        //            rank
        //            << ".csv";
        // std::string filename = batch_name.str();
        // std::vector<std::vector<double>> local_X;
        // local_X = readCSV(filename);
        std::vector<std::vector<double>> local_X;
        int files_per_rank = total_files / size;
        int start_file = rank * files_per_rank;
        int end_file = start_file + files_per_rank;

        for (int r = start_file; r < end_file; r++) {
            std::ostringstream batch_name;
            batch_name << "data/generated_batches/batch_" << std::setw(3)
                       << std::setfill('0') << batch << "/generated_rank_" << r
                       << ".csv";

            std::string filename = batch_name.str();
            auto temp = readCSV(filename);
            local_X.insert(local_X.end(), temp.begin(), temp.end());
        }

        if (local_X.empty()) {
            std::cout << "Rank " << rank << " failed loading batch " << batch << std::endl;
            continue;
        }
        // if(batch == 1 && rank == 0)
        // {
        //     global_mean = computeMean(local_X);
        //     global_std = computeStd(local_X,global_mean);
        // }

        // int dim=8;
        // if(rank!=0)
        // {
        //     global_mean.resize(dim);
        //     global_std.resize(dim);
        // }

        // MPI_Bcast(global_mean.data(),dim,MPI_DOUBLE,0,MPI_COMM_WORLD);
        // MPI_Bcast(global_std.data(),dim,MPI_DOUBLE,0,MPI_COMM_WORLD);

        // normalize(local_X);
        normalizeWithStats(local_X,global_mean,global_std);

        std::cout << "Rank " << rank << " processing batch " << batch
                  << " size " << local_X.size() << std::endl;
        model.partial_fit(local_X);
        local_X.clear();
    }



    if(rank==0)
    {
        model.print_centroids();
        double end_time = MPI_Wtime();
        std::cout << "Time: " << end_time - start_time << " seconds"
                  << std::endl;
    }

    MPI_Finalize();


    return 0;
}