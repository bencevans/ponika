# Ponika

Ponika is a Python library for interacting with Teltonika devices.  
The compatibility is tested with RUT devices.

## supported Endpoints

| Modul | Endpoint | Status |
| ----- | -------- | ------ |
| Auto Reboot | Scheduler | ✅ |
| Auto Reboot | Ping/Wget | ✅ |
| Backup |  | ✅ |
| Call | Util Setup | ⭕ |
| Data Usages  | SIM Card | ✅ |
| Data Usages  | Modem | ⭕ |
| Data Usages  | eSIM | ❌ |
| DHCP  | DHCP Server IPv4 | ✅ |
| DHCP  | Static Leases IPv4 | ✅ |
| DHCP  | DHCP Server IPv6 | ✅ |
| DHCP  | Static Leases IPv6 | ✅ |
| Firmware  | Upgrade | ✅ |
| GPS |  | ✅ |
| Internet Connection |  | ✅ |
| IP Neightbors | IPv4 | ✅ |
| IP Neightbors | IPv6 | ✅ |
| IP Routes  | IPv4 Routes | ✅ |
| IP Routes  | IPv6 Routes | ✅ |
| Modem |  | 🟡 |
| MQTT | Broker  | ❌ |
| MQTT | Publisher  | ❌ |
| OpenVPN |  | ⭕ |
| Recipient Groups |  | ✅ |
| SMS | Send | ✅ |
| SMS | Read/Delete | ✅ |
| SMS | Command Setup | ✅ |
| Tailscale |  | ⚠️ |
| Usermanagement  | - | ✅ |
| Wireguard |  | ✅ |
| Wireless  | Devices | ✅ |
| Wireless  | Interfaces | ✅ |
| Zerotier |  | ✅ |

✅ - Supported  
⚠️ - Supported, but lack of practical use case, not real tested  
🟡 - Partially implemented  
⭕ - Will be implemented   
❌ - Will not implemented at the moment (missing hardware or test case)
## Installation

You can install Ponika using pip:

```bash
pip install ponika
```

## Usage

To use Ponika, you need to create an instance of `PonikaClient` with the appropriate parameters. Here's a basic example:

```python
from ponika import PonikaClient

client = PonikaClient(
    host="192.168.1.1",
    username="your_username",
    password="your_password",
    # port=80,       # Optional, default is 443 if tls=True else 80
    # tls=False,     # Optional, default is True
    # verify_tls=False,  # Optional, default is True
)
```

The library follows the structure of the Teltonika API endpoints. For example, to get the internet status from the endpoint `/api/v1/internet_connection/status`, you can do the following:

```python
response = client.internet_connection.get_status()

if response.success and response.data:
    print("Internet Status:")
    print("IPv4:", response.data.ipv4_status)
    print("IPv6:", response.data.ipv6_status)
    print("DNS: ", response.data.dns_status)
else:
    print("Error:", response.errors)
```

> [!NOTE]
> Not all endpoints are implemented. If you need a specific endpoint that's missing, the existing endpoints should be a good reference for how to implement new ones.

## Examples

#### Get Internet Status

```python
response = client.internet_connection.get_status()

if response.success and response.data:
    print("Internet Status:")
    print("IPv4:", response.data.ipv4_status)
    print("IPv6:", response.data.ipv6_status)
    print("DNS: ", response.data.dns_status)
else:
    print("Error:", response.errors)
```

#### Get GPS Position

```python
response = client.gps.position.get_status()

if response.success and response.data:
    print("GPS Position:")
    print("Latitude:", response.data.latitude)
    print("Longitude:", response.data.longitude)
    print("Altitude:", response.data.altitude)
else:
    print("Error:", response.errors)
```

## Contributing

If you want to contribute to Ponika, feel free to open a pull request on the GitHub repository. Contributions are welcome!

The project is setup to use [`uv`](https://docs.astral.sh/uv/) for development and requires prior installation. Once you've cloned the repository, you can set up the development environment by running:

```bash
uv sync
```

### Testing

Ponika includes both unit tests (with mocked responses) and integration tests (requiring real hardware).

**Run unit tests only (no hardware required):**
```bash
uv run pytest -m unit
```

**Run integration tests (requires real hardware):**
```bash
# Required variables
export TELTONIKA_HOST=192.168.1.1
export TELTONIKA_USERNAME=admin
export TELTONIKA_PASSWORD=password

# Optional variables
export MOBILE_NUMBER=441234567890  # Enables SMS sending tests

# Run integration tests
uv run pytest -m integration
```

**Run all tests:**
```bash
uv run pytest
```

For detailed information about writing and running tests, see [docs/TESTING.md](docs/TESTING.md).
