from examples.config import connection
from ponika.config import PonikaConfig, WireguardConfig, WireguardPeersConfig
from ponika.endpoints.wireguard.config import WireguardConfigCreatePayload
from ponika.endpoints.wireguard.peers import WireguardPeerCreateItemPayload

interface = WireguardConfigCreatePayload()
interface.id = 'wg0'
interface.enabled = False
interface.private_key = 'a' * 44
interface.listen_port = '51820'
interface.addresses = ['10.0.0.1/24']

peer = WireguardPeerCreateItemPayload()
peer.id = 'peer1'
peer.public_key = 'p' * 44
peer.allowed_ips = ['10.10.0.2/32']
peer.route_allowed_ips = True

desired_config = PonikaConfig(
    wireguard=WireguardConfig(
        config=[interface],
        peers=[WireguardPeersConfig(interface_id='wg0', items=[peer])],
    )
)

preview = connection.config.apply(
    desired_config,
    dry_run=True,
    delete_unmanaged=False,
)
print(preview.changes)

result = connection.config.apply(
    desired_config,
    delete_unmanaged=False,
)
print(result)
