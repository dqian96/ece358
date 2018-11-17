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

def simulate_ABQ(csv_filename, enable_NAK=False):
    print('Running simulate ABQ with enable_NAK={}\n'.format(enable_NAK))

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

    results = []
    for timeout_multiplier in timeout_multipliers:
        multiplier_results = []
        for propagation_delay in prop_delays:
            for bit_rate_error in BER_values:
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
                sender = GBNSender(es, _SEND, get_packet_fn, channel, receiver, timeout_duration, max_send,
                                   window_size, enable_NAK)

                throughput = sender.throughput
                print('Throughput: {}B/s\n'.format(throughput))
                multiplier_results.append(throughput)

        results.append(multiplier_results)

    f = open(csv_filename, 'w')
    str_results = [[str(val) for val in r] for r in results]
    output = '\n'.join([','.join(r) for r in str_results])
    f.write(output)
    f.close()

    return results

def simulate_GBN(csv_filename):
    pass

def graph_q1_q2(q1_results, q2_results):
    import matplotlib.pyplot as plt

    x = [2.5, 5, 7.5, 10, 12.5]

    plt.figure(num=None, figsize=(14, 10), dpi=80, facecolor='w', edgecolor='k')

    # BER = 0.0
    col = 0
    y_q1_10 = [r[col] for r in q1_results]
    y_q2_10 = [r[col] for r in q2_results]

    y_q1_500 = [r[3 + col] for r in q1_results]
    y_q2_500 = [r[3 + col] for r in q2_results]

    plt.subplot(1, 2, 1)
    plt.plot(x, y_q1_10, 'ko-')
    plt.plot(x, y_q2_10, 'r.-')
    plt.title('Throughput, BER=0, black=q1, red=q2')
    plt.ylabel('Throughput (bytes/sec)')
    plt.xlabel('delta/tau (2tau = 10 ms)')

    plt.subplot(1, 2, 2)
    plt.plot(x, y_q1_500, 'ko-')
    plt.plot(x, y_q2_500, 'r.-')
    plt.title('Throughput, BER=0, black=q1, red=q2')
    plt.ylabel('Throughput (bytes/sec)')
    plt.xlabel('delta/tau (2tau = 500 ms)')

    plt.savefig('q1_q2_ber_0.png')
    plt.clf()

    # BER = 1.0 ** 10^(-5)
    col = 1
    y_q1_10 = [r[col] for r in q1_results]
    y_q2_10 = [r[col] for r in q2_results]

    y_q1_500 = [r[3 + col] for r in q1_results]
    y_q2_500 = [r[3 + col] for r in q2_results]

    plt.subplot(1, 2, 1)
    plt.plot(x, y_q1_10, 'ko-')
    plt.plot(x, y_q2_10, 'r.-')
    plt.title('Throughput, BER=1*10^(-5), black=q1, red=q2')
    plt.ylabel('Throughput (bytes/sec)')
    plt.xlabel('delta/tau (2tau = 10 ms)')

    plt.subplot(1, 2, 2)
    plt.plot(x, y_q1_500, 'ko-')
    plt.plot(x, y_q2_500, 'r.-')
    plt.title('Throughput, BER=1*10^(-5), black=q1, red=q2')
    plt.ylabel('Throughput (bytes/sec)')
    plt.xlabel('delta/tau (2tau = 500 ms)')

    plt.savefig('q1_q2_ber_0.00001.png')
    plt.clf()

    # BER = 1.0 ** 10^(-4)
    col = 2
    y_q1_10 = [r[col] for r in q1_results]
    y_q2_10 = [r[col] for r in q2_results]

    y_q1_500 = [r[3 + col] for r in q1_results]
    y_q2_500 = [r[3 + col] for r in q2_results]

    plt.subplot(1, 2, 1)
    plt.plot(x, y_q1_10, 'ko-')
    plt.plot(x, y_q2_10, 'r.-')
    plt.title('Throughput, BER=1*10^(-4), black=q1, red=q2')
    plt.ylabel('Throughput (bytes/sec)')
    plt.xlabel('delta/tau (2tau = 10 ms)')

    plt.subplot(1, 2, 2)
    plt.plot(x, y_q1_500, 'ko-')
    plt.plot(x, y_q2_500, 'r.-')
    plt.title('Throughput, BER=1*10^(-4), black=q1, red=q2')
    plt.ylabel('Throughput (bytes/sec)')
    plt.xlabel('delta/tau (2tau = 500 ms)')

    plt.savefig('q1_q2_ber_0.0001.png')
    plt.clf()

def graph_q1_q3(q1_results, q3_results):
    pass
