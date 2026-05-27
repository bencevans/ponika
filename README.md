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

## Config State as Code

Ponika can reconcile selected configuration sections declaratively with
`client.config.apply(...)`. Only the sections included in the configuration are
managed. For each included section Ponika will:

- create missing entries,
- update existing entries when one of the defined fields differs,
- delete existing entries that are not present in the desired configuration.

Only fields defined in the desired configuration are compared. This allows you
to omit read-only fields or fields that differ between read and write models.
CRUD endpoints use `id` as the default identifier field and match existing
entries by `id` or `name` by default.

```python
from ponika import PonikaClient
from ponika.config import PonikaConfig, RecipientsConfig
from ponika.endpoints.recipients.phone_groups import PhoneGroupCreatePayload


client = PonikaClient(
    host="192.168.1.1",
    username="your_username",
    password="your_password",
    verify_tls=False,
)

result = client.config.apply(
    PonikaConfig(
        recipients=RecipientsConfig(
            phone_groups=[
                PhoneGroupCreatePayload(
                    name="Admins",
                    tel=["+49170123456"],
                ),
            ],
        )
    )
)

print("Created:", len(result.created))
print("Updated:", len(result.updated))
print("Deleted:", len(result.deleted))
print("Unchanged:", len(result.unchanged))
```

To preview the planned changes without writing them to the device, use
`dry_run=True`. Dry-run mode still reads the current configuration but skips
create, update and delete requests. The returned `ConfigApplyResult` contains
the same change summary plus `existing` and `desired` data on each change where
available.

```python
preview = client.config.apply(
    PonikaConfig(
        recipients=RecipientsConfig(
            phone_groups=[
                PhoneGroupCreatePayload(
                    name="Admins",
                    tel=["+49170123456"],
                ),
            ],
        )
    ),
    dry_run=True,
)

for change in preview.changes:
    print(change.action, change.section, change.match_field, change.match_value)
    print("Existing:", change.existing)
    print("Desired:", change.desired)
```

By default, Config as Code deletes existing entries in managed sections when
they are not present in the desired configuration. If you only want to create
and update entries, disable that behavior with `delete_unmanaged=False`:

```python
result = client.config.apply(
    desired_config,
    delete_unmanaged=False,
)
```

> [!WARNING]
> Config as Code is intentionally destructive for managed sections: entries in
> an included section that are not part of the desired state will be deleted.
> Include only sections you want Ponika to fully manage.

For IDE autocompletion and type checking, prefer `PonikaConfig` and the nested
section models such as `RecipientsConfig`. A plain dict is also accepted for
dynamic use cases.

Typed ConfigState-as-Code models are available for all currently reconcilable
configuration endpoints:

- `AutoRebootConfig`: `scheduler`, `ping_wget`
- `DhcpConfig`: `static_leases_ipv4`, `static_leases_ipv6`
- `IpRoutesConfig`: `routes_ipv4`, `routes_ipv6`
- `RecipientsConfig`: `phone_groups`, `email_users`
- `SmsUtilitiesConfig`: `rules`
- `WireguardConfig`: `config`, `peers`
- `WirelessConfig`: `interfaces`
- `ZerotierConfig`: `config`, `networks`

Dynamic sub-configurations such as WireGuard peers and ZeroTier networks include
their parent identifier (`interface_id` or `config_id`) plus an `items` list.

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
