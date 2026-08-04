#include "normalize.hpp"

#include <cmath>
#include <iostream>

// origin
//  void normalize(std::vector<std::vector<double>>& data)
//  {
//      int rows = data.size();

//     if(rows == 0)
//         return;

//     int cols = data[0].size();

//     std::vector<double> mean(cols,0.0);
//     std::vector<double> stddev(cols,0.0);

//     // calculate mean of each feature
//     for(int i=0;i<rows;i++)
//     {
//         for(int j=0;j<cols;j++)
//         {
//             mean[j] += data[i][j];
//         }
//     }

//     for(int j=0;j<cols;j++)
//     {
//         mean[j] /= rows;
//     }

//     // calculate standard deviation
//     for(int i=0;i<rows;i++)
//     {
//         for(int j=0;j<cols;j++)
//         {
//             double diff=data[i][j]-mean[j];
//             stddev[j]+=diff*diff;
//         }
//     }

//     for(int j=0;j<cols;j++)
//     {
//         stddev[j]=sqrt(stddev[j]/rows);
//     }

//     // standardization
//     for(int i=0;i<rows;i++)
//     {
//         for(int j=0;j<cols;j++)
//         {
//             if(stddev[j] != 0)
//             {
//                 data[i][j]=(data[i][j]-mean[j])/stddev[j];
//             }
//         }
//     }

//     std::cout<< "Data normalization finished"<< std::endl;
// }

// update
std::vector<double> computeMean(const std::vector<std::vector<double>> &data) {
    int rows = data.size();

    if (rows == 0)
        return {};

    int cols = data[0].size();
    std::vector<double> mean(cols, 0.0);
    for (int i = 0; i < rows; i++) 
    {
        for (int j = 0; j < cols; j++) 
        {
            mean[j] += data[i][j];
        }
    }

    for (int j = 0; j < cols; j++) {
        mean[j] /= rows;
    }

    return mean;
}




std::vector<double> computeStd(const std::vector<std::vector<double>>& data,const std::vector<double>& mean)
{
    int rows=data.size();

    int cols=data[0].size();

    std::vector<double> stddev(cols,0.0);
    for(int i=0;i<rows;i++)
    {
        for(int j=0;j<cols;j++)
        {
            double diff=data[i][j]-mean[j];

            stddev[j]+=diff*diff;
        }
    }

    for(int j=0;j<cols;j++)
    {
        stddev[j]=sqrt(stddev[j]/rows);
    }

    return stddev;
}



void normalizeWithStats(std::vector<std::vector<double>>& data,const std::vector<double>& mean,const std::vector<double>& stddev)
{

    int rows=data.size();
    if(rows==0)
        return;


    int cols=data[0].size();

    for(int i=0;i<rows;i++)
    {
        for(int j=0;j<cols;j++)
        {
            if(stddev[j]!=0)
            {
                data[i][j]=(data[i][j]-mean[j])/stddev[j];
            }
        }
    }


    std::cout<<"Data normalization finished"<<std::endl;
}