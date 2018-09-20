#include "simulation.h"

using namespace std;

PerformanceMetrics simulateMM1Queue(double alpha, double L, double lambda,
                                    double C, double T) {
    // determine observer times
    auto observerEventTimes = genPoissionDistr(alpha, T);

    // determine packet arrival time/sizes
    auto packetArrivialTimes = genPoissionDistr(lambda, T);
    auto packetSizes = genExpDistr(1.0/L, packetArrivialTimes->size());

    // snap sizes to ints
    for (int i = 0; i < packetSizes->size(); i++) {
        packetSizes->at(i) = round(packetSizes->at(i));
    }


    // determine departure times
    shared_ptr<vector<double>> packetDepartureTimes = make_shared<vector<double>>();
    double lastDepartureTime = 0;

    for (int i = 0; i < packetArrivialTimes->size(); i++) {
        double arrivalTime = packetArrivialTimes->at(i);
        double packetSize = packetSizes->at(i);

        double serviceTime = packetSize/C;

        if (arrivalTime >= lastDepartureTime) {
            lastDepartureTime = arrivalTime + serviceTime;
        } else {
            lastDepartureTime += serviceTime;
        }

        packetDepartureTimes->push_back(lastDepartureTime);
    }

    // combine into an event queue for easier simulation
    vector<Event> events;

    for (int i = 0; i < observerEventTimes->size(); i++) {
        Event event = Event(EventType::OBSERVER, observerEventTimes->at(i));
        events.push_back(event);
    }

    for (int i = 0; i < packetArrivialTimes->size(); i++) {
        Event event = Event(EventType::ARRIVAL, packetArrivialTimes->at(i));
        event._packetSize = packetSizes->at(i);
        events.push_back(event);
    }

    for (int i = 0; i < packetDepartureTimes->size(); i++) {
        Event event = Event(EventType::DEPARTURE, packetDepartureTimes->at(i));
        events.push_back(event);
    }

    sort(events.begin(), events.end(),
         [](Event a, Event b) {return a._eventTime < b._eventTime;}
        );

    // simulate
    NetworkQueue q;
    for (int i = 0; i < events.size(); i += 1) {
        q.handle(events.at(i));
    }

    double averageNumberOfPackets = 1.0 * q._sumSampledQueueSize / q._numObservations;
    double proportionIdle = 1.0 * q._numIdle / q._numObservations;

    /* cout << "Num Arrivals: " << q._numArrivals << endl; */
    /* cout << "Num Departures: " << q._numDepartures << endl; */
    /* cout << "Num Observations: " << q._numObservations << endl; */


    /* cout << "Average Number of Packets: " << averageNumberOfPackets << endl; */
    /* cout << "Proprtion Idle: " << proportionIdle << endl << endl; */

    PerformanceMetrics metrics;

    metrics.pIdle = proportionIdle;
    metrics.pLoss = 0.0;
    metrics.averageQSize = averageNumberOfPackets;

    return metrics;
}

PerformanceMetrics simulateMM1KQueue(double alpha, double L, double lambda,
                                    double C, double T, int K) {
    // determine observer times
    auto observerEventTimes = genPoissionDistr(alpha, T);

    // determine packet arrival time/sizes
    auto packetArrivialTimes = genPoissionDistr(lambda, T);

    // combine into an event queue for easier simulation
    queue<Event> events;

    int p1 = 0, p2 = 0;
    while (p1 < observerEventTimes->size() || p2 < packetArrivialTimes->size()) {
        if (p1 < observerEventTimes->size() && p2 < packetArrivialTimes->size()) {
            if (observerEventTimes->at(p1) < packetArrivialTimes->at(p2)) {
                events.push(Event(EventType::OBSERVER, observerEventTimes->at(p1++)));
            } else {
                events.push(Event(EventType::ARRIVAL, packetArrivialTimes->at(p2++)));
                events.back()._averagePacketLength = L;
            }
            continue;
        }

        if (p1 < observerEventTimes->size()) {
            events.push(Event(EventType::OBSERVER, observerEventTimes->at(p1++)));
        } else {
            events.push(Event(EventType::ARRIVAL, packetArrivialTimes->at(p2++)));
        }
    }

    queue<Event> dynamicEvents;  // dynamic events generated on the fly

    // simulate
    NetworkQueue q(true, K, C);

    while (!events.empty() || !dynamicEvents.empty()) {
        if (!events.empty() && !dynamicEvents.empty()) {
            if (events.front()._eventTime < dynamicEvents.front()._eventTime) {
                Event newEvent = q.handle(events.front());
                events.pop();

                if (newEvent._type != EventType::NONE) dynamicEvents.push(newEvent);
            } else {
                Event newEvent = q.handle(dynamicEvents.front());
                dynamicEvents.pop();

                if (newEvent._type != EventType::NONE) dynamicEvents.push(newEvent);
            }
            continue;
        }

        if (!events.empty()) {
            Event newEvent = q.handle(events.front());
            events.pop();
            if (newEvent._type != EventType::NONE) dynamicEvents.push(newEvent);
        } else {
            Event newEvent = q.handle(dynamicEvents.front());
            dynamicEvents.pop();
            if (newEvent._type != EventType::NONE) dynamicEvents.push(newEvent);
        }
    }

    double averageNumberOfPackets = 1.0 * q._sumSampledQueueSize / q._numObservations;
    double proportionIdle = 1.0 * q._numIdle / q._numObservations;
    double proportionLost = 1.0 * q._numDropped / q._numPacketsGenerated;

    /* cout << "Num Arrivals: " << q._numArrivals << endl; */
    /* cout << "Num Departures: " << q._numDepartures << endl; */
    /* cout << "Num Observations: " << q._numObservations << endl; */
    /* cout << "Num Dropped: " << q._numDropped << endl; */
    /* cout << "Num Generated: " << q._numPacketsGenerated << endl; */


    /* cout << "Average Number of Packets: " << averageNumberOfPackets << endl; */
    /* cout << "Proprtion Idle: " << proportionIdle << endl; */
    /* cout << "Proprtion Lost: " << proportionLost << endl << endl; */

    PerformanceMetrics metrics;

    metrics.pIdle = proportionIdle;
    metrics.pLoss = proportionLost;
    metrics.averageQSize = averageNumberOfPackets;

    return metrics;
}
