import os
import shutil
from pathlib import Path


class FileManager:
    def root_check_challenge(self, boring_path):
        cool_path = self.path.joinpath(boring_path).resolve()
        if cool_path.is_relative_to(self.root):
            return True
        else:
            print("Нельзя выходить за пределы родительской директории!!!!!!!!")
            return False

    def __init__(self, path):
        self.path = Path(path).absolute()
        self.root = Path(path).absolute()
        os.chdir(self.path)
        self.files = []
        self.update_files()

    def list_commands(self):
        return """КОМАНДЫ:
        \nls - показать содержимое директории
        \ncd <path> - изменить текущую рабочую директорию на другую
        \ncopy <source> <destination> - скопировать файл по указанному пути
        \nrm <file> - удалить файл из директории
        \nmk <name> <type> - создать файл или директорию
        \nwt <file> <text> - написать текст в файл
        \nsc <file> - показать содержимое файла
        \nmv <file> <new_path> - переместить файл
        \nrn <name> <new_name> - переименовать файл
        \nrf <name> - удалить директорию (с файлами)
        \ncwd - вывести текущую рабочую директорию
        \nexit - выйти из программы"""

    def execute_commands(self, command):
        command = command.split()

        if command[0] == "ls":
            if len(command) == 1:
                return self.show_files()
            elif len(command) == 2:
                return self.show_file_contents(command[1])
            else:
                return "Неверная команда или аргументы"
        elif command[0] == "cd":
            if len(command) == 2:
                return self.change_dir(command[1])
            else:
                return "Неверная команда или аргументы (нужен один)"
        elif command[0] == "copy":
            if len(command) == 3:
                return self.copy_file(command[1], command[2])
            else:
                return "Неверная команда или аргументы (нужно два аргумента)"
        elif command[0] == "rm":
            if len(command) == 2:
                return self.delete_file(command[1])
            else:
                return "Неверная команда или аргументы"
        elif command[0] == "mk":
            if len(command) == 3 and command[2] in ["file", "dir"]:
                return self.create_file_or_dir(command[1], command[2])
            else:
                return "Неверная команда или аргументы"
        elif command[0] == "wt":
            if len(command) >= 3:
                file = command[1]
                text = " ".join(command[2:])
                return self.write_to_file(file, text)
            else:
                return "Неверная команда или аргументы"
        elif command[0] == "sc":
            if len(command) == 2:
                return self.show_file_contents(command[1])
            else:
                return "Неверная команда или аргументы"
        elif command[0] == "mv":
            if len(command) == 3:
                return self.move_file(command[1], command[2])
            else:
                return "Неверная команда или аргументы"
        elif command[0] == "rn":
            if len(command) == 3:
                return self.rename_file_or_dir(command[1], command[2])
            else:
                return "Неверная команда или аргументы"
        elif command[0] == "rf":
            if len(command) == 2:
                return self.remove_folder(command[1])
            else:
                return "Неверная команда или аргументы"
        elif command[0] == "cwd":
            return self.cwd()
        else:
            print(f"Неверная команда или аргументы")

    def update_files(self):
        self.files = sorted(os.listdir(self.path))

    def show_files(self):
        msg = ''
        msg += f"Файлы и директории в {self.path}:\n"
        for i, file in enumerate(self.files):
            msg += f"{i + 1}. {file}\n"
        return msg

    def change_dir(self, new_path):
        try:
            if new_path == '..':
                requested_path = Path.cwd().parent
            elif new_path == '.':
                requested_path = self.root
            else:
                requested_path = self.path.joinpath(new_path).resolve()
            if requested_path.is_relative_to(self.root):
                os.chdir(requested_path)
                self.path = Path.cwd()
                self.update_files()
                return f"Меняем директорию на {requested_path}"
            else:
                os.chdir(Path(self.path).absolute())
                return "Айайай, нельзя выходить за пределы родительской директории"

        except FileNotFoundError as e:
            print(e)
            return f"Неправильный путь: {new_path}"

    def copy_file(self, source, destination):
        if not self.root_check_challenge(destination):
            return
        if not self.root_check_challenge(source):
            return
        try:
            if destination == '.':
                destination = self.path
            shutil.copy(source, destination)
            return f"Скопировал {source} в {destination}"
        except FileNotFoundError:
            print(f"Неверный исходный путь или конечный: {source}, {destination}")

    def delete_file(self, file):
        if not self.root_check_challenge(file):
            return
        try:
            os.remove(file)
            self.update_files()
            return f"Удален {file}"
        except FileNotFoundError:
            return f"Неверный файл: {file}"

    def create_file_or_dir(self, name, type):
        if type == "file":
            try:
                open(name, "w").close()
                self.update_files()
                return f"Создан {name}"
            except OSError:
                return f"Неверное имя: {name}"

        elif type == "dir":
            try:
                os.mkdir(name)
                self.update_files()
                return f"Создана директория {name}"
            except OSError:
                return f"Неверное имя: {name}"

    def write_to_file(self, file, text):
        try:
            with open(file, "w") as f:
                f.write(text)
            return f"Записал в файл {file}"
        except FileNotFoundError:
            return f"Неверный файл: {file}"

    def show_file_contents(self, file):
        try:
            with open(file, "r") as f:
                contents = f.read()
            msg = ''
            msg += f"Содержимое {file}:\n"
            msg += contents
            return msg
        except FileNotFoundError:
            return f"Неверный файл: {file}"

    def move_file(self, file, new_path):
        if not self.root_check_challenge(new_path):
            return
        try:
            shutil.move(file, new_path)
            self.update_files()
            return f"Переместил файл {file} в {new_path}"

        except FileNotFoundError:
            return f"Неверный файл или путь: {file}, {new_path}"

    def rename_file_or_dir(self, name, new_name):
        try:
            os.rename(name, new_name)
            self.update_files()
            return f"Переименовал {name} в {new_name}"
        except FileNotFoundError:
            return f"Неверное имя или новое имя: {name}, {new_name}"

    def remove_folder(self, folder):
        try:
            shutil.rmtree(folder)
            self.update_files()
            return f"Удалил директорию {folder}"
        except FileNotFoundError:
            return f"Неверная директория: {folder}"

    def upload_file(self, client_socket, file_name):
        file_size = int(client_socket.receive_message_with_header())
        client_socket.send_message_with_header("ReadyUp")

        try:
            with open(file_name, "wb") as file:
                received = 0
                while received < file_size:
                    data = client_socket.receive_message_with_header_without_decode()
                    file.write(data)
                    received += len(data)
            client_socket.send_message_with_header(f"Файл '{file_name}' загружен успешно.")
        except Exception as e:
            client_socket.send_message_with_header(f"Ошибка при загрузке: {str(e)}")

    def download_file(self, client_socket, file_name):

        try:
            with open(file_name, "rb") as file:
                file_data = file.read()
            file_len = len(file_data)
            client_socket.send_message_with_header('ReadyDown')
            client_socket.send_message_with_header(file_name)
            client_socket.send_message_with_header(str(file_len))
            ready = client_socket.client_socket.receive_message_with_header()
            if ready == "ReadyDown":
                while file_len > 0:
                    client_socket.send_message_with_header_without_encode(file_data[:client_socket.HEADER])
                    file_len -= client_socket.HEADER
        except Exception as e:
            client_socket.send_message_with_header(f"Ошибка при скачивании: {str(e)}")

    def cwd(self):
        return Path.cwd()


