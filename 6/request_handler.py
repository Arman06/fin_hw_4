import os
from datetime import datetime
from MyLogger import MyLogger


class RequestHandler:
    def __init__(self, request_data, working_directory, address):
        self.request_data = request_data
        self.working_directory = working_directory
        self.logger = MyLogger('log.txt')
        self.address = address

    def handle_request(self):
        request_lines = self.request_data.split("\r\n")
        request_method, request_path, _ = request_lines[0].split(" ")
        if request_method == "GET":
            if request_path == "/":
                request_path = "/index.html"

            file_path = os.path.join(self.working_directory, request_path.strip("/"))

            # потому что при открытии в браузере выдавал ошибку
            if request_path == '/favicon.ico':
                return self.generate_error_response(501)

            if os.path.isfile(file_path):
                response = self.generate_success_response(file_path)
            else:
                response = self.generate_error_response(404)
        else:
            response = self.generate_error_response(501)

        return response

    def generate_success_response(self, file_path):
        file_extension = os.path.splitext(file_path)[1]
        content_type = self.get_content_type(file_extension)
        date = datetime.now().strftime('%a, %d %b %Y %H:%M:%S')
        try:
            with open(file_path, "rb") as file:
                file_data = file.read()

            response_headers = [
                b"HTTP/1.1 200 OK",
                b"Date: " + date.encode('utf-8'),
                b"Content-type: " + content_type.encode("utf-8"),
                b"Server: SimpleWebServer",
                b"Content-length: " + str(len(file_data)).encode("utf-8"),
                b"Connection: close",
                b"",
            ]
            self.logger.make_an_entry(f'{date} || {content_type} || {self.address} || '
                                      f'{os.path.splitext(file_path)[0]} || 200 OK')
            response = b"\r\n".join(response_headers) + b"\r\n" + file_data
        except IOError:
            response = self.generate_error_response(500)

        return response

    def generate_error_response(self, error_code):
        error_messages = {
            400: "400 Bad Request",
            404: "404 Not Found",
            500: "500 Internal Server Error",
            501: "501 Not Implemented",
            403: "403 Forbidden",
        }
        date = datetime.now().strftime('%a, %d %b %Y %H:%M:%S')

        response = f"HTTP/1.1 {error_messages[error_code]}\r\n"
        response += f"Date: {date.encode('utf-8')}\r\n"
        response += f"Content-type: text/html\r\n"
        response += f"Server: SimpleWebServer\r\n"
        response += f"Connection: close\r\n"
        response += f"\r\n"
        response += f"<h1>{error_messages[error_code]}</h1>"
        self.logger.make_an_entry(f'{date} || text/html || {self.address} || {error_messages[error_code]}')
        return response.encode()

    def get_content_type(self, file_extension):
        content_types = {
            ".html": "text/html",
            ".css": "text/css",
            ".js": "text/javascript",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
        }

        return content_types.get(file_extension, "application/octet-stream")



