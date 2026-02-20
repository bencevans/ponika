# Getting Started

In this guide, you'll learn how to install Ponika and make your first API call to a Teltonika device.

## Install

Ponika is available on PyPI. You can install it using pip, uv, or poetry:

/// tab | pip

    :::bash
    pip install ponika
///

/// tab | uv

    :::bash
    uv add ponika
///

/// tab | poetry

    :::bash
    poetry add ponika
///


## Create a Client

To interact with your Teltonika device, create a `PonikaClient` instance with the appropriate connection parameters.

```python
from ponika import PonikaClient

client = PonikaClient(
    host="192.168.1.1",
    username="admin",
    password="password",
    tls=True,
    verify_tls=False,
)
```

## Make a Request

You can now call methods on the client to interact with the device's API. For example, to get the internet connection status:

```python
response = client.internet_connection.get_status()

if response.success and response.data:
    print(response.data.ipv4_status)
else:
    print(response.errors)
```

## Authentication Behavior

- Ponika logs in lazily when an authenticated endpoint is first called.
- The token is cached in memory and reused until expiry.
- You can call `client.logout()` to end the session.
