from enum import Enum


class SmsRuleAction(str, Enum):
    REBOOT = 'reboot'
    SEND_STATUS = 'send_status'
    VPN_STATUS = 'vpnstatus'
    MOBILE = 'mobile'
    CHANGE_MOBILE_SETTINGS = 'change_mobile_settings'
    RESET_CONN = 'reset_conn'
    LIST_OF_PROFILE = 'list_of_profile'
    VPN = 'vpn'
    CHANGE_PROFILE = 'change_profile'
    SSH_ACCESS = 'ssh_access'
    WEB_ACCESS = 'web_access'
    IP_UNBLOCK = 'ip_unblock'
    FIRSTBOOT = 'firstboot'
    USERDEFAULTS = 'userdefaults'
    FW_UPGRADE = 'fw_upgrade'
    MONITORING_STATUS = 'monitoring_status'
    UCI = 'uci'
    RMS_STATUS = 'rms_status'
    RMS_ACTION = 'rms_action'
    RMS_CONNECT = 'rms_connect'
    MORE = 'more'
    IO_STATUS = 'iostatus'
    IO_SET = 'io_set'
    SWITCH_SIM = 'switch_sim'
    GPS = 'gps'
    GPS_COORDINATES = 'gps_coordinates'
    WOL = 'wol'
    DATA_USAGE_RESET = 'data_usage_reset'
    DATA_LIMIT = 'data_limit'
    WIFI = 'wifi'
    EXEC = 'exec'
    CONFIG_RELOAD = 'config_reload'
    API = 'api'
    ESIM_LIST = 'esim_list'
    ESIM_CHANGE = 'esim_change'
    ESIM_INSTALL = 'esim_install'


class SmsRuleIo(str, Enum):
    DIO0 = 'dio0'
    DIO1 = 'dio1'
    DIO2 = 'dio2'
    DOUT2 = 'dout2'
    DOUT1 = 'dout1'
    RELAY1 = 'relay1'


class SmsRuleSimcard(str, Enum):
    SIM_1 = '1'
    SIM_2 = '2'


class SmsRuleMethod(str, Enum):
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    DELETE = 'delete'


class SmsRuleAclMode(str, Enum):
    ALLOWED = 'allowed'
    DENIED = 'denied'


class SmsRuleAuthorization(str, Enum):
    NO_AUTHORIZATION = 'no'
    SERIAL = 'serial'  # Serial
    PASSWORD = 'password'  # Router Admin Password
    LOCAL = 'local'  # Custom password


class SmsRuleAllowedPhone(str, Enum):
    ALL = 'all'
    GROUP = 'group'
    SINGLE = 'single'


class DeviceParamType(str, Enum):
    IO_LEGACY = 'IO = "io"'
    EVENT = 'event'
    DEVICE = 'device'
    NETWORK = 'network'
    MOBILE = 'mobile'
    IO = 'io'
    OTHER = 'other'
