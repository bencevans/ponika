from examples.config import connection
from ponika.endpoints.wireguard.config import WireguardConfigCreatePayload

response = connection.wireguard.config.create(
    WireguardConfigCreatePayload(
        id='wg0',
        enabled=False,
        private_key='a' * 44,
        listen_port='51820',
        addresses=['10.0.0.1/24'],
    )
)

print(type(response))
print(response)
