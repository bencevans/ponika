from examples.config import connection
from ponika.endpoints.wireguard.config import WireguardConfigUpdatePayload

response = connection.wireguard.config.update(
    WireguardConfigUpdatePayload(
        id='wg0',
        enabled=False,
        private_key='a' * 44,
        metric='10',
    )
)

print(type(response))
print(response)
