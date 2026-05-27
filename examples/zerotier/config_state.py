from examples.config import connection
from ponika.config import (
    PonikaConfig,
    ZerotierConfig,
    ZerotierNetworksConfig,
)
from ponika.endpoints.zerotier.config import ZerotierConfigCreatePayload
from ponika.endpoints.zerotier.networks import (
    ZerotierNetworkConfigCreatePayload,
)

controller = ZerotierConfigCreatePayload()
controller.enabled = True
controller.name = 'main_zt'

network = ZerotierNetworkConfigCreatePayload()
network.enabled = True
network.name = 'office'
network.allow_managed = True
network.allow_default = False
network.allow_global = False
network.network_id = '8d2e657774097d36'

desired_config = PonikaConfig(
    zerotier=ZerotierConfig(
        config=[controller],
        networks=[ZerotierNetworksConfig(config_id='1', items=[network])],
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
