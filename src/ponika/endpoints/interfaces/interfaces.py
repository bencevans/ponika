from typing import List, Optional

from pydantic import Field

from ponika.models import BaseModel


class InterfaceConfigResponseDataItem(BaseModel):
    """Data model for wireless interface configuration response."""

    id: str
    name: str
    enabled: Optional[str] = None
    proto: Optional[str] = None
    ipaddr: Optional[str] = None
    netmask: Optional[str] = None
    gateway: Optional[str] = None
    broadcast: Optional[str] = None
    broadcast_dhcp: Optional[str] = None
    auth: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    ac: Optional[str] = None
    service: Optional[str] = None
    reqaddress: Optional[str] = None
    reqprefix: Optional[str] = None
    hostname: Optional[str] = None
    method: Optional[str] = None
    pdptype: Optional[str] = None
    sim: Optional[str] = None
    esim_profile: Optional[str] = None
    auto_apn: Optional[str] = None
    apn: Optional[str] = None
    passthrough_mode: Optional[str] = None
    framed_routing: Optional[str] = None
    leasetime: Optional[str] = None
    dns: List[str] = Field(default_factory=list)
    delegate: Optional[str] = None
    force_link: Optional[str] = None
    ipv6: Optional[str] = None
    defaultroute: Optional[str] = None
    metric: Optional[str] = None
    ip6prefix: Optional[str] = None
    clientid: Optional[str] = None
    vendorid: Optional[str] = None
    keepalive_failure: Optional[str] = None
    keepalive_interval: Optional[str] = None
    host_uniq: Optional[str] = None
    demand: Optional[str] = None
    mac: Optional[str] = None
    macaddr: Optional[str] = None
    mtu: Optional[str] = None
    ip4table: Optional[str] = None
    ip6table: Optional[str] = None
    ip6assign: Optional[str] = None
    ip6hint: Optional[str] = None
    ip6addr: Optional[str] = None
    ip6gw: Optional[str] = None
    ip6ifaceid: Optional[str] = None
    bridge: Optional[str] = None
    stp: Optional[str] = None
    igmp_snooping: Optional[str] = None
    ifname: List[str] = Field(default_factory=list)
    fiber_priority: Optional[str] = None
    tag: Optional[str] = None
    priority: Optional[str] = None
    fwzone: Optional[str] = None
    p2p: Optional[str] = None
    area_type: Optional[str] = None
    password_set: Optional[str] = Field(default=None, alias='password:set')
