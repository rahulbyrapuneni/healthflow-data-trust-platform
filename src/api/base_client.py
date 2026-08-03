from __future__ import annotations
from src.core.logging_config import get_logger
from typing import Any
from urllib.parse import urljoin

import requests

from src.api.exceptions import (
    APIClientError,
    APIConnectionError,
    APIDataFormatError,
    APIRateLimitError,
    APIResponseError,
    APITimeoutError,
)
from src.api.models import APIResponse


logger = get_logger("api")


class BaseAPIClient:
    """Reusable base client for external REST APIs."""

    def __init__(
        self,
        source_name: str,
        base_url: str,
        timeout: float = 30.0,
    ) -> None:
        if not source_name.strip():
            raise ValueError("source_name cannot be empty.")

        if not base_url.strip():
            raise ValueError("base_url cannot be empty.")

        self.source_name = source_name
        self.base_url = base_url.rstrip("/") + "/"
        self.timeout = timeout

        self.session = requests.Session()

        self.session.headers.update(
            {
                "Accept": "application/json",
                "User-Agent": (
                    "HealthFlow-Data-Trust-Platform/0.2"
                ),
            }
        )

    def build_url(self, endpoint: str) -> str:
        """Create a complete URL from the base URL and endpoint."""

        return urljoin(
            self.base_url,
            endpoint.lstrip("/"),
        )

    def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> APIResponse:
        """Send a GET request and return a normalized response."""

        url = self.build_url(endpoint)

        logger.info(
            "Sending GET request source=%s endpoint=%s",
            self.source_name,
            url,
        )

        try:
            response = self.session.get(
                url=url,
                params=params,
                timeout=self.timeout,
            )

        except requests.Timeout as error:
            logger.exception(
                "API request timed out source=%s endpoint=%s",
                self.source_name,
                url,
            )

            raise APITimeoutError(
                f"{self.source_name} request timed out "
                f"after {self.timeout} seconds."
            ) from error

        except requests.ConnectionError as error:
            logger.exception(
                "API connection failed source=%s endpoint=%s",
                self.source_name,
                url,
            )

            raise APIConnectionError(
                f"Unable to connect to {self.source_name}."
            ) from error

        except requests.RequestException as error:
            logger.exception(
                "Unexpected request failure source=%s endpoint=%s",
                self.source_name,
                url,
            )

            raise APIClientError(
                f"Unexpected error while calling "
                f"{self.source_name}: {error}"
            ) from error

        if response.status_code == 429:
            logger.warning(
                "API rate limit reached source=%s endpoint=%s",
                self.source_name,
                url,
            )

            raise APIRateLimitError(
                f"{self.source_name} rate limit was reached."
            )

        try:
            response.raise_for_status()

        except requests.HTTPError as error:
            logger.exception(
                (
                    "API returned unsuccessful response "
                    "source=%s endpoint=%s status=%s"
                ),
                self.source_name,
                url,
                response.status_code,
            )

            raise APIResponseError(
                f"{self.source_name} returned HTTP "
                f"{response.status_code}."
            ) from error

        try:
            payload = response.json()

        except requests.JSONDecodeError as error:
            logger.exception(
                (
                    "API returned invalid JSON "
                    "source=%s endpoint=%s"
                ),
                self.source_name,
                url,
            )

            raise APIDataFormatError(
                f"{self.source_name} returned invalid JSON."
            ) from error

        row_count = self._calculate_row_count(payload)

        logger.info(
            (
                "API request completed source=%s "
                "status=%s rows=%s"
            ),
            self.source_name,
            response.status_code,
            row_count,
        )

        return APIResponse(
            source=self.source_name,
            endpoint=url,
            success=True,
            status_code=response.status_code,
            row_count=row_count,
            message="Request completed successfully.",
            data=payload,
        )

    @staticmethod
    def _calculate_row_count(payload: Any) -> int:
        """Estimate the number of records in a JSON response."""

        if isinstance(payload, list):
            return len(payload)

        if isinstance(payload, dict):
            for key in (
                "data",
                "results",
                "items",
                "records",
            ):
                value = payload.get(key)

                if isinstance(value, list):
                    return len(value)

            return 1

        return 0

    def close(self) -> None:
        """Close the HTTP session."""

        self.session.close()

    def __enter__(self) -> BaseAPIClient:
        return self

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception_value: BaseException | None,
        traceback: object | None,
    ) -> None:
        self.close()