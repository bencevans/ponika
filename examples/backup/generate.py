from examples.config import connection
from ponika.endpoints.backup import BackupEncryptInfoPayload

response = connection.backup.generate(BackupEncryptInfoPayload(encrypt=False))

print(type(response))
print(response)
