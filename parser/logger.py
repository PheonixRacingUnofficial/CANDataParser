class Logger:

    def __init__(self, is_debug: bool, is_log: bool):
        self.is_debug = is_debug
        self.is_log = is_log

    def get_debug(self) -> bool:
        return self.is_debug

    def get_log(self) -> bool:
        return self.is_log

    def info(self, message) -> None:
        if type(message) == list:
            for msg in message:
                print(f"[INFO] / {msg}")
        else:
            print(f"[INFO / {message}")

    def debug(self, message) -> None:
        if self.is_debug:
            if type(message) == list:
                for msg in message:
                    print(f"[DEBUG] {msg}")
            else:
                print(f"[DEBUG] {message}")

    def python_error(self, message) -> None:
        if type(message) == list:
            for msg in message:
                print(f"[PYTHON ERROR] {msg}")
        else:
            print(f"[PYTHON ERROR] {message}")

    def data_error(self, message) -> None:
        if type(message) == list:
            for msg in message:
                print(f"[DATA ERROR] {msg}")
        else:
            print(f"[DATA ERROR] {message}")

    def value_error(self, message) -> None:
        if type(message) == list:
            for msg in message:
                print(f"[VALUE ERROR] {msg}")
        else:
            print(f"[VALUE ERROR] {message}")

    def sensor_error(self, message) -> None:
        if type(message) == list:
            for msg in message:
                print(f"[SENSOR ERROR / {msg}")
        else:
            print(f"[SENSOR ERROR /  {message}")
