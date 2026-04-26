from ponika.endpoints import CRUDEndpoint, StatusEndpoint
from pydantic import Field
from typing import TYPE_CHECKING, List, Optional

from ponika.models import BaseModel, BasePayload

from ponika.endpoints.wireless.enums import Encryption, Cipher, WifiMode

if TYPE_CHECKING:
    pass


class WirelessInterfaceBase:
    encryption: Encryption | str = Encryption.PSK2
    key: Optional[str] = None
    enabled: bool | str = True
    mode: WifiMode | str = WifiMode.ACCESSPOINT
    mesh_id: Optional[str] = None
    ssid: Optional[str] = None
    bssid: Optional[str] = None
    network: Optional[str] = 'lan'
    mesh_fwding: Optional[str] = None
    mesh_rssi_threshold: Optional[str] = None
    hidden: Optional[str] = None
    isolate: bool | str = True
    bss_transition: Optional[str] = None
    ieee80211k: Optional[str] = None
    ieee80211w: Optional[str] = None
    disassoc_low_ack: Optional[str] = None
    trm_enabled: Optional[str] = None
    cipher: Cipher | str = Cipher.AUTO
    auth_server: Optional[str] = None
    auth_port: Optional[str] = None
    auth_secret: Optional[str] = None
    acct_server: Optional[str] = None
    acct_port: Optional[str] = None
    acct_secret: Optional[str] = None
    ieee80211r: Optional[str] = None
    nasid: Optional[str] = None
    mobility_domain: Optional[str] = None
    reassociation_deadline: Optional[str] = None
    ft_over_ds: Optional[str] = None
    eap_type: Optional[str] = None
    use_pkcs: Optional[str] = None
    pkcs_cert: Optional[str] = None
    pkcs_passwd: Optional[str] = None
    ca_cert: Optional[str] = None
    client_cert: Optional[str] = None
    priv_key: Optional[str] = None
    priv_key_pwd: Optional[str] = None
    auth: Optional[str] = None
    ca_cert2: Optional[str] = None
    client_cert2: Optional[str] = None
    priv_key2: Optional[str] = None
    priv_key2_pwd: Optional[str] = None
    identity: Optional[str] = None
    anonymous_identity: Optional[str] = None
    password: Optional[str] = None
    macfilter: Optional[str] = None
    maclist: List[str] = Field(default_factory=list)
    delete_from_whitelist: Optional[str] = None
    short_preamble: Optional[str] = None
    dtim_period: Optional[str] = None
    wpa_group_rekey: Optional[str] = None
    skip_inactivity_poll: Optional[str] = None
    max_inactivity: Optional[str] = None
    max_listen_interval: Optional[str] = None
    device_files: Optional[str] = None
    device_files2: Optional[str] = None
    wds: Optional[str] = None
    wmm: Optional[str] = None
    scan_time: Optional[str] = None
    auto_reconnect: Optional[str] = None


class WirelessInterfaceConfigResponse(BaseModel, WirelessInterfaceBase):
    key_set: Optional[str] = Field(
        serialization_alias='key:set', exclude=True, default=None
    )
    auth_secret_set: Optional[str] = Field(
        serialization_alias='auth_secret:set', exclude=True, default=None
    )
    acct_secret_set: Optional[str] = Field(
        serialization_alias='acct_secret:set', exclude=True, default=None
    )
    password_set: Optional[str] = Field(
        serialization_alias='password:set', exclude=True, default=None
    )
    pkcs_passwd_set: Optional[str] = Field(
        serialization_alias='pkcs_passwd:set', exclude=True, default=None
    )
    priv_key_pwd_set: Optional[str] = Field(
        serialization_alias='priv_key_pwd:set', exclude=True, default=None
    )
    priv_key2_pwd_set: Optional[str] = Field(
        serialization_alias='priv_key2_pwd:set', exclude=True, default=None
    )


class WirelessInterfaceCreatePayload(BasePayload, WirelessInterfaceBase): ...


class WirelessInterfaceUpdatePayload(BasePayload, WirelessInterfaceBase):
    id: int


class WirelessInterfacesDeleteResponse(BaseModel):
    # deleted interface
    id: str


class WirelessInterfacesStatusResponse(BaseModel):
    """Data model for wireless interfaces response."""

    class Client(BaseModel):
        """Data model for wireless client information."""

        expires: Optional[int] = None
        band: str
        ipaddr: Optional[str] = None
        hostname: Optional[str] = None
        tx_rate: int
        macaddr: str
        rx_rate: int
        signal: str
        interface: Optional[str] = None
        device: str

    id: str
    wifi_id: str
    ifname: str

    encryption: str
    # differs from docs says is required
    vht_supported: Optional[bool] = None
    num_assoc: int
    clients: List[Client] = Field(default_factory=list)
    status: str
    mode: Optional[str] = None
    multiple: Optional[bool] = None
    # ht_supported: bool
    ssid: str
    # conf_id: str
    # auth_status: int


class InterfacesEndpoint(
    CRUDEndpoint[
        WirelessInterfaceCreatePayload,
        WirelessInterfaceConfigResponse,
        WirelessInterfaceUpdatePayload,
        WirelessInterfacesDeleteResponse,
    ],
    StatusEndpoint[WirelessInterfacesStatusResponse],
):
    endpoint_path = '/wireless/interfaces/config'
    status_endpoint_path = '/wireless/interfaces/status'

    config_response_model = WirelessInterfaceConfigResponse
    create_model = WirelessInterfaceCreatePayload
    update_model = WirelessInterfaceUpdatePayload

    delete_reponse_model = WirelessInterfacesDeleteResponse
    status_response_model = WirelessInterfacesStatusResponse
