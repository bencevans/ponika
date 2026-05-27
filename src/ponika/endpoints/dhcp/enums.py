from enum import Enum


class DHCPMode(str, Enum):
    SERVER = 'server'
    RELAY = 'relay'
