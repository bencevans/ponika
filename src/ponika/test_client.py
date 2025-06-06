import os
from ponika import PonikaClient
from os import environ
import pytest

TELTONIKA_HOST = environ.get("TELTONIKA_HOST")
TELTONIKA_USERNAME = environ.get("TELTONIKA_USERNAME")
TELTONIKA_PASSWORD = environ.get("TELTONIKA_PASSWORD")


def create_client():
    if not TELTONIKA_HOST or not TELTONIKA_USERNAME or not TELTONIKA_PASSWORD:
        raise ValueError(
            "Environment variables TELTONIKA_HOST, TELTONIKA_USERNAME, and TELTONIKA_PASSWORD must be set."
        )

    """Create a PonikaClient instance for testing."""
    return PonikaClient(
        TELTONIKA_HOST, TELTONIKA_USERNAME, TELTONIKA_PASSWORD, verify_tls=False
    )


def test_client_logout():
    """Test the logout functionality of the PonikaClient."""

    logout_response = create_client().logout()
    assert logout_response.success


def test_client_session_status():
    """Test the session status functionality of the PonikaClient."""

    session_status_response = create_client().session.get_status()
    assert session_status_response.success


def test_client_gps_get_global():
    """Test the GPS global functionality of the PonikaClient."""

    gps_global_response = create_client().gps.get_global()
    assert gps_global_response.success


def test_client_gps_get_status():
    """Test the GPS status functionality of the PonikaClient."""

    gps_status_response = create_client().gps.get_status()
    assert gps_status_response.success


def test_client_gps_position_get_status():
    """Test the GPS status functionality of the PonikaClient."""

    gps_status_response = create_client().gps.position.get_status()
    assert gps_status_response.success


def test_client_messages_get_status():
    """Test the messages status functionality of the PonikaClient."""

    messages_status_response = create_client().messages.get_status()
    assert messages_status_response.success


@pytest.mark.skipif(
    os.getenv("MOBILE_NUMBER") is None,
    reason="Mobile number ($MOBILE_NUMBER) required for this test",
)
def test_client_messages_actions_post_send():
    """Test the messages actions send functionality of the PonikaClient."""

    messages_actions_send_response = create_client().messages.actions.post_send(
        number=str(os.getenv("MOBILE_NUMBER")), message="Hello, World!", modem="2-1"
    )
    assert messages_actions_send_response.success


def test_client_dhcp_leases_ipv4_get_status():
    """Test the leases IPv4 status functionality of the PonikaClient."""

    leases_dhcp_leases_ipv4_sg = create_client().dhcp.leases.ipv4.get_status()
    assert leases_dhcp_leases_ipv4_sg.success


def test_client_tailscale_get_config():
    """Test the Tailscale configuration functionality of the PonikaClient."""

    tailscale_config_response = create_client().tailscale.get_config()
    assert tailscale_config_response.success
    assert tailscale_config_response.data


def test_client_tailscale_get_status():
    """Test the Tailscale status functionality of the PonikaClient."""

    tailscale_status_response = create_client().tailscale.get_status()
    assert tailscale_status_response.success
    assert tailscale_status_response.data


def test_client_wireless_interfaces_get_status():
    """Test the wireless interfaces status functionality of the PonikaClient."""

    wireless_interfaces_response = create_client().wireless.interfaces.get_status()
    assert wireless_interfaces_response.success
    assert wireless_interfaces_response.data


def test_client_internet_connection_get_status():
    """Test the internet connection status functionality of the PonikaClient."""

    internet_status_response = create_client().internet_connection.get_status()
    assert internet_status_response.success
    assert internet_status_response.data
