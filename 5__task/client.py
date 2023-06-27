import socket

import socket

# Введите простые числа для основания и модуля.
BASE = 5
MODULUS = 23


class Client:
    def __init__(self, host='localhost', port=8000):
        self.sock = socket.socket()
        self.sock.connect((host, port))

        self.private_key = 15  # Введите свой секретный ключ.
        self.public_key = (BASE ** self.private_key) % MODULUS

    def exchange_keys(self):
        self.sock.send(str(self.public_key).encode())

        server_key = self.sock.recv(1024).decode()

        self.shared_key = (int(server_key) ** self.private_key) % MODULUS

        print(f"Shared secret key: {self.shared_key}")

    def send_messages(self):
        while True:
            message = input("Введите сообщение: ")
            encrypted_message = ''.join(chr(ord(c) + self.shared_key) for c in message)
            self.sock.send(encrypted_message.encode())


if __name__ == "__main__":
    client = Client()
    client.exchange_keys()
    client.send_messages()

