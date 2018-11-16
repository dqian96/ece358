from collections import namedtuple
from enum import Enum
from heapq import heappop, heappush, heapify

class EventType(Enum):
    TIMEOUT = 1
    ACK = 2

# namedtuples act as C-like struct for representing the events
TimeoutEvent = namedtuple('TimeoutEvent', 'type time')
ACKEvent = namedtuple('ACKEvent', 'type time is_error seq_no')

class EventScheduler(object):

    """An Event Schedule/Queue."""

    def __init__(self, events_list=None):
        """Create a Event Scheduler object

        :events_list: a list of Events to initialize the queue with

        """
        self._heap_q = []

        if events_list is not None:
            self._heap_q = [(e.time, e) for e in events_list]
            heapify(self._heap_q)

    def pop(self):
        """Pops the next event by time

        :returns: an Event object

        """
        if len(self._heap_q) == 0:
            # no events to consume
            return None

        event_tuple = heappop(self._heap_q)  # (time: int, e Event)
        return event_tuple[1]

    def peek(self):
        """Peeks are the next event in the queue

        :returns: an Event object

        """
        if len(self._heap_q) == 0:
            # no events to consume
            return None

        return self._heap_q[0][1]


    def register(self, time, event):
       """Add an Event to the scheduler with time

       :time: int time of the event
       :event: event to insert

       """

       heap_ele = (time, event)
       heappush(self._heap_q, heap_ele)

    def purge(self, should_del_fn):
        """Purge from the event buffer all events matching a qualifier.

        :should_del_fn: function(event): bool that evaluates true if event should be deleted

        """
        self._heap_q = [e for e in self._heap_q if not should_del_fn(e[1])]
        heapify(self._heap_q)
