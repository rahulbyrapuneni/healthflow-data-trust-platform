from __future__ import annotations

from pathlib import Path

import pandas as pd


CMS_FILE = Path("data/external/cms/hospitals.csv")


def main() -> None:
    if not CMS_FILE.exists():
        raise FileNotFoundError(
            "CMS hospital file was not found. "
            "Run the CMS ingestion process first."
        )

    hospitals = pd.read_csv(
        CMS_FILE,
        dtype=str,
    )

    print("=" * 80)
    print("CMS HOSPITAL DATA SCHEMA")
    print("=" * 80)

    print(f"Rows: {len(hospitals):,}")
    print(f"Columns: {len(hospitals.columns):,}")
    print()

    print("COLUMN NAMES")
    print("-" * 80)

    for position, column in enumerate(
        hospitals.columns,
        start=1,
    ):
        non_null_count = hospitals[column].notna().sum()
        missing_count = hospitals[column].isna().sum()
        unique_count = hospitals[column].nunique(
            dropna=True
        )

        print(
            f"{position:02d}. {column}"
            f" | non-null={non_null_count}"
            f" | missing={missing_count}"
            f" | unique={unique_count}"
        )

    print()
    print("FIRST THREE RECORDS")
    print("-" * 80)

    print(
        hospitals.head(3).to_string(
            index=False,
        )
    )


if __name__ == "__main__":
    main()