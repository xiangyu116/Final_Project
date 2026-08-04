#include <iostream>
#include <vector>
#include <fstream>

#include "csv_reader.hpp"
#include "dbscan.hpp"


int main()
{

    //Dataset data =readBlobCSV("blobs_test.csv");
    Dataset data =readCovtypeCSV("covtype_test.csv");
    std::cout<<"Loaded data size: "<<data.size()<<std::endl;

    std::cout<<"Dimension: "<<data[0].size()<<std::endl;


    //blobs
    //double eps = 3.0;
    //int MinPts = 5;

    double eps = 50.0;
    int MinPts = 10;
    std::vector<int> labels =MyDBSCAN(data,eps,MinPts);


    std::cout<<"DBSCAN finished\n";


    for(int i=0;i<20;i++)
    {
        std::cout<<"Point "<<i<<" -> Cluster "<<labels[i]<<std::endl;
    }


    std::cout<<"Cluster number: "<<getClusterNumber(labels)<<std::endl;

    
    std::ofstream output("dbscan_result.csv");


    output<<"cluster\n";


    for(int label : labels)
    {
        output<<label<<"\n";
    }


    output.close();


    std::cout<<"Saved dbscan_result.csv\n";


return 0;





}