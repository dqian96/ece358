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

    def __init__(self, reverse_channel, num_seq_nos):
        """TODO: to be defined1.

        :reverse_channel: the Channel to send ACKs to the sender
        :num_seq_nos: the number of distinct sequence numbers of Frames

        """
        self._reverse_channel = reverse_channel
        self._num_seq_nos = num_seq_nos

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
        :returns: TODO

        """
        self._current_time = time

        if not frame.is_error:
            if frame.seq_no == self._next_expected_frame:
                # in order frame
                self._deliver(frame)
                self._next_expected_frame = (self._next_expected_frame + 1) % self._num_seq_nos

        ack = Frame(self._next_expected_frame, None, 0)

        transmission_delay = self._reverse_channel.get_transmission_delay(ack.packet_length)
        time_sent = self._current_time + transmission_delay
        self._reverse_channel.transmit(time_sent, ack)



    def _deliver(self, datagram):
        """Deliver a datagram to layer 3

        :datagram: the datagram to deliver to the above layer

        """
        self._num_delivered += 1
        # deliver(datagram)
