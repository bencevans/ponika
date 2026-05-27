from examples.config import connection
from ponika.config import PonikaConfig, WirelessConfig
from ponika.endpoints.wireless.interfaces import WirelessInterfaceCreatePayload

interface = WirelessInterfaceCreatePayload()
interface.ssid = 'Example-SSID'
interface.key = 'Wifi-Key'

desired_config = PonikaConfig(wireless=WirelessConfig(interfaces=[interface]))

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
