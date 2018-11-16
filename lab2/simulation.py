from event_scheduler import ACKEvent, EventType, EventScheduler
from channel import Channel
from gbn import GBNReceiver, GBNSender

def SEND(time, frame, channel, receiver):
    """Simulate the life of a frame as it is sent, received, and ack'd.

    :time: the int time that the frame was sent by the sender
    :frame: the frame: Frame being sent
    :channel: channel: Channel connecting the sender and receiver
    :receiver: the receiver: GBNReceiver object
    :returns: an Event generated at the sender

    """
    delivered_frame, delivered_time = channel.transmit(time, frame)

    delivered_ack = None  # default ack lost
    if delivered_frame is not None:
        # frame passed through channel without being lost
        ack, time_replied = receiver.receive(delivered_time, delivered_frame)
        delivered_ack, delivered_ack_time = channel.transmit(time_replied, ack)

    if delivered_ack is not None:
        # ack not lost on its way to teh sender
        ack_event = ACKEvent(EventType.ACK, delivered_ack_time, delivered_ack.is_error, delivered_ack.seq_no)
        return ack_event

    return None  # ack lost; no event

def create_datagram_gen_fn(datagram_length):
    # dynamically create get packet functions for certain packet lengths
    def get_packet_fn():
        return 1, datagram_length
    return get_packet_fn

def ABQ():
    window_size = 1

    BER = 0
    C = 625000 # 5 Mb/s is 625000 bytes
    prop_delay = 0.5  # 5000 ms and 10 ms
    timeout_duration = 5 * prop_delay
    datagram_length = 1500


    get_packet_fn = create_datagram_gen_fn(datagram_length)
    es = EventScheduler()

    channel = Channel(C, prop_delay, BER)
    receiver = GBNReceiver(window_size + 1, C)
    sender = GBNSender(es, SEND, get_packet_fn, channel, receiver, timeout_duration, window_size)

    print(sender.throughput)

def ABQ_NAK():
    pass

def GBN():
    pass
