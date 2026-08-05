from pathlib import Path

import pandas as pd

from src.frontend.views.data_sources import (
    count_csv_rows,
    format_file_timestamp,
)


def test_count_csv_rows_returns_record_count(
    tmp_path: Path,
):
    file_path = tmp_path / "example.csv"

    pd.DataFrame(
        [
            {"id": 1},
            {"id": 2},
        ]
    ).to_csv(
        file_path,
        index=False,
    )

    assert count_csv_rows(file_path) == 2


def test_missing_csv_returns_zero(
    tmp_path: Path,
):
    missing_file = tmp_path / "missing.csv"

    assert count_csv_rows(missing_file) == 0


def test_missing_file_timestamp_is_unavailable(
    tmp_path: Path,
):
    missing_file = tmp_path / "missing.csv"

    assert (
        format_file_timestamp(missing_file)
        == "Not available"
    )