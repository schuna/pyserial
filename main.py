from dependency_injector.wiring import inject, Provide
from serial.threaded import ReaderThread

from api.container import Container
from api.protocols import protocol_scenario
from api.threads import SerialReader, Observer


@inject
def main(
        server: SerialReader = Provide[Container.server_thread],
        client: ReaderThread = Provide[Container.client_thread]
):
    server.start()
    client.start()
    Observer(1, server)

    server_transport, server_protocol = server.connect()
    client_transport, client_protocol = client.connect()

    protocol_scenario(client_protocol, server_protocol)

    server.stop()
    client.stop()


if __name__ == '__main__':
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])
    main()
