#include "csv_reader.hpp"

#include <fstream>
#include <sstream>
#include <iostream>


std::vector<std::vector<double>> readCSV(const std::string& filename)
{
    std::vector<std::vector<double>> data;

    std::ifstream file(filename);

    if(!file.is_open())
    {
        std::cout<<"Cannot open file\n";
        return data;
    }


    std::string line;


    getline(file,line); // skip header


    while(getline(file,line))
    {
        std::stringstream ss(line);

        std::string value;

        std::vector<double> row;


        int column = 0;


        while(getline(ss,value,','))
        {

            // Skip user_id
            if(column == 5 ||   // price
               column == 6 ||   // discount
               column == 7 ||   // final_price
               column == 8 ||   // rating
               column == 9 ||   // review_count
               column == 10 ||  // stock
               column == 12 ||  // seller_rating
               column == 14     // shipping_time_days
            ) 
            {
              row.push_back(std::stod(value));
            }
            else if(column==18)
            {
              if(value=="true")
              {
                row.push_back(1);
              }
              else
              {
                row.push_back(0);
              }
  
            }

            column++;
        }


        data.push_back(row);
    }


    return data;
}