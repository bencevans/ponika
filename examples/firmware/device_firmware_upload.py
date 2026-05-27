import os

from examples.config import connection

current_dir = os.path.dirname(os.path.abspath(__file__))

update_filepath = current_dir + '/RUT2M_R_00.07.20.3_WEBUI.bin'
response = connection.firmware.device.upload_firmware(update_filepath)

# print(absolute_path)
print(type(response))
print(response)
