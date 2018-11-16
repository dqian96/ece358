from random import random

class Channel(object):

    """Represents a Channel."""

    # constants
    BIT_ERROR_TOLERANCE = 4 # according to the lab manual, 'we consider a frame exp 5 or more...to be lost'

    def __init__(self, capacity, propagation_delay, bit_error_rate):
        """Creates the Channel object

        :capacity: capacity of the channel in (bytes/s)
        :propagation_delay: propagation delay of sending a packet through the channel (seconds)
        :bit_error_rate: the probability of each bit having an error during transmission

        """
        self._capacity = capacity
        self._propagation_delay = propagation_delay
        self._bit_error_rate = bit_error_rate

    def transmit(self, time, frame):
        """Transmit the frame through the channel

        :time: the int time that the frame was sent to the channel
        :frame: the frame object to be sent through the channel
        :returns: a tuple (delivered_frame: Frame, delivered_time: int)

        """
        delivered_frame = Channel._undergo_interference(frame, self._bit_error_rate)

        if delivered_frame is not None:
            # frame not lost
            delivered_time = time + self._propagation_delay
            return delivered_frame, delivered_time

        return None, None  # lost frame

    @property
    def capacity(self):
        return self._capacity

    @staticmethod
    def _undergo_interference(frame, bit_error_rate):
        """Return the frame after it has been affected by the interference of tranmission/

        :frame: the unaffected frame
        :bit_error_rate: BER of the channel
        :returns: the affected frame

        """
        frame_length = frame.length

        num_bit_errors = 0
        for bit in range(frame_length * 8):
            ### IMPORTANT: the frame length is given in bytes.
            ### We iterate over each bit to check if it is corrupted.
            is_bit_safe = 0 if random() <= bit_error_rate else 1
            num_bit_errors += not is_bit_safe

        if num_bit_errors == 0:
            # no bit errors
            return frame

        if num_bit_errors <= Channel.BIT_ERROR_TOLERANCE:
            # bit error'd
            frame.is_error = True
            return frame

        # lost
        return None
