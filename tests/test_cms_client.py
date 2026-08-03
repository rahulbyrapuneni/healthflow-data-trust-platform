from src.api.cms_client import (
    CMSClient,
    HOSPITAL_GENERAL_INFORMATION_DATASET_ID,
)
from src.api.models import APIResponse


def test_cms_client_uses_correct_base_url():
    client = CMSClient()

    assert client.base_url == (
        "https://data.cms.gov/provider-data/api/1/"
    )


def test_fetch_hospitals_uses_expected_dataset(
    monkeypatch,
):
    client = CMSClient()

    captured: dict = {}

    def fake_fetch_dataset_page(
        dataset_id: str,
        limit: int,
        offset: int,
    ) -> APIResponse:
        captured["dataset_id"] = dataset_id
        captured["limit"] = limit
        captured["offset"] = offset

        return APIResponse(
            source="CMS Provider Data Catalog",
            endpoint="test",
            success=True,
            status_code=200,
            row_count=0,
            message="Success",
            data={"results": []},
        )

    monkeypatch.setattr(
        client,
        "fetch_dataset_page",
        fake_fetch_dataset_page,
    )

    client.fetch_hospitals(
        limit=25,
        offset=50,
    )

    assert captured["dataset_id"] == (
        HOSPITAL_GENERAL_INFORMATION_DATASET_ID
    )
    assert captured["limit"] == 25
    assert captured["offset"] == 50


def test_cms_response_converts_to_dataframe():
    response = APIResponse(
        source="CMS Provider Data Catalog",
        endpoint="test",
        success=True,
        status_code=200,
        row_count=2,
        message="Success",
        data={
            "results": [
                {
                    "facility_id": "100001",
                    "facility_name": "Test Hospital One",
                },
                {
                    "facility_id": "100002",
                    "facility_name": "Test Hospital Two",
                },
            ]
        },
    )

    dataframe = CMSClient.response_to_dataframe(
        response
    )

    assert len(dataframe) == 2
    assert "facility_id" in dataframe.columns
    assert "facility_name" in dataframe.columns


def test_fetch_dataset_page_rejects_invalid_limit():
    client = CMSClient()

    try:
        client.fetch_dataset_page(
            dataset_id="test",
            limit=0,
        )
    except ValueError as error:
        assert "limit" in str(error)
    else:
        raise AssertionError(
            "Expected ValueError for invalid limit."
        )