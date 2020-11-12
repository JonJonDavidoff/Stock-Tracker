import threading
import time
from datetime import datetime


class Log:
    __logInstance__ = None

    def __init__(self):
        Log.__logInstance__ = self
        current_time = datetime.now()
        self._time_stamp = str("[") + str(current_time.strftime("%d-%m-%Y")) + ", " + str(
            current_time.strftime("%H%M")) + str(
            "]")
        self._file = open(
            "C:/Users/jonjo/OneDrive/Desktop/Stock-Tracker/Stock-Tracker/log_files/" + self._time_stamp + "_log.txt",
            'w')
        self._file.close()
        self._file = "C:/Users/jonjo/OneDrive/Desktop/Stock-Tracker/Stock-Tracker/log_files/" + self._time_stamp + "_log.txt"

    @staticmethod
    def get_log():
        if not Log.__logInstance__:
            with threading.Lock():
                if not Log.__logInstance__:
                    return Log()
        else:
            return Log.__logInstance__

    def get_time_stamp(self):
        current_time = datetime.now()
        return str("[") + str(current_time.strftime("%d-%m-%Y")) + ", " + str(
            current_time.strftime("%H%M")) + str(
            "]")

    def log(self, file_name, function_name, exception):
        with threading.Lock():
            with open(self._file, 'a') as file:
                file.write(
                    '\n ' + self.get_time_stamp() + ', file_name=  ' + file_name + ', function_name= ' + function_name + ', exception= ' + exception)
                print('Logged')
