#ifndef CSV_READER_HPP
#define CSV_READER_HPP

#include <vector>
#include <string>

// Read Amazon dataset
std::vector<std::vector<double>> readCSV(const std::string& filename);

// Read sklearn make_blobs dataset
std::vector<std::vector<double>> readBlobCSV(const std::string &filename);
#endif

// read covtypeCSV
std::vector<std::vector<double>> readCovtypeCSV(const std::string &filename);