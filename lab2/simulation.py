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
        delivered_ack, delivered_ack_time = channel.transmit(time_replied, ack)

    if delivered_ack is not None:
        # ack not lost
        ack_event = ACKEvent(EventType.ACK, delivered_ack_time, delivered_ack.is_error, delivered_ack.seq_no)
        return ack_event

    return None  # ack lost; no event

def create_datagram():
    datagram_length = 1500
    return None, datagram_length

def ABQ():
    window_size = 1

    BER = 0
    C = 625000 # 5 Mb/s is 625000 bytes
    prop_delay = 0.5  # 5000 ms and 10 ms
    timeout_duration = 5 * prop_delay

    max_gen = 10000
    num_gen = [0]

    es = EventScheduler()

    channel = Channel(C, prop_delay, BER)
    receiver = GBNReceiver(window_size + 1, C)
    sender = GBNSender(es, send, create_datagram, channel, receiver, timeout_duration, window_size)

    print(sender.throughput)
