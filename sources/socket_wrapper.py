import socket
import select

class SocketWrapper():

    def __init__(self, s=''):
        if s:
            self.socket = s
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def bind(self, address):
        try:
            self.socket.bind(address)
        except Exception as e:
            print(f'Error: {e}')
    
    def listen(self, concurrent_connections=5):
        self.socket.listen(concurrent_connections)
    
    def accept(self):
        return self.socket.accept()
    
    #def connect(self, address):
    #    self.socket.connect(address)
    
    def recv_message(self, buffer_size=1024):
        is_readable, _, _ = select.select([self.socket], [], [])
        for s in is_readable:
            full_message = b''
            while True:
                try:
                    data = s.recv(buffer_size)
                except Exception:
                    break
                # The maximum allowed request length is 4096 bytes - if bigger close the socket
                if len(full_message) > 4096:
                    s.close()
                    full_message = False
                elif not data:
                    break
                else:
                    full_message += data
        return full_message
    
    def send_message(self, message):
        _, is_writeable, _ = select.select([], [self.socket], [])
        for s in is_writeable:
            s.send(message)
    
    def close(self):
        self.socket.close()
    
    def get_socket(self):
        return self.socket