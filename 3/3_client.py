import socket
from MySuperSocket import MySocket


class MySuperClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None

    def connect(self):
        self.client_socket = MySocket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        print(f"Соединение с сервером {self.host}:{self.port}")

    def send_message(self, message):
        self.client_socket.send_message_with_header(message)

    def receive_message(self):
        return self.client_socket.receive_message_with_header()

    def disconnect(self):
        self.client_socket.close()
        print("Разрыв соединения с сервером")

    def start(self):
        self.connect()
        first_message = self.receive_message()
        if first_message == 'REG':
            print("Вам нужно пройти регистрацию :((")
            name = input("Имя: ")
            self.send_message(name)
            password = input("Пароль (он будет захеширован): ")
            self.send_message(password)
            greeting_message = self.receive_message()
            print(greeting_message)
        elif first_message == 'CHECK':
            greeting_message = self.receive_message()
            print(greeting_message)
            is_success = False
            while not is_success:
                password = input('Введите пароль:')
                self.send_message(password)
                received = self.receive_message()
                if received == 'False':
                    print('Неверный пароль!!!!!!!!!')
                    is_success = False
                elif received == 'True':
                    print('ВСЕ ОК')
                    is_success = True

        try:
            while True:
                message = input("Введите сообщение для отправки серверу: ")
                self.send_message(message)
                print(f"Отправка данных серверу: {message}")
                data = self.receive_message()
                print(f"Cервер: {data}")
        except KeyboardInterrupt:
            pass

        self.client_socket.disconnect()


if __name__ == "__main__":
    client = MySuperClient("localhost", 8000)
    client.start()
