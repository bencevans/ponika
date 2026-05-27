"""Unit tests for Data Usage endpoints."""

import pytest
import responses

from tests.mocks import (
    mock_endpoint,
    mock_error_response,
)

# Data Usage mock responses
# fmt: off
DATA_USAGE_DAY_RESPONSE = {
    "success": True,
    "data": [[1707912000, 1048576, 524288]]
}

    # fmt: off
DATA_USAGE_WEEK_RESPONSE = {
    "success": True,
    "data": [
        [1707912000, 10485760, 5242880],
        [1707998400, 20971520, 10485760]
    ]
}


@pytest.mark.unit
@responses.activate
def test_data_usage_day(mock_client):
    """Test getting daily data usage."""
    from ponika.endpoints.data_usage import UsageInterval

    mock_endpoint("get", "/data_usage/day/status", DATA_USAGE_DAY_RESPONSE)

    result = mock_client.data_usage.get_simcard_usage(UsageInterval.DAY)

    assert len(result) == 1
    assert result[0][0] == 1707912000  # timestamp
    assert result[0][1] == 1048576  # download bytes (1 MB)
    assert result[0][2] == 524288  # upload bytes (512 KB)


@pytest.mark.unit
@responses.activate
def test_data_usage_week(mock_client):
    """Test getting weekly data usage."""
    from ponika.endpoints.data_usage import UsageInterval

    mock_endpoint("get", "/data_usage/week/status", DATA_USAGE_WEEK_RESPONSE)

    result = mock_client.data_usage.get_simcard_usage(UsageInterval.WEEK)

    assert len(result) == 2
    assert result[0][0] == 1707912000
    assert result[1][0] == 1707998400


@pytest.mark.unit
@responses.activate
def test_data_usage_month(mock_client):
    """Test getting monthly data usage."""
    from ponika.endpoints.data_usage import UsageInterval

    # fmt: off
    month_response = {
        "success": True,
        "data": [
            [1707912000, 104857600, 52428800],
            [1708516800, 209715200, 104857600]
        ]
    }

    mock_endpoint("get", "/data_usage/month/status", month_response)

    result = mock_client.data_usage.get_simcard_usage(UsageInterval.MONTH)

    assert len(result) == 2
    assert result[0][1] == 104857600  # 100 MB download
    assert result[1][1] == 209715200  # 200 MB download


@pytest.mark.unit
@responses.activate
def test_data_usage_total(mock_client):
    """Test getting total data usage."""
    from ponika.endpoints.data_usage import UsageInterval

    total_response = {
        "success": True,
        "data": [[0, 1073741824, 536870912]],  # 1 GB / 512 MB
    }

    mock_endpoint("get", "/data_usage/total/status", total_response)

    result = mock_client.data_usage.get_simcard_usage(UsageInterval.TOTAL)

    assert len(result) == 1
    assert result[0][1] == 1073741824  # 1 GB
    assert result[0][2] == 536870912  # 512 MB


@pytest.mark.unit
@responses.activate
def test_data_usage_empty(mock_client):
    """Test data usage with no data."""
    from ponika.endpoints.data_usage import UsageInterval

    empty_response = {"success": True, "data": []}

    mock_endpoint("get", "/data_usage/day/status", empty_response)

    result = mock_client.data_usage.get_simcard_usage(UsageInterval.DAY)

    assert len(result) == 0


@pytest.mark.unit
@responses.activate
def test_data_usage_not_supported(mock_client):
    """Test data usage when feature is not supported."""
    from ponika.endpoints.data_usage import UsageInterval
    from ponika.exceptions import TeltonikaApiException

    mock_error_response(
        "get",
        "/data_usage/day/status",
        error_code=122,
        error_message="Not found",
        error_source="data_usage",
    )

    with pytest.raises(TeltonikaApiException):
        mock_client.data_usage.get_simcard_usage(UsageInterval.DAY)
