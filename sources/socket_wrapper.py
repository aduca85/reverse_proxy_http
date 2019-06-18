import socket
import select
import datetime

class SocketWrapper():
    '''
    This class is a wrapper over socket library
    '''
    def __init__(self, s=''):
        if s:
            self.socket = s
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Disable nagle algorithm for this socket
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
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
    
    def recv_client(self, buffer_size=2048):
        full_message = bytearray()
        wait_for_message = True
        connection_start_time = datetime.datetime.now()
        while wait_for_message:
            connection_time = datetime.datetime.now() - connection_start_time
            # The request should arrive in less than 10 seconds
            if connection_time.seconds > 60:
                self.socket.close()
                full_message = bytearray()
                break
            is_readable, _, _ = select.select([self.socket], [], [], 0)
            for s in is_readable:
                try:
                    data = s.recv(buffer_size)
                except Exception:
                    break
                # The maximum allowed request length is 4096 bytes
                if len(full_message) > 4096:
                    s.close()
                    full_message = bytearray()
                    wait_for_message = False
                else:
                    full_message.extend(data)
                    # Proper HTTP protocol ends with 2 return cariage and new line
                    if '\r\n\r\n' in full_message.decode():
                        wait_for_message = False
        if len(full_message) > 0:
            return full_message
        return False

    def recv_upstream(self):
        is_readable, _, _ = select.select([self.socket], [], [])
        for s in is_readable:
            data = s.recv(4096)
        return data
            
    
    def send_message(self, message):
        _, is_writeable, _ = select.select([], [self.socket], [])
        for s in is_writeable:
            s.send(message)
    
    def close(self):
        self.socket.close()
    
    def get_socket(self):
        return self.socket