import logging.config
from dependency_injector import containers, providers
from serial import Serial
from serial.threaded import ReaderThread

from api.protocols import ServerPrintLines, ClientPrintLines
from api.threads import SerialReader, Observer


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(json_files=["config.json"])
    logging = providers.Resource(
        logging.config.fileConfig,
        fname="logging.ini"
    )

    serial_a = providers.Factory(
        Serial,
        port="COM6",
        baudrate=config.server.baudrate,
        timeout=config.server.timeout
    )

    serial_b = providers.Factory(
        Serial,
        port="COM7",
        baudrate=config.client.baudrate,
        timeout=config.client.timeout
    )

    server_thread = providers.Factory(
        SerialReader,
        serial_instance=serial_a,
        protocol_factory=ServerPrintLines
    )

    client_thread = providers.Factory(
        ReaderThread,
        serial_instance=serial_b,
        protocol_factory=ClientPrintLines
    )

