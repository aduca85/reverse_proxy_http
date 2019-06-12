import client
import socket_wrapper
import select

class Server(socket_wrapper.SocketWrapper):

    def __init__(self):
        super()
    
    def run(self, server_address, upstream_list):
        socket = socket_wrapper.SocketWrapper()
        socket.bind(server_address)
        socket.listen(5)
        inputs = [socket.get_socket()]
        while True:
            is_readable,_ ,_ = select.select(inputs, [], [])
            for s in is_readable:
                if s == socket.get_socket():
                    client_connection, client_address = socket.accept()
                    client_thread = client.Client(client_connection, client_address, upstream_list)
                    client_thread.start()
        socket.close()
