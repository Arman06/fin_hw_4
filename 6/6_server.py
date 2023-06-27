import socket
import threading
from request_handler import RequestHandler


class WebServer:
    def __init__(self, host, port, max_request_size, working_directory):
        self.host = host
        self.port = port
        self.max_request_size = max_request_size
        self.working_directory = working_directory
        self.server_socket = None
        self.is_running = False

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # чтоб быстренько перезапустить и не менять порт в конфиге каждый божий раз
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        self.is_running = True
        print(f"Server started on {self.host}:{self.port}")

        while self.is_running:
            client_socket, client_address = self.server_socket.accept()
            print(f"New connection from {client_address[0]}:{client_address[1]}")

            client_thread = threading.Thread(target=self.handle_client_request, args=(client_socket, client_address[0]))
            client_thread.start()

    def stop(self):
        self.is_running = False
        self.server_socket.close()
        print("Server stopped")

    def handle_client_request(self, client_socket, address):
        request_data = client_socket.recv(self.max_request_size).decode("utf-8")
        request_handler = RequestHandler(request_data, self.working_directory, address)
        response = request_handler.handle_request()
        client_socket.sendall(response)
        client_socket.close()


def read_config_file(config_file):
    config = {}
    with open(config_file, "r") as file:
        for line in file:
            key, value = line.strip().split("=")
            config[key.strip()] = value.strip()
    return config


def main():
    config = read_config_file("config.txt")

    host = config.get("HOST", "localhost")
    port = int(config.get("PORT", 8000))
    max_request_size = int(config.get("MAX_REQUEST_SIZE", 1024))
    working_directory = config.get("WORKING_DIRECTORY", ".")

    server = WebServer(host, port, max_request_size, working_directory)
    server.start()


if __name__ == "__main__":
    main()
