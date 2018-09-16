#ifndef UTILS_H
#define UTILS_H

#include <math.h>

#include <cstdlib>
#include <vector>

double genExpRand(double lambda);

std::shared_ptr<std::vector<double>> genPoissionDistr(double lambda, int T);
std::shared_ptr<std::vector<double>> genExpDistr(double lambda, int T);

#endif  // UTILS_H
