class Frame(object):

    """Represents a frame transferred over the Channel"""

    # constants
    HEADER_LENGTH = 54  # length of the header in bytes

    def __init__(self, seq_no, datagram, datagram_length):
        """Creates a Frame object.

        :seq_no: the sequence number of the frame
        :datagram: the datagram encapsulated
        :datagram_length: length of the datagram in bytes

        """
        self._seq_no = seq_no
        self._datagram = datagram
        self._datagram_length = datagram_length

        self._is_error = False

    def __str__(self):
        return 'seq no: {}, is_error: {}'.format(self._seq_no, self._is_error)

    def __repr__(self):
        return str(self)

    @property
    def is_error(self):
        return self._is_error

    @is_error.setter
    def is_error(self, val):
        self._is_error = val

    @property
    def length(self):
        """Returns the total size of the Frame in bytes."""
        return Frame.HEADER_LENGTH + self._datagram_length

    @property
    def seq_no(self):
        return self._seq_no

    def unravel(self):
        """De-encapsulates the frame to return the datagram.

        This not used in our simulation but added for completeness.

        :returns: the datagram

        """
        return self._datagram
