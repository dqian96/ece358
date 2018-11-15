from random import random

class Channel(object):

    """Represents a Channel."""

    # constants
    BIT_ERROR_TOLERANCE = 4

    def __init__(self, capacity, propagation_delay, bit_error_rate, receiver):
        """Creates the Channel object

        :capacity: capacity of the channel in (bytes/s)
        :propagation_delay: propagation delay of sending a packet through the channel
        :bit_error_rate: the probability of each bit having an error during transmission
        :receiver: the receiver object that the data is sent to

        """
        self._capacity = capacity
        self._propagation_delay = propagation_delay
        self._bit_error_rate = bit_error_rate
        self._receiver = receiver

    def transmit(self, time, frame):
        """Transmit

        :time: the int time that the frame was sent
        :frame: the frame object to be sent through the channel
        :returns: TODO

        """
        frame = Channel._undergo_interference(frame, self._bit_error_rate)

        if frame is not None:
            # frame not lost
            received_time = time + self._propagation_delay
            self._receiver.receive(received_time, frame)

    def get_transmission_delay(self, packet_length):
        """Calculate the tranmission delay to send a packet of given length

        :packet_length: int size of the packet in bytes
        :returns: the time in seconds for the packet to be put on the link

        """
        assert packet_length != 0
        return packet_length/self._capacity

    @staticmethod
    def _undergo_interference(frame, bit_error_rate):
        """Return the frame after it has been affected by the interference of tranmission/

        :frame: the unaffected frame
        :bit_error_rate: BER of the channel
        :returns: the affected frame

        """
        packet_length = frame.length

        num_bit_errors = 0
        for bit in range(packet_length):
            is_bit_safe = 0 if random() <= bit_error_rate else 1
            num_bit_errors += not is_bit_safe

        if num_bit_errors == 0:
            # no bit errors
            return frame
        elif num_bit_errors <= Channel.BIT_ERROR_TOLERANCE:
            frame.is_error = True
            return frame

        # lost
        return None
