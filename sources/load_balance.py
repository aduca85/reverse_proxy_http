import socket_wrapper
import random

class LoadBalance(socket_wrapper.SocketWrapper):

    def __init__(self):
        socket_wrapper.SocketWrapper.__init__(self)

    def connect(self, upstream_list, load_balancer_strategy):
        if load_balancer_strategy == 'random':
            upstream = random.choice(upstream_list)
        self.socket.connect(upstream)
        