import logging

import pytest
from dependency_injector.wiring import Provide, inject
from serial.threaded import ReaderThread

from api.container import Container
from api.threads import SerialReader


@pytest.fixture
def container():
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])
    yield container


@inject
def get_transports(
        server: SerialReader = Provide[Container.server_thread],
        client: ReaderThread = Provide[Container.client_thread]):
    return server, client


@pytest.fixture
def transports(container):
    server, client = get_transports()
    logging.info("Setup transports")
    yield server, client
    logging.info("Teardown transports")
    server.close()
    client.close()
