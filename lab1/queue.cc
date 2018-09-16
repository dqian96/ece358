#include "queue.h"

using namespace std;

Event::Event(EventType type, double eventTime) : _eventTime(eventTime), _type(type) {}

NetworkQueue::NetworkQueue(bool isGenDepartureEvents,
                           int maxSize,
                           double linkCapacity)
    : _maxSize(maxSize), _isGenDepartureEvents(isGenDepartureEvents), _linkCapacity(linkCapacity) {}

Event NetworkQueue::handle(Event e) {
    int currentSize = _numArrivals - _numDepartures;

    if (e._type == EventType::OBSERVER) {
        _numObservations += 1;
        _numIdle += (currentSize == 0);

        _sumSampledQueueSize += currentSize;
    } else if (e._type == EventType::ARRIVAL) {
        _numPacketsGenerated += 1;

        if (currentSize >= _maxSize && _maxSize != -1) {
            // packets dropped
            _numDropped += 1;
        } else {
            // packet not dropped
            _numArrivals += 1;
            currentSize += 1;

            // M/M/1/N QUEUE IMPL START
            if (e._packetSize == -1) {
                // packet size undetermined = randomly generate
                e._packetSize = genExpRand(1.0/e._averagePacketLength);
            }

            if (_isGenDepartureEvents) {
                double serviceTime = e._packetSize / _linkCapacity;

                if (currentSize == 1) {
                    // this packet just arrived
                    _lastDepartureTime = e._eventTime + serviceTime;
                } else {
                    _lastDepartureTime = _lastDepartureTime + serviceTime;
                }

                return Event(EventType::DEPARTURE, _lastDepartureTime);
            }
            // M/M/1/N QUEUE IMPL END
        }

    } else if (e._type == EventType::DEPARTURE) {
        _numDepartures += 1;
    }

    return Event(EventType::NONE);  // event type is none branches here
}
