"""Reusable mock response templates and helpers."""

import json
import responses
from typing import Any, Dict, Callable

# Base URL for mocked API
BASE_URL = 'https://test-device:443/api'

# Standard responses
# fmt: off
LOGIN_RESPONSE = {
    "success": True,
    "data": {
        "username": "admin",
        "token": "test-token-123",
        "expires": 3600
    }
}

# fmt: off
LOGOUT_RESPONSE = {
    "success": True,
    "data": {
        "response": "Logged out successfully"
    }
}

# Error responses
# fmt: off
ERROR_NOT_FOUND = {
    "success": False,
    "errors": [{
        "code": 122,
        "error": "Not found",
        "source": "endpoint",
        "section": None
    }]
}

# fmt: off
ERROR_UNAUTHORIZED = {
    "success": False,
    "errors": [{
        "code": 401,
        "error": "Unauthorized",
        "source": "auth",
        "section": None
    }]
}


# Session mock responses
# fmt: off
SESSION_STATUS_RESPONSE = {
    "success": True,
    "data": {
        "status": "active",
        "username": "admin",
        "expires_in": 3600
    }
}


# # DHCP Server IPv4 mock responses
# DHCP_IPV4_SERVER_CONFIG_RESPONSE = {
#     "success": True,
#     "data": [{
#         "id": "lan",
#         "interface": "br-lan",
#         "enable_dhcpv4": "1",
#         "mode": "server",
#         "start_ip": "192.168.1.100",
#         "end_ip": "192.168.1.200",
#         "leasetime": "12h",
#         "dynamicdhcp": True,
#         "force": False,
#         "netmask": "255.255.255.0"
#     }]
# }

# DHCP_IPV4_SERVER_STATUS_RESPONSE = {
#     "success": True,
#     "data": [{
#         "id": "lan",
#         "running": True,
#         "interface": ["br-lan"]
#     }]
# }

# DHCP_IPV4_DYNAMIC_LEASES_RESPONSE = {
#     "success": True,
#     "data": [
#         {
#             "expires": 43200,
#             "macaddr": "00:11:22:33:44:55",
#             "ipaddr": "192.168.1.100",
#             "hostname": "test-device",
#             "interface": "br-lan"
#         }
#     ]
# }

# # Users mock responses
# USER_CONFIG_RESPONSE = {
#     "success": True,
#     "data": [{
#         "id": "user1",
#         "username": "testuser",
#         "group": "admin",
#         "ssh_enable": False
#     }]
# }

# USER_CREATE_RESPONSE = {
#     "success": True,
#     "data": {
#         "id": "user1",
#         "username": "testuser",
#         "group": "admin",
#         "ssh_enable": False
#     }
# }

# USER_DELETE_RESPONSE = {
#     "success": True,
#     "data": {
#         "id": "user1"
#     }
# }

# # IP Routes IPv4 mock responses
# IP_ROUTES_IPV4_CONFIG_RESPONSE = {
#     "success": True,
#     "data": [{
#         "id": "route1",
#         "interface": "wan",
#         "target": "10.0.0.0",
#         "netmask": "255.255.255.0",
#         "gateway": "192.168.1.1",
#         "metric": "0"
#     }]
# }

# IP_ROUTES_IPV4_STATUS_RESPONSE = {
#     "success": True,
#     "data": [{
#         "interface": "wan",
#         "target": "10.0.0.0/24",
#         "gateway": "192.168.1.1",
#         "metric": 0
#     }]
# }

# # Wireless mock responses
# WIRELESS_DEVICES_CONFIG_RESPONSE = {
#     "success": True,
#     "data": [{
#         "id": "radio0",
#         "type": "mac80211",
#         "channel": "auto",
#         "hwmode": "11g",
#         "disabled": False
#     }]
# }

# WIRELESS_INTERFACES_CONFIG_RESPONSE = {
#     "success": True,
#     "data": [{
#         "id": "wlan0",
#         "device": "radio0",
#         "mode": "ap",
#         "ssid": "TestNetwork",
#         "encryption": "psk2",
#         "key": "testpassword",
#         "disabled": False
#     }]
# }

# WIRELESS_INTERFACES_STATUS_RESPONSE = {
#     "success": True,
#     "data": [{
#         "interface": "wlan0",
#         "ssid": "TestNetwork",
#         "mode": "Master",
#         "channel": 6,
#         "signal": -45,
#         "noise": -95,
#         "bitrate": 144.4
#     }]
# }

