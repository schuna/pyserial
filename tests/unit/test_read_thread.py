import time

from serial.threaded import ReaderThread

from api.protocols import PrintLines


def test_read(
        stub_print_lines,
        serial):
    thread = ReaderThread(serial, PrintLines)
    thread.start()
    transport, protocol = thread.connect()
    protocol.write_line("hello")
    time.sleep(2)
    thread.close()
