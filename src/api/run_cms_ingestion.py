from __future__ import annotations

from src.core.logging_config import get_logger
from pathlib import Path

from src.api.cms_client import CMSClient
from src.core.logging_config import configure_logging


OUTPUT_DIRECTORY = Path("data/external/cms")
OUTPUT_FILE = OUTPUT_DIRECTORY / "hospitals.csv"

logger = get_logger("pipeline")


def main() -> None:
    configure_logging()

    logger.info("Starting CMS hospital-data ingestion")

    with CMSClient() as client:
        response = client.fetch_hospitals(
            limit=100,
            offset=0,
        )

        hospitals = client.response_to_dataframe(
            response
        )

    OUTPUT_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    hospitals.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print("=" * 60)
    print("CMS HOSPITAL DATA INGESTION")
    print("=" * 60)
    print(f"HTTP status: {response.status_code}")
    print(f"Rows received: {len(hospitals):,}")
    print(f"Columns received: {len(hospitals.columns):,}")
    print(f"Output file: {OUTPUT_FILE}")
    print("=" * 60)

    logger.info(
        "CMS ingestion completed rows=%s output=%s",
        len(hospitals),
        OUTPUT_FILE,
    )


if __name__ == "__main__":
    main()