import os

from examples.config import connection

current_dir = os.path.dirname(os.path.abspath(__file__))

response = connection.firmware.device.verify_uploaded_firmware()

# print(absolute_path)
print(type(response))
print(response)
