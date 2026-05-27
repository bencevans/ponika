from examples.config import connection
from ponika.endpoints.wireguard.config import WireguardConfigUpdatePayload

response = connection.wireguard.config.update_bulk(
    [
        WireguardConfigUpdatePayload(
            id='wg0',
            enabled=True,
            private_key='b' * 44,
        ),
        WireguardConfigUpdatePayload(
            id='wg1',
            enabled=False,
            private_key='b' * 44,
        ),
    ]
)

print(type(response))
print(response)
