#ifndef QUEUE_H
#define QUEUE_H

#include <limits>
#include <vector>
#include <queue>

#include "utils.h"

enum class EventType { NONE, OBSERVER, ARRIVAL, DEPARTURE };

struct Event {
    double _eventTime;
    EventType _type;

    // potential metadata
    int _packetSize = -1;
    double _averagePacketLength = 0.0;

    Event(EventType type, double eventTime = 0);
};

struct NetworkQueue {
    // counters
    int _numArrivals = 0, _numDepartures = 0;
    int _numObservations = 0, _numIdle = 0;

    int _sumSampledQueueSize = 0;

    // M/M/1/N QUEUE IMPL START
    bool _isGenDepartureEvents;      // let the queue generate its own departure events
    double _lastDepartureTime = 0;   // the expected departure time of the last packet in q
    double _linkCapacity;
    int _maxSize;                    // default infinite size
    int _numPacketsGenerated = 0, _numDropped = 0;
    // M/M/1/N QUEUE IMPL END


    NetworkQueue(
        bool isGenDepartureEvents = false,
        int maxSize = -1,
        double linkCapacity = 1000000
    );

    Event handle(Event e);
};


#endif  // QUEUE_H
