from enum import Enum


class SchedulerAction(str, Enum):
    DEVICE_REBOOT = '1'
    MODEM_REBOOT = '2'


class SchedulerPeriod(str, Enum):
    WEEK = 'week'
    MONTH = 'month'


class SchedulerWeekDay(str, Enum):
    MONDAY = 'mon'
    TUESDAY = 'tue'
    WEDNESDAY = 'wed'
    THURSDAY = 'thu'
    FRIDAY = 'fri'
    SATURDAY = 'sat'
    SUNDAY = 'sun'


class SchedulerMonthDay(str, Enum):
    DAY_1 = '1'
    DAY_2 = '2'
    DAY_3 = '3'
    DAY_4 = '4'
    DAY_5 = '5'
    DAY_6 = '6'
    DAY_7 = '7'
    DAY_8 = '8'
    DAY_9 = '9'
    DAY_10 = '10'
    DAY_11 = '11'
    DAY_12 = '12'
    DAY_13 = '13'
    DAY_14 = '14'
    DAY_15 = '15'
    DAY_16 = '16'
    DAY_17 = '17'
    DAY_18 = '18'
    DAY_19 = '19'
    DAY_20 = '20'
    DAY_21 = '21'
    DAY_22 = '22'
    DAY_23 = '23'
    DAY_24 = '24'
    DAY_25 = '25'
    DAY_26 = '26'
    DAY_27 = '27'
    DAY_28 = '28'
    DAY_29 = '29'
    DAY_30 = '30'
    DAY_31 = '31'


class SchedulerMonth(str, Enum):
    JANUARY = '1'
    FEBRUARY = '2'
    MARCH = '3'
    APRIL = '4'
    MAY = '5'
    JUNE = '6'
    JULY = '7'
    AUGUST = '8'
    SEPTEMBER = '9'
    OCTOBER = '10'
    NOVEMBER = '11'
    DECEMBER = '12'


class PingWgetType(str, Enum):
    PING = 'ping'
    WGET = 'wget'


class PingWgetAction(str, Enum):
    REBOOT_DEVICE = '1'
    REBOOT_MODEM = '2'
    RESTART_CONNECTION = '3'
    SWITCH_MOBILE_DATA = '4'
    SEND_SMS = '5'
    SEND_MESSAGE = '6'
    RUN_SCRIPT = '7'


class PingWgetInterval(str, Enum):
    MINUTE_1 = '1'
    MINUTE_2 = '2'
    MINUTE_3 = '3'
    MINUTE_4 = '4'
    MINUTE_5 = '5'
    MINUTE_15 = '15'
    MINUTE_30 = '30'
    MINUTE_60 = '60'
    MINUTE_120 = '120'


class PingWgetInterface(str, Enum):
    WAN = '1'
    MODEM = '2'


class PingWgetIpType(str, Enum):
    IPV4 = 'ipv4'
    IPV6 = 'ipv6'


class PingWgetActionWhen(str, Enum):
    ALL = 'all'
    ANY = 'any'