def main():
    try:
        with open("settings.txt", "r") as f:
            path = f.read().strip()
    except FileNotFoundError:
        path = os.getcwd()

    print(path)
    fm = FileManager(path)

    print("КОМАНДЫ:")
    print("ls - показать содержимое директрии")
    print("cd <path> - изменить текущую рабочую директорию на другую")
    print("copy <source> <destination> - скопировать файл по указанному пути")
    print("rm <file> - удалить файл из директории")
    print("mk <name> <type> - создать файл или директорию")
    print("wt <file> <text> - написать текст в файл")
    print("sc <file> - показать содержимое файла")
    print("mv <file> <new_path> - переместить файл")
    print("rn <name> <new_name> - переименовать файл")
    print("rf <name> - удалить директорию (с файлами)")
    print("cwd - вывести текущую рабочую директорию")
    print("exit - выйти из программы")

    while True:
        command = input('ты тут --> ' + str(fm.path) + '\n> ').split()

        if command[0] == "ls":
            if len(command) == 1:
                fm.show_files()
            elif len(command) == 2:
                fm.show_file_contents(command[1])
            else:
                print("Неверная команда или аргументы")
        elif command[0] == "cd":
            if len(command) == 2:
                fm.change_dir(command[1])
            else:
                print("Неверная команда или аргументы (нужен один)")
        elif command[0] == "copy":
            if len(command) == 3:
                fm.copy_file(command[1], command[2])
            else:
                print("Неверная команда или аргументы (нужно два аргумента)")
        elif command[0] == "rm":
            if len(command) == 2:
                fm.delete_file(command[1])
            else:
                print("Неверная команда или аргументы")
        elif command[0] == "mk":
            if len(command) == 3 and command[2] in ["file", "dir"]:
                fm.create_file_or_dir(command[1], command[2])
            else:
                print("Неверная команда или аргументы")
        elif command[0] == "wt":
            if len(command) >= 3:
                file = command[1]
                text = " ".join(command[2:])
                fm.write_to_file(file, text)
            else:
                print("Неверная команда или аргументы")
        elif command[0] == "sc":
            if len(command) == 2:
                fm.show_file_contents(command[1])
            else:
                print("Неверная команда или аргументы")
        elif command[0] == "mv":
            if len(command) == 3:
                fm.move_file(command[1], command[2])
            else:
                print("Неверная команда или аргументы")
        elif command[0] == "rn":
            if len(command) == 3:
                fm.rename_file_or_dir(command[1], command[2])
            else:
                print("Неверная команда или аргументы")
        elif command[0] == "rf":
            if len(command) == 2:
                fm.remove_folder(command[1])
            else:
                print("Неверная команда или аргументы")
        elif command[0] == "cwd":
            fm.cwd()
        elif command[0] == "exit":
            break
        else:
            print(f"Неверная команда или аргументы")


# main()
