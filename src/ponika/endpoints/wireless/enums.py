from enum import Enum


class Encryption(str, Enum):
    NONE = 'none'  # No encryption
    PSK = 'psk'  # WPA-PSK
    PSK2 = 'psk2'  # WPA2-PSK
    PSK_MIXED = 'psk-mixed'  # WPA/WPA2 mixed
    SAE = 'sae'  # WPA3-SAE
    SAE_MIXED = 'sae-mixed'  # WPA2/WPA3 mixed
    WPA = 'wpa'  # WPA-EAP
    WPA2 = 'wpa2'  # WPA2-EAP
    OWE = 'owe'  # OWE
    WPA3_MIXED = 'wpa3-mixed'  # WPA2/WPA3-EAP mixed
    WPA3 = 'wpa3'  # WPA3-EAP


class Cipher(str, Enum):
    AUTO = 'auto'
    CCMP = 'psk'
    TKIP = 'tkip'
    TKIP_CCMP = 'tkip+ccmp'


class WifiMode(str, Enum):
    ACCESSPOINT = 'ap'
    CLIENT = 'sta'
    MESH = 'mesh'
    MULTI_ACCESSPOINT = 'multi_ap'


class WifiDeviceBand(str, Enum):
    GHZ_2_4 = '2.4GHz'
    GHZ_5 = '5GHz'
