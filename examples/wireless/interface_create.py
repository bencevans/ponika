import pprint
from examples.config import connection

from ponika.endpoints.wireless.interfaces import WirelessInterfaceCreatePayload

newInterface = WirelessInterfaceCreatePayload()
newInterface.ssid = 'Example-SSID'
newInterface.key = 'Wifi-Key'

response = connection.wireless.interfaces.create(newInterface)

print(type(response))
pprint.pprint(response)
