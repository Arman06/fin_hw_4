import socket

BASE = 5
MODULUS = 23


class Server:
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port

        self.private_key = 6 
        self.public_key = (BASE ** self.private_key) % MODULUS

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_socket.bind((self.host, self.port))

        server_socket.listen(1)

        print("Сервер ожидает соединения")

        client_socket, address = server_socket.accept()
        print("Подключение от ", address)
        self.exchange_keys(client_socket)
        self.receive_messages(client_socket)

    def exchange_keys(self, client_socket):
        client_key = client_socket.recv(1024).decode()

        client_socket.send(str(self.public_key).encode())

        self.shared_key = (int(client_key) ** self.private_key) % MODULUS

        print(f"Shared secret key: {self.shared_key}")
        return client_socket

    def receive_messages(self, conn):
        while True:
            encrypted_message = conn.recv(1024).decode()
            message = ''.join(chr(ord(c) - self.shared_key) for c in encrypted_message)

            print(f"Decrypted message: {message}")


if __name__ == "__main__":
    server = Server()
    server.start()

