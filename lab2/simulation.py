from copy import deepcopy
from event_scheduler import ACKEvent, EventType, EventScheduler
from channel import Channel
from gbn import GBNReceiver, GBNSender

def _SEND(time, frame, channel, receiver):
    """Simulate the life of a frame as it is sent, received, and ack'd.

    :time: the int time that the frame was sent by the sender
    :frame: the frame: Frame being sent
    :channel: channel: Channel connecting the sender and receiver
    :receiver: the receiver: GBNReceiver object
    :returns: an Event generated at the sender

    """
    # num_delivered = receiver.num_delivered
    # if num_delivered % 100 == 0:
    #     print('successfully sent: {}'.format(num_delivered))

    frame = deepcopy(frame)  # make a copy to send
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

def _create_datagram_gen_fn(datagram_length):
    # dynamically create get packet functions for certain packet lengths
    def get_packet_fn():
        return 1, datagram_length
    return get_packet_fn

def simulate_ABQ(csv_filename):
    window_size = 1
    seq_no_range = window_size + 1

    # exercise i)
    C = 5 * 10**6 / 8 # 5 Mb/s = 625000 bytes/s
    BER_values = [0, 1 * 10**(-5), 1 * 10**(-4)]
    prop_delays = [10/2000, 500/2000]
    timeout_multipliers = [2.5, 5, 7.5, 10, 12.5]

    max_send = 10000
    datagram_length = 1500

    get_packet_fn = _create_datagram_gen_fn(datagram_length)

    for bit_rate_error in BER_values:
        for propagation_delay in prop_delays:
            for timeout_multiplier in timeout_multipliers:
                timeout_duration = timeout_multiplier * propagation_delay

                msg = """Running ABQ simulation with options:
                         C={}B
                         BER={}
                         prop_delay={}s
                         timeout={}s
                         datagram_length={}B
                         max_send={} """
                print(msg.format(C, bit_rate_error, propagation_delay, timeout_duration,
                                 datagram_length, max_send))

                es = EventScheduler()
                channel = Channel(C, propagation_delay, bit_rate_error)
                receiver = GBNReceiver(seq_no_range, C)
                sender = GBNSender(es, _SEND, get_packet_fn, channel, receiver, timeout_duration, max_send, window_size)

                throughput = sender.throughput
                print('Throughput: {}B/s\n'.format(throughput))

def ABQ_NAK():
    pass

def GBN():
    pass
