#include "dbscan.hpp"
#include "csv_reader.hpp"
#include "normalize.hpp"

#include <iostream>
#include <vector>
#include <random>
#include <algorithm>
#include <chrono>

int main()
{
    std::cout<<"Loading data..."<<std::endl;
    std::vector<std::vector<double>> data;
    data=readCSV("data/generated_batches/batch_001/generated_rank_0.csv");


    if(data.empty())
    {
        std::cout<<"Cannot load data"<<std::endl;
        return -1;
    }

    std::cout<<"Original size: "<<data.size()<<std::endl;

    std::vector<double> mean=computeMean(data);

    std::vector<double> stddev=computeStd(data,mean);

    normalizeWithStats(data, mean,stddev);
    std::cout<<"Data normalization finished"<<std::endl;

    int sample_size=std::min(50000,(int)data.size());
    std::shuffle(data.begin(),data.end(),std::mt19937(42));

    std::vector<std::vector<double>> sample;

    for(int i=0;i<sample_size;i++)
    {
        sample.push_back(data[i]);
    }

    std::cout<<"Sample size: "<<sample.size()<<std::endl;
    auto start=std::chrono::high_resolution_clock::now();
    std::vector<int> labels=
    MyDBSCAN(sample,1.0,5);

    auto end=std::chrono::high_resolution_clock::now();
    double time=std::chrono::duration<double>(end-start).count();
    std::cout<<"DBSCAN finished"<<std::endl;

    for(int i=0;i<5;i++)
    {
        std::cout<<"label "<<labels[i]<<std::endl;
    }

    int K=getClusterNumber(labels);

    std::cout<<"Original DBSCAN found " <<K<<" clusters"<<std::endl;
    std::cout<<"DBSCAN time: "<<time<<" seconds"<<std::endl;

    return 0;
}