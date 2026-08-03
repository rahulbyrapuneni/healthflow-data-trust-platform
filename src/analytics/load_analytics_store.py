from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.analytics.duckdb_store import replace_table
from src.core.logging_config import get_logger


logger = get_logger("pipeline")


QUALITY_RESULTS_PATH = Path("data/quality_results")
CMS_PATH = Path("data/external/cms/hospitals.csv")

TABLE_FILES = {
    "quality_issues": (
        QUALITY_RESULTS_PATH / "all_quality_issues.csv"
    ),
    "dataset_trust_summary": (
        QUALITY_RESULTS_PATH / "dataset_trust_summary.csv"
    ),
    "cms_hospitals": CMS_PATH,
}


def load_csv_table(
    table_name: str,
    file_path: Path,
) -> None:
    """Load one CSV file into DuckDB."""

    if not file_path.exists():
        logger.warning(
            "Skipping missing analytics source table=%s file=%s",
            table_name,
            file_path,
        )
        return

    dataframe = pd.read_csv(file_path)

    replace_table(
        table_name=table_name,
        dataframe=dataframe,
    )

    logger.info(
        "Loaded DuckDB table=%s rows=%s",
        table_name,
        len(dataframe),
    )


def load_summary_history() -> None:
    """Load all dataset-summary history files into DuckDB."""

    history_path = QUALITY_RESULTS_PATH / "history"
    history_files = sorted(
        history_path.glob("summary_*.csv")
    )

    if not history_files:
        logger.warning(
            "No summary history files were found."
        )
        return

    history = pd.concat(
        [
            pd.read_csv(file_path)
            for file_path in history_files
        ],
        ignore_index=True,
    )

    replace_table(
        table_name="dataset_trust_history",
        dataframe=history,
    )

    logger.info(
        "Loaded DuckDB table=dataset_trust_history rows=%s",
        len(history),
    )


def main() -> None:
    logger.info("Starting DuckDB analytics load")

    for table_name, file_path in TABLE_FILES.items():
        load_csv_table(
            table_name=table_name,
            file_path=file_path,
        )

    load_summary_history()

    logger.info("DuckDB analytics load completed")

    print("=" * 60)
    print("HEALTHFLOW DUCKDB ANALYTICS LOAD")
    print("=" * 60)
    print("Database: data\\healthflow.duckdb")
    print("Analytics load completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()