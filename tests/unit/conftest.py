import pytest
from serial import Serial

PORT_A = "COM6"
PORT_B = "COM7"


@pytest.fixture
def serial_ports():
    print("Setup Ports")
    server = Serial(port=PORT_A, baudrate=115200, timeout=5)
    client = Serial(port=PORT_B, baudrate=115200, timeout=5)

    yield server, client
    print("Tear down Ports")
    server.close()
    client.close()
