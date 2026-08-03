from unittest.mock import Mock

import pytest
import requests

from src.api.base_client import BaseAPIClient
from src.api.exceptions import (
    APIConnectionError,
    APIRateLimitError,
    APIResponseError,
    APITimeoutError,
)


def create_client() -> BaseAPIClient:
    return BaseAPIClient(
        source_name="Test API",
        base_url="https://example.com/api",
        timeout=10,
    )


def test_build_url_combines_base_and_endpoint():
    client = create_client()

    url = client.build_url("/patients")

    assert url == "https://example.com/api/patients"


def test_get_returns_normalized_api_response(monkeypatch):
    client = create_client()

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "results": [
            {"id": 1},
            {"id": 2},
        ]
    }
    mock_response.raise_for_status.return_value = None

    monkeypatch.setattr(
        client.session,
        "get",
        Mock(return_value=mock_response),
    )

    result = client.get("/patients")

    assert result.success is True
    assert result.status_code == 200
    assert result.row_count == 2
    assert result.source == "Test API"


def test_timeout_is_converted_to_healthflow_error(
    monkeypatch,
):
    client = create_client()

    monkeypatch.setattr(
        client.session,
        "get",
        Mock(side_effect=requests.Timeout()),
    )

    with pytest.raises(APITimeoutError):
        client.get("/patients")


def test_connection_error_is_converted(
    monkeypatch,
):
    client = create_client()

    monkeypatch.setattr(
        client.session,
        "get",
        Mock(side_effect=requests.ConnectionError()),
    )

    with pytest.raises(APIConnectionError):
        client.get("/patients")


def test_rate_limit_is_detected(monkeypatch):
    client = create_client()

    mock_response = Mock()
    mock_response.status_code = 429

    monkeypatch.setattr(
        client.session,
        "get",
        Mock(return_value=mock_response),
    )

    with pytest.raises(APIRateLimitError):
        client.get("/patients")


def test_unsuccessful_status_is_detected(
    monkeypatch,
):
    client = create_client()

    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.raise_for_status.side_effect = (
        requests.HTTPError()
    )

    monkeypatch.setattr(
        client.session,
        "get",
        Mock(return_value=mock_response),
    )

    with pytest.raises(APIResponseError):
        client.get("/patients")