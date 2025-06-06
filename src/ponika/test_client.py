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
    return PonikaClient(TELTONIKA_HOST, TELTONIKA_USERNAME, TELTONIKA_PASSWORD)


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
