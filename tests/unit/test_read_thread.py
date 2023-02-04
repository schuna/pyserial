import time

from serial.threaded import ReaderThread

from api.protocols import ServerPrintLines, ClientPrintLines


def test_read(serial_ports):
    server = ReaderThread(serial_ports[0], ServerPrintLines)
    client = ReaderThread(serial_ports[1], ClientPrintLines)
    server.start()
    client.start()

    server_transport, server_protocol = server.connect()
    client_transport, client_protocol = client.connect()

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
    server.stop()
    client.stop()
