import datetime


class MyLogger:
    def __init__(self, filename):
        self.filename = filename

    def make_an_entry(self, entry, verbose=False):
        with open(self.filename, "a") as file:
            now = datetime.datetime.now()
            formatted_date = now.strftime("%H:%M:%S")
            msg = f'{entry} || {formatted_date}'
            file.write(msg + '\n')
            if not verbose:
                print(msg)
