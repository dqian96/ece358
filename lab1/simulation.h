#ifndef SIMULATION_H
#define SIMULATION_H

#include "queue.h"
#include "utils.h"

#include <algorithm>
#include <memory>
#include <iostream>
#include <vector>

struct PerformanceMetrics {
    double pIdle = 0;
    double pLoss = 0;
    double averageQSize = 0;
};

PerformanceMetrics simulateMM1Queue(double alpha, double L, double lambda, double C, double T);
PerformanceMetrics simulateMM1KQueue(double alpha, double L, double lambda,
                                    double C, double T, int K);

#endif  // SIMULATION_H
