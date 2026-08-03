from pathlib import Path

from csv_ingestion import ingest_csv


SOURCE_DIRECTORY = Path("data/raw")
INGESTED_DIRECTORY = Path("data/ingested")


DATASETS = [
    "patients",
    "appointments",
    "labs",
    "insurance",
    "claims",
]


def main() -> None:
    print("=" * 60)
    print("HEALTHFLOW DATA INGESTION")
    print("=" * 60)

    for dataset_name in DATASETS:
        source_file = (
            SOURCE_DIRECTORY / f"{dataset_name}.csv"
        )

        ingest_csv(
            source_file=source_file,
            dataset_name=dataset_name,
            destination_directory=INGESTED_DIRECTORY,
        )

    print("=" * 60)
    print("Ingestion completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()