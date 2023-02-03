import logging

import pytest
from serial import Serial


@pytest.fixture
def serial(mock_serial):
    logging.info("Setup...")
    s = Serial(mock_serial.port, timeout=1)
    yield s
    logging.info("Tear down ...")
    s.close()


@pytest.fixture
def bytes_0to256():
    return bytes(bytearray(range(32)))


@pytest.fixture
def stub(mock_serial, bytes_0to256):
    mock_serial.stub(
        receive_bytes=bytes_0to256[:16],
        send_bytes=bytes_0to256[:16])
    mock_serial.stub(
        receive_bytes=bytes_0to256[16:32],
        send_bytes=bytes_0to256[16:32])
    yield


@pytest.fixture
def stub_print_lines(mock_serial):
    mock_serial.stub(
        receive_bytes="hello world".encode('utf-8', 'replace') + b'\r\n',
        send_bytes="hello world".encode('utf-8', 'replace') + b'\r\n')
    mock_serial.stub(
        receive_bytes="hello".encode('utf-8', 'replace') + b'\r\n',
        send_bytes="hello".encode('utf-8', 'replace') + b'\r\n')
    yield
