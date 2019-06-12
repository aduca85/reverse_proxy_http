import load_balance
import threading
import socket_wrapper

class Client(threading.Thread):
    '''
    This class will support multi-threading requests 
    '''
    def __init__(self, client_connection, client_address, upstream_list):
       threading.Thread.__init__(self)
       self.client_connection = client_connection
       self.client_address = client_address
       self.upstream_list = upstream_list

    def run(self):
        self.client_connection.setblocking(0)
        
        socket_client = socket_wrapper.SocketWrapper(self.client_connection)
        message_from_client = socket_client.recv_message(20)

        if message_from_client:
            socket_upstream = load_balance.LoadBalance()
            socket_upstream.connect(self.upstream_list)
            socket_upstream.get_socket().setblocking(0)
            socket_upstream.send_message(message_from_client)
            message_from_upstream = socket_upstream.recv_message()
            socket_client.send_message(message_from_upstream)
            socket_upstream.close()
        
        socket_client.close()    
        