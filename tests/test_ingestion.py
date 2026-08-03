from pathlib import Path

import pandas as pd
import pytest

from src.ingestion.csv_ingestion import (
    ingest_csv,
    validate_required_columns,
)


def test_patient_schema_accepts_required_columns():
    dataframe = pd.DataFrame(
        [
            {
                "patient_id": 1,
                "mrn": "MRN0000001",
                "first_name": "Test",
                "last_name": "Patient",
                "date_of_birth": "1990-01-01",
                "gender": "Female",
                "phone": "555-1234",
                "postal_code": "75001",
            }
        ]
    )

    validate_required_columns(
        dataframe=dataframe,
        dataset_name="patients",
    )


def test_patient_schema_rejects_missing_columns():
    dataframe = pd.DataFrame(
        [
            {
                "patient_id": 1,
                "mrn": "MRN0000001",
            }
        ]
    )

    with pytest.raises(ValueError):
        validate_required_columns(
            dataframe=dataframe,
            dataset_name="patients",
        )


def test_ingest_csv_writes_destination_file(
    tmp_path: Path,
):
    source_file = tmp_path / "patients.csv"
    destination_directory = tmp_path / "ingested"

    dataframe = pd.DataFrame(
        [
            {
                "patient_id": 1,
                "mrn": "MRN0000001",
                "first_name": "Test",
                "last_name": "Patient",
                "date_of_birth": "1990-01-01",
                "gender": "Female",
                "phone": "555-1234",
                "postal_code": "75001",
            }
        ]
    )

    dataframe.to_csv(source_file, index=False)

    result = ingest_csv(
        source_file=source_file,
        dataset_name="patients",
        destination_directory=destination_directory,
    )

    assert len(result) == 1
    assert (destination_directory / "patients.csv").exists()