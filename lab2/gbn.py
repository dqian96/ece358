from collections import deque, namedtuple

from .event_scheduler import ACKEvent, TimeoutEvent, EventType, EventScheduler
from .frame import Frame


class GBNSender(object):

    """GBN Sender. Sends messages based on go-back-n."""

    FRAME_HEADER_SIZE = 10

    WaitingPacket = namedtuple('WaitingPacket', 'time_sent frame')

    def __init__(self, es, udt_send_fn, get_packet_fn, channel, link_capacity, timeout_duration, window_size=1):
        """Creates the GBN sender.

        :es: an event scheduler object to push/pop events from
        :get_packet_fn: function() -> (packet: Packet, length: int) that returns a packet from the above layer
        :capacity: the capacity of the forward channel in bytes/sec
        :timeout_duration: seconds until the sender times out
        :window_size: an integer buffer size

        """
        # config
        assert window_size >= 1
        self._window_size = window_size
        self._timeout_duration = timeout_duration
        self._link_capacity = link_capacity

        # state
        self._seq_no = 0
        self._current_time = 0

        self._buffer = []
        self._next_packet_to_send_idx = 0

        # association
        self._es = es
        self._get_packet_fn = get_packet_fn
        self._udt_send_fn = udt_send_fn
        self._channel = channel

        self._listen()  # listen to above for data; start sending packets

    @staticmethod
    def _is_timeout_event(event):
        return event.type == EventType.TIMEOUT

    def _handle_event(self, next_event):
        if next_event is None:
            # no event occurred
            return

        if next_event.type == EventType.TIMEOUT:
            # retransmit all
            self._next_packet_to_send_idx = 0
            return

        if next_event.type == EventType.ACK:
            ack_event = next_event
            oldest_seq_no = self._buffer[0].frame.seq_no
            if not ack_event.is_error and ack_event.seq_no != oldest_seq_no:
                # correctly received
                no_ackd = (ack_event.seq_no - oldest_seq_no) % (self._window_size + 1)
                self._slide(no_ackd)
                self._fill_buffer()

                self._next_packet_to_send_idx -= no_ackd
                oldest_packet = self._buffer[self._next_packet_to_send_idx]
                if oldest_packet.time_sent is not None:
                    # update timeout timer to the used for this sent frame
                    timeout_time = oldest_packet.time_sent + self._timeout_duration
                    self._es.purge(GBNSender._is_timeout_event)
                    timeout_event = TimeoutEvent(EventType.TIMEOUT, timeout_time)
                    self._es.register(timeout_time, timeout_event)
            else:
                # erroneous ack'd or transmission
                return  # ignore

        assert False  # should never happen

    def _listen(self):
        """TODO: Docstring for start.

        :arg1: TODO
        :returns: TODO

        """

        self._fill_buffer()  # fill buffer completely

        self._next_packet_to_send_idx = 0
        while True:
            _, frame = self._buffer[self._next_packet_to_send_idx]

            transmission_delay = frame.length / self._link_capacity
            time_sent = self._current_time + transmission_delay

            if self._next_packet_to_send_idx == 0:
                # start timeout on oldest packet in buffer
                timeout_time = time_sent + self._timeout_duration
                timeout_event = TimeoutEvent(EventType.TIMEOUT, timeout_time)
                self._es.purge(GBNSender._is_timeout_event)
                self._es.register(timeout_time, timeout_event)

            self._buffer[self._next_packet_to_send_idx] = GBNSender.WaitingPacket(time_sent, frame)

            event = self._udt_send_fn(time_sent, frame, self._channel)
            if event is not None:
                # packet not lost
                self._es.register(event.time, event)

            self._next_packet_to_send_idx += 1

            next_event = self._es.peek()
            if self._current_time <= next_event.time and next_event.time <= self._current_time + transmission_delay:
                # event occurred between transmission
                self._current_time += transmission_delay
                continue
            elif self._next_packet_to_send_idx == self._window_size:
                # no events occurred in between and no more packets to send
                self._current_time = next_event.time
                self._handle_event(self._es.pop())


            self._current_time = time_sent



    def _fill_buffer(self):
        """Fill the remaining empty space in the buffer by asking the upper layer for more data."""
        while len(self._buffer) < self._window_size:
            datagram, datagram_length = self._get_packet_fn()
            frame = Frame(self._seq_no, datagram, datagram_length)
            self._seq_no = (self._seq_no + 1) % (self._window_size + 1)

            waiting_packet = GBNSender.WaitingPacket(None, frame)
            self._buffer.append(waiting_packet)

    def _slide(self, n):
        """Slides the buffer to the left by n steps.

        :n: the number of elements to slide to the left by

        """
        return self._buffer[n:]


class GBNReceiver(object):

    """GBN Receiver class."""

    def __init__(self, num_seq_nos, capacity):
        """Create the GBNReceiver object

        :num_seq_nos: the number of distinct sequence numbers of Frames (i.e. 2 for seq # E [0, 1])
        :capacity: the int capacity of the reverse link in bytes

        """
        assert num_seq_nos > 0 and capacity > 0

        self._num_seq_nos = num_seq_nos
        self._link_capacity = capacity

        self._next_expected_frame = 0
        self._current_time = 0
        self._num_delivered = 0

    @property
    def num_delievered(self):
        return self._num_delivered

    def receive(self, time, frame):
        """Receives a Frame from a channel.

        :time: the time that the Frame was received
        :frame: the frame received
        :returns: a tuple (ack: Frame, time_replied: int) to acknowledge a received packet

        """
        assert frame is not None  # lost frames should be not be given to this method

        self._current_time = time

        if not frame.is_error:
            if frame.seq_no == self._next_expected_frame:
                # in order frame
                self._deliver(frame)
                self._next_expected_frame = (self._next_expected_frame + 1) % self._num_seq_nos

        ack = Frame(self._next_expected_frame, None, 0)

        transmission_delay = ack.length/self._link_capacity

        time_replied = self._current_time + transmission_delay

        return ack, time_replied

    def _deliver(self, datagram):
        """Deliver a datagram to layer 3

        :datagram: the datagram to deliver to the above layer

        """
        self._num_delivered += 1
        # deliver(datagram)
