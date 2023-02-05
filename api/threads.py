from serial.threaded import ReaderThread


class SerialReader(ReaderThread):
    def __init__(self, serial_instance, protocol_factory):
        super().__init__(serial_instance, protocol_factory)
        self.__observers: list[Observer] = []

    def register(self, observer):
        self.__observers.append(observer)

    def notify(self, *args, **kwargs):
        for observer in self.__observers:
            observer.notify(*args, **kwargs)


class Observer:
    def __init__(self, observer_id: int, server: SerialReader):
        self.observer_id = observer_id
        server.register(self)

    def notify(self, *args, **kwargs):
        print(f"Observer {self.observer_id} got {args}, {kwargs}")