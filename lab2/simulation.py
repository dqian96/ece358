import Channel

def simulate_arq():
    """TODO: Docstring for simulate_arq.
    :returns: TODO

    """

    sender = ARQSender()
    receiver = ARQReciver()

    forward_channel = Channel(prop_delay, 0.5, receiver)
    backward_channel = Channel(prop_delay, 0.5, sender)
