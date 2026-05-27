from datetime import datetime
from examples.config import connection
from ponika.endpoints.data_usage import UsageInterval

response = connection.data_usage.get_simcard_usage(UsageInterval.DAY)

print(type(response))
print(response)

for row in response:
    dt = datetime.fromtimestamp(row[0])
    print(
        f'{dt.strftime("%Y-%m-%d %H:%M")}: {row[1]} byte received, {row[2]} byte send'
    )

response = connection.data_usage.get_simcard_usage(UsageInterval.TOTAL)

print(type(response))
print(response)

for row in response:
    dt = datetime.fromtimestamp(row[0])
    print(
        f'{dt.strftime("%Y-%m-%d %H:%M")}: {row[1]} byte received, {row[2]} byte send'
    )
