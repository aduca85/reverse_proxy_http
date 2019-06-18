import load_balance
import threading
import socket_wrapper
import http_parser

class Client(threading.Thread):
    '''
    This class will configures how to handle the request received from the client
    '''
    def __init__(self, client_connection, client_address, upstream_list, load_balancer_strategy):
       threading.Thread.__init__(self)
       self.client_connection = client_connection
       self.client_address = client_address
       self.upstream_list = upstream_list
       self.load_balancer_strategy = load_balancer_strategy

    def run(self):
        self.client_connection.setblocking(0)
        
        socket_client = socket_wrapper.SocketWrapper(self.client_connection)
        message_from_client = socket_client.recv_client()
        is_valid_http_request = True
        try:
            http_parser.BasicHTTPHandler(message_from_client)
        except Exception:
            is_valid_http_request = False
  

        if is_valid_http_request:
            socket_upstream = load_balance.LoadBalance()
            socket_upstream.connect(self.upstream_list, self.load_balancer_strategy)
            socket_upstream.get_socket().setblocking(0)
            socket_upstream.send_message(message_from_client)
            message_from_upstream = socket_upstream.recv_upstream()
            socket_client.send_message(message_from_upstream)
            socket_upstream.close()
        
        socket_client.close()    
        