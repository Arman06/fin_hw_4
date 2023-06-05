import socket
import _socket


class MySocket(socket.socket):
    def __init__(self, *args, **kwargs):
        super(MySocket, self).__init__(*args, **kwargs)
        self.HEADER = 10

    @classmethod
    def copy(cls, sock):
        fd = _socket.dup(sock.fileno())
        copy = cls(sock.family, sock.type, sock.proto, fileno=fd)
        copy.settimeout(sock.gettimeout())
        return copy

    def send_message_with_header(self, data):
        message_with_header = f"{len(data):<{self.HEADER}}" + data
        super(MySocket, self).sendall(message_with_header.encode())

    def receive_message_with_header(self):
        try:
            message_header = self.recv(self.HEADER)
            if not len(message_header):
                return False
            return self.recv(int(message_header.decode().strip())).decode()
        except:
            return False


