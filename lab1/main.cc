#include <assert.h>
#include "simulation.h"
#include "utils.h"

#include <fstream>
#include <iostream>

using namespace std;

const double T = 10;       // simulate for 10 seconds
const double ALPHA = 100;  // observation rate

void validateExpGen() {
    int lambda = 75, numIterations = 1000;

    int distr[numIterations];
    double sum = 0;

    for (int i = 0; i < numIterations; i++) {
        double genValue = genExpRand(75);

        distr[i] = genValue;
        sum += genValue;
    }

    double mean = sum/numIterations;
    double variance = 0;

    for (int i = 0; i < numIterations; i++) {
        variance += pow((distr[i] - mean), 2);
    }

    variance = variance / numIterations;

    cout << "Mean of distirbution : " << mean << endl;
    cout << "Variance of distirbution : " << variance << endl;

    double expectedMean = 1.0 / lambda;
    double expectedVariance = 1.0 / pow(lambda, 2);

    assert(abs(mean - expectedMean) < 0.01);
    assert(abs(variance - expectedVariance) < 0.01);
}


void testMM1QueueUtilization(double alpha, double T) {
    double L = 12000;
    double C = 1000000;

    ofstream mm1AvgQueueSizeData("mm1AvgQueueSize.csv");
    ofstream mm1PIdleData("mm1P1Idle.csv");

    cout << '\n' << "Question 3: " << endl;
    cout << "rho" << " | " << "E[n]" << " | " << "PIdle" << endl;

    for (double utilization = 0.26; utilization < 0.95; utilization += 0.1) {
        double lambda = (utilization * C) / L;

        auto metrics = simulateMM1Queue(alpha, L, lambda, C, T);

        cout << utilization << " | " << metrics.averageQSize << " | " << metrics.pIdle << endl;

        mm1AvgQueueSizeData << utilization << ", " << metrics.averageQSize << endl;
        mm1PIdleData << utilization << ", " << metrics.pIdle << endl;
    }

    cout << endl;

    mm1AvgQueueSizeData.close();
    mm1PIdleData.close();
}

void testMM1QueueHighUtlization(double alpha, double T) {
    double L = 12000;
    double C = 1000000;

    double utilization = 1.2;
    double lambda = (utilization * C) / L;

    cout << '\n' << "Question 4: " << endl;
    auto metrics = simulateMM1Queue(alpha, L, lambda, C, T);

    cout
        << "rho=" << utilization
        << ", E[N]=" << metrics.averageQSize
        << ", PIdle=" << metrics.pIdle << endl;

    cout << endl;
}


void testMM1KQueueUtilization(double alpha, double T) {
    double L = 12000;
    double C = 1000000;

    ofstream mm1KAvgQueueSizeData("mm1KAvgQueueSize.csv");
    ofstream mm1KPLossData("mm1KPLoss.csv");

    cout << '\n' << "Question 6: " << endl;

    cout << "\nE[n]" << endl;
    cout << "rho" << " | " << "K=1" << " | " << "K=10" <<  " | " << "K=40" << "K=inf" << endl;

    for (double utilization = 0.6; utilization < 1.5; utilization += 0.1) {
        double lambda = (utilization * C) / L;

        auto metricsK5 = simulateMM1KQueue(alpha, L, lambda, C, T, 5);
        auto metricsK10 = simulateMM1KQueue(alpha, L, lambda, C, T, 10);
        auto metricsK40 = simulateMM1KQueue(alpha, L, lambda, C, T, 40);
        auto metricsKInf = simulateMM1KQueue(alpha, L, lambda, C, T, -1);

        cout << utilization
            << " | " << metricsK5.averageQSize
            << " | " << metricsK10.averageQSize
            << " | " << metricsK40.averageQSize
            << " | " << metricsKInf.averageQSize
            << endl;

        mm1KAvgQueueSizeData << utilization
            << ", " << metricsK5.averageQSize
            << ", " << metricsK10.averageQSize
            << ", " << metricsK40.averageQSize
            << ", " << metricsKInf.averageQSize
            << endl;
    }

    cout << "\nPLoss" << endl;
    cout << "rho" << " | " << "K=1" << " | " << "K=10" <<  " | " << "K=40" << endl;

    double utilization = 0.5;
    while (utilization < 10) {
        double lambda = (utilization * C) / L;

        auto metricsK5 = simulateMM1KQueue(alpha, L, lambda, C, T, 5);
        auto metricsK10 = simulateMM1KQueue(alpha, L, lambda, C, T, 10);
        auto metricsK40 = simulateMM1KQueue(alpha, L, lambda, C, T, 40);

        cout << utilization
            << " | " << metricsK5.pLoss
            << " | " << metricsK10.pLoss
            << " | " << metricsK40.pLoss
            << endl;

        mm1KPLossData
            << utilization
            << ", " << metricsK5.pLoss
            << ", " << metricsK10.pLoss
            << ", " << metricsK40.pLoss
            << endl;

        if (utilization <= 2) {
            utilization += 0.1;
        } else if (utilization <= 5) {
            utilization += 0.2;
        } else {
            utilization += 0.4;
        }
    }

    mm1KAvgQueueSizeData.close();
    mm1KPLossData.close();
}

int main() {
    validateExpGen();  // validate that our rand gen is correct
    cout << endl;

    testMM1QueueUtilization(ALPHA, T);
    testMM1KQueueUtilization(ALPHA, T);
    testMM1QueueHighUtlization(ALPHA, T);
}
