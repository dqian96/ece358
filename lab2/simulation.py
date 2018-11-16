from event_scheduler import ACKEvent, EventType, EventScheduler
from channel import Channel
from gbn import GBNReceiver, GBNSender

def send(time, frame, channel, receiver):
    """Simulate the life of a frame as it is sent, received, and ack'd.

    :time: the int time that the frame was sent
    :frame: the frame: Frame being sent
    :receiver: the receiver: GBNReceiver object
    :channel: channel: Channel connecting the sender and receiver
    :returns: an Event object

    """
    delivered_frame, delivered_time = channel.transmit(time, frame)

    delivered_ack = None  # default ack lost
    if delivered_frame is not None:
        # packet not lost
        ack, time_replied = receiver.receive(delivered_time, delivered_frame)
        print(ack, time_replied)
        delivered_ack, delivered_ack_time = channel.transmit(time_replied, ack)

    if delivered_ack is not None:
        # ack not lost
        ack_event = ACKEvent(EventType.ACK, delivered_ack_time, delivered_ack.is_error, delivered_ack.seq_no)
        return ack_event

    return None  # ack lost; no event

def create_datagram():
    datagram_length = 1500
    return None, datagram_length

def simulate(window_size, timeout_duration, link_capacity, propagation_delay, bit_error_rate):
    es = EventScheduler()

    channel = Channel(link_capacity, propagation_delay, bit_error_rate)
    receiver = GBNReceiver(window_size, link_capacity)
    sender = GBNSender(es, send, create_datagram, channel, receiver, timeout_duration, window_size)