# # Firmware mock responses
# FIRMWARE_STATUS_RESPONSE = {
#     "success": True,
#     "data": {
#         "current_version": "7.19.2",
#         "available_version": "7.20.0",
#         "update_available": True
#     }
# }

# FIRMWARE_UPLOAD_RESPONSE = {
#     "success": True,
#     "data": {
#         "uploaded": True,
#         "filename": "firmware.bin"
#     }
# }


def login_callback(request):
    """Callback for login endpoint that validates credentials.

    Returns success if credentials are correct, error otherwise.
    """

    try:
        body = json.loads(request.body)
        username = body.get("username")
        password = body.get("password")

        # Validate credentials
        if username == "admin" and password == "admin":
            return (200, {}, json.dumps(LOGIN_RESPONSE))
        else:
            # Invalid credentials
            error_response = {
                "success": False,
                "errors": [
                    {
                        "code": 401,
                        "error": "Invalid credentials",
                        "source": "auth",
                        "section": None,
                    }
                ],
            }
            return (200, {}, json.dumps(error_response))
    except Exception:
        # Malformed request
        # fmt: off
        error_response = {
            "success": False,
            "errors": [{
                "code": 400,
                "error": "Bad request",
                "source": "auth",
                "section": None
            }]
        }
        return (200, {}, json.dumps(error_response))


def mock_login_with_validation():
    """Register login mock with credential validation.

    Must be called within a @responses.activate context.
    """
    responses.add_callback(
        responses.POST,
        f"{BASE_URL}/login",
        callback=login_callback,
        content_type="application/json",
    )


def mock_endpoint(
    method: str,
    path: str,
    response_data: Dict[str, Any],
    status: int = 200,
    include_login: bool = True,
    validate_login: bool = False,
) -> None:
    """Register a mocked endpoint response.

    Args:
        method: HTTP method (get, post, put, delete)
        path: API path (e.g., '/tailscale/config')
        response_data: Response JSON data
        status: HTTP status code
        include_login: Whether to also mock the login endpoint
        validate_login: Whether to validate login credentials (requires correct username/password)

    Must be called within a @responses.activate context.
    """
    if include_login:
        if validate_login:
            mock_login_with_validation()
        else:
            responses.post(
                f"{BASE_URL}/login",
                json=LOGIN_RESPONSE,
                status=200,
            )

    getattr(responses, method.lower())(
        f"{BASE_URL}{path}",
        json=response_data,
        status=status,
    )


def mock_endpoint_with_callback(
    method: str,
    path: str,
    callback: Callable,
    include_login: bool = True,
    validate_login: bool = False,
) -> None:
    """Register a mocked endpoint with a callback function for validation.

    Args:
        method: HTTP method (get, post, put, delete)
        path: API path (e.g., '/tailscale/config')
        callback: Callback function that receives request and returns (status, headers, body)
        include_login: Whether to also mock the login endpoint
        validate_login: Whether to validate login credentials

    Must be called within a @responses.activate context.

    Example callback:
        def my_callback(request):
            body = json.loads(request.body)
            if body.get('param') == 'expected':
                return (200, {}, json.dumps({'success': True, 'data': {}}))
            else:
                return (200, {}, json.dumps({'success': False, 'errors': [...]}))
    """
    if include_login:
        if validate_login:
            mock_login_with_validation()
        else:
            responses.post(
                f"{BASE_URL}/login",
                json=LOGIN_RESPONSE,
                status=200,
            )

    responses.add_callback(
        getattr(responses, method.upper()),
        f"{BASE_URL}{path}",
        callback=callback,
        content_type="application/json",
    )


def mock_error_response(
    method: str,
    path: str,
    error_code: int = 122,
    error_message: str = "Not found",
    error_source: str = "endpoint",
    status: int = 200,
    include_login: bool = True,
) -> None:
    """Register a mocked error response.

    Args:
        method: HTTP method (get, post, put, delete)
        path: API path (e.g., '/tailscale/config')
        error_code: Error code
        error_message: Error message
        error_source: Error source
        status: HTTP status code
        include_login: Whether to also mock the login endpoint

    Must be called within a @responses.activate context.
    """
    error_response = {
        "success": False,
        "errors": [
            {
                "code": error_code,
                "error": error_message,
                "source": error_source,
                "section": None,
            }
        ],
    }

    mock_endpoint(
        method=method,
        path=path,
        response_data=error_response,
        status=status,
        include_login=include_login,
    )
