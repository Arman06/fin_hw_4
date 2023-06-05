import socket
import threading
import json
import datetime
import hashlib
from MySuperSocket import MySocket


class MyLogger:
    def __init__(self, filename):
        self.filename = filename

    def make_an_entry(self, entry, verbose=False):
        with open(self.filename, "a") as file:
            now = datetime.datetime.now()
            formatted_date = now.strftime("%H:%M:%S")
            msg = f'{entry} || {formatted_date}'
            file.write(msg + '\n')
            if verbose:
                print(msg)


class MySuperServer:
    def __init__(self, host, port, logger_filename='log.txt'):
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_connections = []
        self.logger = MyLogger(logger_filename)

    def port_binding(self):
        searching_port = True
        while searching_port:
            try:
                self.server_socket.bind((self.host, self.port))
                searching_port = False
            except OSError:
                self.port += 1

    def start(self):
        msg = f"Запуск сессии от {datetime.datetime.now().strftime('%Y.%m.%d')}"
        self.logger.make_an_entry(msg)
        self.server_socket = MySocket(socket.AF_INET, socket.SOCK_STREAM)
        self.port_binding()
        self.server_socket.listen(5)
        msg = f"Сервер запущен на {self.host}:{self.port}"
        self.logger.make_an_entry(msg)

        try:
            while True:
                client_socket, addr = self.server_socket.accept()
                my_client_socket = MySocket.copy(client_socket)
                client_socket.close()
                self.client_connections.append(my_client_socket)

                msg = f"Подключение клиента {addr[0]}:{addr[1]}"
                self.logger.make_an_entry(msg)
                user = self.check_user(addr[0])

                client_thread = threading.Thread(target=self.handle_client, args=(my_client_socket, user, addr[0]))
                client_thread.start()
        except KeyboardInterrupt:
            self.stop()

    def add_user(self, name, password, address):
        with open('users.json', 'r') as file:
            data = json.load(file)
        salt = "random_salt_man"
        salted_password = password + salt
        hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()
        new_entry = {'name': name, 'address': address, 'password': hashed_password}
        data.append(new_entry)

        with open('users.json', 'w') as f:
            json.dump(data, f)
        return new_entry

    def check_user(self, address):
        try:
            with open("users.json", "r") as file:
                users = json.load(file)
                for user in users:
                    if user['address'] == address:
                        return user
        except FileNotFoundError:
            with open("users.json", "w") as file:
                file.write('[]')

    def auth_user(self, user, password):
        salt = "random_salt_man"
        salted_password = password + salt
        hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()
        return hashed_password == user['password']

    def handle_client(self, client_socket, user, address):
        if not user:
            try:
                client_socket.send_message_with_header('REG')
                name = client_socket.receive_message_with_header()
                self.logger.make_an_entry('Received name')
                password = client_socket.receive_message_with_header()
                self.logger.make_an_entry('Received password')
                user = self.add_user(name, password, address)
                self.logger.make_an_entry('Register complete')
                client_socket.send_message_with_header(f'dobro poszhalovat, {user["name"]}')
            except ConnectionResetError:
                self.client_connections.remove(client_socket)
                client_socket.close()
                msg = "Клиент отключен"
                self.logger.make_an_entry(msg)
                return
        else:
            try:
                client_socket.send_message_with_header('CHECK')
                client_socket.send_message_with_header(f'S vozvrascheniem, {user["name"]}')
                is_success = False
                while not is_success:
                    password = client_socket.receive_message_with_header()
                    is_success = bool(self.auth_user(user, password))
                    client_socket.send_message_with_header(f'{str(is_success)}')
            except ConnectionResetError:
                self.client_connections.remove(client_socket)
                client_socket.close()
                msg = "Клиент отключен"
                self.logger.make_an_entry(msg)
                return
        while True:
            data = client_socket.receive_message_with_header()
            if not data:
                break
            client_socket.send_message_with_header(data)
            msg = f"Отправка данных клиенту: {data}"
            self.logger.make_an_entry(msg)

        self.client_connections.remove(client_socket)
        client_socket.close()
        msg = "Клиент отключен"
        self.logger.make_an_entry(msg)

    def stop(self):
        for client_socket in self.client_connections:
            client_socket.close()
        self.server_socket.close()
        msg = "Сервер остановлен"
        self.logger.make_an_entry(msg)


if __name__ == "__main__":
    server = MySuperServer("localhost", 8000)
    server.start()
