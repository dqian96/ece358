from .event_scheduler import EventScheduler
from .channel import Channel
from .gbn import GBNReceiver, GBNSender

def send(time, frame, channel):
    """Sen
    :returns: TODO

    """
    delivered_time, delivered_frame = channel.transmit(time, frame)

    delivered_ack = None  # default ack lost
    if delivered_frame is not None:
        # packet not lost
        ack, time_replied = receiver.receive(delivered_time, delivered_frame)
        delivered_ack, delivered_ack_time = channel.transmit(ack, time_replied)

    if delivered_ack is not None:
        # ack not lost
        ack_event = ACKEvent(EventType.ACK, delivered_ack_time, delivered_ack.is_error, delivered_ack.seq_no)
        return ack_event

    return None  # ack lost; no event

def simulate_arq():
    """TODO: Docstring for simulate_arq.
    :returns: TODO

    """

    sender = ARQSender()
    receiver = ARQReciver()

    forward_channel = Channel(prop_delay, 0.5, receiver)
    backward_channel = Channel(prop_delay, 0.5, sender)

def simulate(N, datagram_length, timeout):
    es = EventScheduler()

    sender = GBNSender()
    receiver = GBNReceiver(N)

    for:
        sender.rdt_send(None, datagram_length)
