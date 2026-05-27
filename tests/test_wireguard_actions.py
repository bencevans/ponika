"""Unit tests for wireguard actions endpoints."""

import pytest
import responses

from ponika.exceptions import TeltonikaApiException
from tests.mocks import mock_endpoint, mock_error_response


WIREGUARD_GENERATE_KEYS_RESPONSE = {
    'success': True,
    'data': {
        'private': 'a' * 44,
        'public': 'b' * 44,
    },
}


@pytest.mark.unit
@responses.activate
def test_wireguard_actions_generate_keys(mock_client):
    mock_endpoint(
        'post',
        '/wireguard/actions/generate_keys',
        WIREGUARD_GENERATE_KEYS_RESPONSE,
    )

    result = mock_client.wireguard.actions.post_generate_keys()

    assert result.private == 'a' * 44
    assert result.public == 'b' * 44


@pytest.mark.unit
@responses.activate
def test_wireguard_actions_generate_keys_error_raises(mock_client):
    mock_error_response(
        'post',
        '/wireguard/actions/generate_keys',
        error_code=500,
        error_message='Failed to generate keys',
        error_source='wireguard',
    )

    with pytest.raises(TeltonikaApiException):
        mock_client.wireguard.actions.post_generate_keys()
