#include "minibatch_kmeans.hpp"

#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include <string>

// int main()
// {
//     // Simple test dataset
//     std::vector<std::vector<double>> X =
//     {
//         {1.0, 1.0},
//         {1.2, 1.1},
//         {0.9, 1.0},

//         {5.0, 5.0},
//         {5.2, 5.1},
//         {4.9, 4.8},

//         {10.0, 10.0},
//         {10.2, 9.9},
//         {9.8, 10.1}
//     };

//     // Create Mini-Batch K-Means
//     MiniBatchKMeans model(
//         3,      // K
//         3,      // batch size
//         100,    // max iterations
//         1e-4    // tolerance
//     );

//     // Train
//     model.fit(X);

//     // Print results
//     model.print_result();

//     return 0;
// }

std::vector<std::vector<double>> read_csv(
    const std::string& filename
)
{
    std::ifstream file(filename);

    if (!file.is_open())
    {
        throw std::runtime_error(
            "Cannot open file"
        );
    }


    std::vector<std::vector<double>> data;

    std::string line;


    // skip header
    std::getline(file, line);


    while (std::getline(file, line))
    {
        std::stringstream ss(line);

        std::string value;

        std::vector<double> row;


        while (std::getline(ss, value, ','))
        {
            try
            {
                row.push_back(
                    std::stod(value)
                );
            }
            catch(...)
            {

            }
        }


        if (!row.empty())
        {
            data.push_back(row);
        }
    }


    return data;
}

int main()
{
    std::vector<std::vector<double>> X = read_csv("generated_v3_data.csv");


    std::cout<< "Data size: "<< X.size()<< std::endl;

    std::cout<< "Dimension: "<< X[0].size()<< std::endl;

    return 0;
}