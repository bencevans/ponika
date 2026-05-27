from enum import Enum


class RoutingType(str, Enum):
    UNICAST = 'unicast'
    LOCAL = 'local'
    BROADCAST = 'broadcast'
    MULTICAST = 'multicast'
    UNREACHABLE = 'unreachable'
    PROHIBIT = 'prohibit'
    BLACKHOLE = 'blackhole'
    ANYCAST = 'anycast'
