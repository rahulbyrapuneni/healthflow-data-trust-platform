from __future__ import annotations

from typing import Any

import pandas as pd

from src.api.base_client import BaseAPIClient
from src.api.exceptions import APIDataFormatError
from src.api.models import APIResponse


CMS_BASE_URL = "https://data.cms.gov/provider-data/api/1/"
HOSPITAL_GENERAL_INFORMATION_DATASET_ID = "xubh-q36u"


class CMSClient(BaseAPIClient):
    """Client for the CMS Provider Data Catalog API."""

    def __init__(
        self,
        timeout: float = 30.0,
    ) -> None:
        super().__init__(
            source_name="CMS Provider Data Catalog",
            base_url=CMS_BASE_URL,
            timeout=timeout,
        )

    def fetch_dataset_page(
        self,
        dataset_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> APIResponse:
        """Retrieve one page from a CMS dataset."""

        if not dataset_id.strip():
            raise ValueError("dataset_id cannot be empty.")

        if limit <= 0:
            raise ValueError("limit must be greater than zero.")

        if offset < 0:
            raise ValueError("offset cannot be negative.")

        endpoint = (
            f"datastore/query/{dataset_id}/0"
        )

        return self.get(
            endpoint=endpoint,
            params={
                "limit": limit,
                "offset": offset,
            },
        )

    def fetch_hospitals(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> APIResponse:
        """Retrieve CMS hospital general-information records."""

        return self.fetch_dataset_page(
            dataset_id=(
                HOSPITAL_GENERAL_INFORMATION_DATASET_ID
            ),
            limit=limit,
            offset=offset,
        )

    @staticmethod
    def response_to_dataframe(
        response: APIResponse,
    ) -> pd.DataFrame:
        """Convert a CMS API response into a DataFrame."""

        payload: Any = response.data

        if not isinstance(payload, dict):
            raise APIDataFormatError(
                "CMS response must be a JSON object."
            )

        records = payload.get("results")

        if not isinstance(records, list):
            raise APIDataFormatError(
                "CMS response does not contain a "
                "valid results list."
            )

        return pd.DataFrame(records)