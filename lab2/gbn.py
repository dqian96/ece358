from collections import deque

from .frame import Frame


class GBNSender(object):

    """GBN Sender. Sends messages based on go-back-n."""

    FRAME_HEADER_SIZE = 10

    def __init__(self, es, forward_channel, time_out, window_size=1):
        """Creates the GBN sender.

        :es: an event scheduler object to push/pop events from
        :foward_channel: a Channel object representing the forward channel
        :time_out: seconds until the sender times out
        :window_size: an integer buffer size

        """
        assert window_size >= 1
        self._window_size = window_size
        self._time_out = time_out

        self._seq_no = 0
        self._next_expected_ack = 1
        self._current_time = 0

        self._buffer = 0


class GBNReceiver(object):

    """GBN Receiver class."""

    def __init__(self, num_seq_nos, reverse_capacity):
        """Create the GBNReceiver object

        :num_seq_nos: the number of distinct sequence numbers of Frames
        :reverse_capacity: the int capacity of the reverse link in bytes

        """
        assert num_seq_nos > 0 and reverse_capacity > 0

        self._num_seq_nos = num_seq_nos
        self._reverse_capacity = reverse_capacity

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
        :returns: a tuple (time_replied: int, ack: Frame) to acknowledge a received packet

        """
        assert frame is not None  # lost frames should be not be given to this method

        self._current_time = time

        if not frame.is_error:
            if frame.seq_no == self._next_expected_frame:
                # in order frame
                self._deliver(frame)
                self._next_expected_frame = (self._next_expected_frame + 1) % self._num_seq_nos

        ack = Frame(self._next_expected_frame, None, 0)

        transmission_delay = ack.length/self._reverse_capacity
        time_replied = self._current_time + transmission_delay

        return time_replied, ack

    def _deliver(self, datagram):
        """Deliver a datagram to layer 3

        :datagram: the datagram to deliver to the above layer

        """
        self._num_delivered += 1
        # deliver(datagram)
