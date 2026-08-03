from __future__ import annotations

from pathlib import Path

import pandas as pd


DATASET_SCHEMAS = {
    "patients": [
        "patient_id",
        "mrn",
        "first_name",
        "last_name",
        "date_of_birth",
        "gender",
        "phone",
        "postal_code",
    ],
    "appointments": [
        "appointment_id",
        "patient_id",
        "scheduled_at",
        "status",
        "department",
    ],
    "labs": [
        "lab_id",
        "patient_id",
        "test_name",
        "result_value",
        "unit",
        "collected_at",
    ],
    "insurance": [
        "coverage_id",
        "patient_id",
        "payer_name",
        "member_id",
        "active",
    ],
    "claims": [
        "claim_id",
        "patient_id",
        "service_date",
        "diagnosis_code",
        "billed_amount",
        "paid_amount",
        "claim_status",
    ],
}


def validate_required_columns(
    dataframe: pd.DataFrame,
    dataset_name: str,
) -> None:
    """Verify that a dataset contains all required columns."""

    if dataset_name not in DATASET_SCHEMAS:
        raise ValueError(
            f"No schema is configured for dataset '{dataset_name}'."
        )

    required_columns = DATASET_SCHEMAS[dataset_name]

    missing_columns = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Dataset '{dataset_name}' is missing required columns: "
            f"{missing_columns}"
        )


def ingest_csv(
    source_file: Path,
    dataset_name: str,
    destination_directory: Path,
) -> pd.DataFrame:
    """
    Read a CSV file, validate its schema, and save an ingested copy.
    """

    if not source_file.exists():
        raise FileNotFoundError(
            f"Source file was not found: {source_file}"
        )

    dataframe = pd.read_csv(source_file)

    validate_required_columns(
        dataframe=dataframe,
        dataset_name=dataset_name,
    )

    destination_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    destination_file = (
        destination_directory / f"{dataset_name}.csv"
    )

    dataframe.to_csv(
        destination_file,
        index=False,
    )

    print(
        f"Ingested {len(dataframe):,} rows "
        f"from {source_file} "
        f"to {destination_file}"
    )

    return dataframe
