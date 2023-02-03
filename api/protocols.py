import sys
import traceback
from serial.threaded import LineReader


class PrintLines(LineReader):
    def connection_made(self, transport):
        super(PrintLines, self).connection_made(transport)
        sys.stdout.write('port opened\n')
        self.write_line('hello world')

    def handle_line(self, data):
        sys.stdout.write('line received: {!r}\n'.format(data))

    def connection_lost(self, exc):
        if exc:
            traceback.print_exc(exc)
        sys.stdout.write('port closed\n')
