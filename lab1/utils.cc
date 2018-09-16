#include "utils.h"

#include <iostream>
#include <vector>

using namespace std;

double genExpRand(double lambda = 75) {
    // generate an uniformaly distributed variable in [0, 1]
    double uniformDistrValue = (1.0 * rand()) / RAND_MAX;
    double expRandValue = -1 * log(1 - uniformDistrValue) / lambda;

    return expRandValue;
}

shared_ptr<vector<double>> genExpDistr(double lambda, int N) {
    shared_ptr<vector<double>> distr = make_shared<vector<double>>();

    for (int i = 0; i < N; i++) {
         distr->push_back(genExpRand(lambda));
    }

    return distr;
}

shared_ptr<vector<double>> genPoissionDistr(double lambda, int T) {
    // generates a poission distribution by calculating the time elapsed
    // between events using an exponential random variable

    double currentTime = 0;
    shared_ptr<vector<double>> distr = make_shared<vector<double>>();


    while (currentTime < T) {
        double genValue = genExpRand(lambda);

        currentTime += genValue;

        distr->push_back(currentTime);
    }

    return distr;
}
