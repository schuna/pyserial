import logging
import time

import pytest
from serial import Serial
from mock_serial import MockSerial
from retry import retry as retry_call

from api.utils import chunks


def retry(fn):
    retry_call(tries=9, delay=1, logger=None)(fn)()


def test_open_close(
        caplog,
):
    mock_serial = MockSerial()
    caplog.set_level(logging.DEBUG)

    mock_serial.open()
    assert 'Attached to mock serial port.' in caplog.text

    mock_serial.close()
    assert 'Detaching mock serial port.' in caplog.text
    assert 'Detached mock serial port.' in caplog.text
    assert 'Closing mock serial port.' in caplog.text
    assert 'Closed mock serial port.' in caplog.text

    with pytest.raises(OSError):
        Serial(mock_serial.port)


def test_stub_assert(
        caplog,
        mock_serial,
):
    caplog.set_level(logging.DEBUG)

    stub = mock_serial.stub(
        name='foo',
        receive_bytes=b'123',
        send_bytes=b'456'
    )

    serial = Serial(mock_serial.port, timeout=1)
    serial.write(b'123')

    def lazy_logger_assertions():
        assert "Buffer read: b'123'." in caplog.text
        assert "Match stub: b'123' => b'456'." in caplog.text
        assert "Buffer write: b'456'." in caplog.text

    assert serial.read(3) == b'456'
    retry(lazy_logger_assertions)

    assert stub == mock_serial.stubs['foo']
    assert stub.called
    assert stub.calls == 1


def test_non_blocking(
        caplog,
        serial
):
    assert serial.read(1).decode() == ""
    print(caplog.text)


def test_loop_back(
        stub,
        serial,
        bytes_0to256):
    for chunk in chunks(bytes_0to256):
        length = len(chunk)
        serial.write(chunk)
        time.sleep(0.05)
        assert serial.in_waiting == length
        assert serial.read(length) == chunk

    assert serial.read(1).decode() == ""
