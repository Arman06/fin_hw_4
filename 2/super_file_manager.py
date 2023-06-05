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

    def update_files(self):
        self.files = sorted(os.listdir(self.path))

    def show_files(self):
        print(f"Файлы и директории в {self.path}:")
        for i, file in enumerate(self.files):
            print(f"{i + 1}. {file}")

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
                print(f"Меняем директорию на {requested_path}")
            else:
                os.chdir(Path(self.path).absolute())
                print("Айайай, нельзя выходить за пределы родительской директории")

        except FileNotFoundError as e:
            print(e)
            print(f"Неправильный путь: {new_path}")

    def copy_file(self, source, destination):
        if not self.root_check_challenge(destination):
            return
        if not self.root_check_challenge(source):
            return
        try:
            if destination == '.':
                destination = self.path
            shutil.copy(source, destination)
            print(f"Скопировал {source} в {destination}")
        except FileNotFoundError:
            print(f"Неверный исходный путь или конечный: {source}, {destination}")

    def delete_file(self, file):
        if not self.root_check_challenge(file):
            return
        try:
            os.remove(file)
            self.update_files()
            print(f"Удален {file}")
        except FileNotFoundError:
            print(f"Неверный файл: {file}")

    def create_file_or_dir(self, name, type):
        if type == "file":
            try:
                open(name, "w").close()
                self.update_files()
                print(f"Создан {name}")
            except OSError:
                print(f"Неверное имя: {name}")

        elif type == "dir":
            try:
                os.mkdir(name)
                self.update_files()
                print(f"Создана директория {name}")
            except OSError:
                print(f"Неверное имя: {name}")

    def write_to_file(self, file, text):
        try:
            with open(file, "w") as f:
                f.write(text)
            print(f"Записал в файл {file}")
        except FileNotFoundError:
            print(f"Неверный файл: {file}")

    def show_file_contents(self, file):
        try:
            with open(file, "r") as f:
                contents = f.read()
            print(f"Содержимое {file}:")
            print(contents)
        except FileNotFoundError:
            print(f"Неверный файл: {file}")

    def move_file(self, file, new_path):
        if not self.root_check_challenge(new_path):
            return
        try:
            shutil.move(file, new_path)
            self.update_files()
            print(f"Переместил файл {file} в {new_path}")

        except FileNotFoundError:
            print(f"Неверный файл или путь: {file}, {new_path}")

    def rename_file_or_dir(self, name, new_name):
        try:
            os.rename(name, new_name)
            self.update_files()
            print(f"Переименовал {name} в {new_name}")
        except FileNotFoundError:
            print(f"Неверное имя или новое имя: {name}, {new_name}")

    def remove_folder(self, folder):
        try:
            shutil.rmtree(folder)
            self.update_files()
            print(f"Удалил директорию {folder}")
        except FileNotFoundError:
            print(f"Неверная директория: {folder}")

    def cwd(self):
        print(Path.cwd())


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


main()
