import sys
import time
import traceback
from typing import Callable, Union

from serial.threaded import LineReader


def get_func(key: str, value: str = None) -> str:
    if key in dataset.keys():
        return dataset[key]
    return ""


def set_func(key: str, value: str) -> str:
    if key in dataset.keys():
        dataset[key] = value
        return value
    return ""


cmds = {
    "get": get_func,
    "set": set_func
}

dataset = {
    "1": "100",
    "2": "200",
}


def get_cmd(key: str) -> Union[None, Callable]:
    if key in cmds.keys():
        return cmds[key]
    return None


def get_args(parameter: str) -> list[str]:
    return parameter.split(',')


class ServerPrintLines(LineReader):
    def connection_made(self, transport):
        super(ServerPrintLines, self).connection_made(transport)
        sys.stdout.write('serer port opened\n')
        self.write_line('hello client')

    def handle_line(self, data):
        sys.stdout.write('server received: {!r}\n'.format(data))
        data_split = data.split(' ')
        if len(data_split) > 1:
            cmd = get_cmd(data_split[0])
            if cmd:
                args = get_args(data_split[1])
                result = cmd(args[0], args[1])
                sys.stdout.write(f'server send: {result!r}\n')
                self.write_line(f'{result}')

    def connection_lost(self, exc):
        if exc:
            traceback.print_exc(exc)
        sys.stdout.write('server port closed\n')


class ClientPrintLines(LineReader):
    def connection_made(self, transport):
        super(ClientPrintLines, self).connection_made(transport)
        sys.stdout.write('client port opened\n')
        self.write_line('hello server')

    def handle_line(self, data):
        sys.stdout.write('client received: {!r}\n'.format(data))

    def connection_lost(self, exc):
        if exc:
            traceback.print_exc(exc)
        sys.stdout.write('client port closed\n')


def protocol_scenario(client_protocol, server_protocol):
    client_protocol.write_line("get 1,1")
    time.sleep(1)
    client_protocol.write_line("set 1,150")
    time.sleep(1)
    client_protocol.write_line("get 1,1")
    time.sleep(1)
    client_protocol.write_line("get 2,1")
    time.sleep(1)
    server_protocol.write_line("bye")
    time.sleep(1)
    client_protocol.write_line("bye")