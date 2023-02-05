from api.protocols import protocol_scenario


def test_read(transports):
    server = transports[0]
    client = transports[1]
    server.start()
    client.start()

    server_transport, server_protocol = server.connect()
    client_transport, client_protocol = client.connect()

    protocol_scenario(client_protocol, server_protocol)

    server.stop()
    client.stop()
