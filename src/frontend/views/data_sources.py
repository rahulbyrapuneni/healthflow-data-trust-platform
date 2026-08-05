from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st


CMS_HOSPITAL_FILE = Path(
    "data/external/cms/hospitals.csv"
)

CLINICAL_TRIALS_FILE = Path(
    "data/source_data/clinical_trials.csv"
)

SYNTHETIC_DATA_DIRECTORY = Path(
    "data/ingested"
)

SYNTHETIC_DATASETS = [
    "patients",
    "appointments",
    "labs",
    "claims",
    "insurance",
]


def format_file_timestamp(
    path: Path,
) -> str:
    """Return a readable file modification timestamp."""

    if not path.exists():
        return "Not available"

    modified_time = datetime.fromtimestamp(
        path.stat().st_mtime
    )

    return modified_time.strftime(
        "%Y-%m-%d %I:%M %p"
    )


def count_csv_rows(
    path: Path,
) -> int:
    """Count records in a CSV file."""

    if not path.exists():
        return 0

    try:
        return len(
            pd.read_csv(path)
        )
    except (
        OSError,
        pd.errors.ParserError,
    ):
        return 0


def build_source_inventory() -> pd.DataFrame:
    """Build the current healthcare-source inventory."""

    synthetic_files = [
        SYNTHETIC_DATA_DIRECTORY / f"{name}.csv"
        for name in SYNTHETIC_DATASETS
    ]

    available_synthetic_files = [
        path
        for path in synthetic_files
        if path.exists()
    ]

    synthetic_rows = sum(
        count_csv_rows(path)
        for path in available_synthetic_files
    )

    synthetic_last_refresh = "Not available"

    if available_synthetic_files:
        newest_file = max(
            available_synthetic_files,
            key=lambda path: path.stat().st_mtime,
        )

        synthetic_last_refresh = (
            format_file_timestamp(newest_file)
        )

    rows = [
        {
            "source": "Synthetic Healthcare Data",
            "source_type": "Local simulator",
            "status": (
                "Connected"
                if available_synthetic_files
                else "Unavailable"
            ),
            "datasets": len(
                available_synthetic_files
            ),
            "records": synthetic_rows,
            "last_refresh": synthetic_last_refresh,
            "description": (
                "Controlled healthcare datasets used "
                "for repeatable validation testing."
            ),
        },
        {
            "source": "CMS Hospital Data",
            "source_type": "Public REST API",
            "status": (
                "Connected"
                if CMS_HOSPITAL_FILE.exists()
                else "Unavailable"
            ),
            "datasets": (
                1
                if CMS_HOSPITAL_FILE.exists()
                else 0
            ),
            "records": count_csv_rows(
                CMS_HOSPITAL_FILE
            ),
            "last_refresh": (
                format_file_timestamp(
                    CMS_HOSPITAL_FILE
                )
            ),
            "description": (
                "Public hospital general-information "
                "records retrieved from CMS."
            ),
        },
        {
            "source": "ClinicalTrials.gov",
            "source_type": "Public REST API",
            "status": (
                "Connected"
                if CLINICAL_TRIALS_FILE.exists()
                else "Unavailable"
            ),
            "datasets": (
                1
                if CLINICAL_TRIALS_FILE.exists()
                else 0
            ),
            "records": count_csv_rows(
                CLINICAL_TRIALS_FILE
            ),
            "last_refresh": (
                format_file_timestamp(
                    CLINICAL_TRIALS_FILE
                )
            ),
            "description": (
                "Public clinical-study and research records "
                "retrieved from ClinicalTrials.gov."
            ),
        },
        {
            "source": "openFDA",
            "source_type": "Public REST API",
            "status": "Planned",
            "datasets": 0,
            "records": 0,
            "last_refresh": "Not connected",
            "description": (
                "Future integration for drug, device, "
                "recall, and adverse-event data."
            ),
        },
    ]

    return pd.DataFrame(rows)


def render_data_sources() -> None:
    """Render the healthcare data-source inventory."""

    st.title("Data Sources")

    st.caption(
        "Connection and refresh status for healthcare "
        "datasets available to HealthFlow."
    )

    inventory = build_source_inventory()

    connected_count = int(
        (
            inventory["status"]
            == "Connected"
        ).sum()
    )

    total_records = int(
        inventory["records"].sum()
    )

    api_count = int(
        (
            inventory["source_type"]
            == "Public REST API"
        ).sum()
    )

    metric_1, metric_2, metric_3 = st.columns(3)

    metric_1.metric(
        "Connected Sources",
        connected_count,
    )

    metric_2.metric(
        "Available Records",
        f"{total_records:,}",
    )

    metric_3.metric(
        "Registered APIs",
        api_count,
    )

    st.divider()

    st.subheader("Source Inventory")

    display_columns = [
        "source",
        "source_type",
        "status",
        "datasets",
        "records",
        "last_refresh",
        "description",
    ]

    st.dataframe(
        inventory[display_columns],
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    st.subheader("CMS Hospital Integration")

    cms_row = inventory[
        inventory["source"]
        == "CMS Hospital Data"
    ].iloc[0]

    cms_1, cms_2, cms_3 = st.columns(3)

    cms_1.metric(
        "Connection Status",
        cms_row["status"],
    )

    cms_2.metric(
        "Hospital Records",
        f"{int(cms_row['records']):,}",
    )

    cms_3.metric(
        "Last Refresh",
        cms_row["last_refresh"],
    )

    if cms_row["status"] == "Connected":
        st.info(
            "CMS hospital data is available for "
            "quality validation and trust scoring."
        )
    else:
        st.info(
            "Run the CMS ingestion pipeline to download "
            "the hospital dataset."
        )

        st.code(
            ".\\.venv\\Scripts\\python.exe "
            "-m src.api.run_cms_ingestion",
            language="powershell",
        )

    st.divider()

    st.subheader(
        "ClinicalTrials.gov Integration"
    )

    clinical_trials_row = inventory[
        inventory["source"]
        == "ClinicalTrials.gov"
    ].iloc[0]

    trial_1, trial_2, trial_3 = st.columns(3)

    trial_1.metric(
        "Connection Status",
        clinical_trials_row["status"],
    )

    trial_2.metric(
        "Clinical Trial Records",
        f"{int(clinical_trials_row['records']):,}",
    )

    trial_3.metric(
        "Last Refresh",
        clinical_trials_row["last_refresh"],
    )

    if clinical_trials_row["status"] == "Connected":
        st.info(
            "ClinicalTrials.gov data is available for "
            "quality validation and trust scoring."
        )
    else:
        st.info(
            "Run the ClinicalTrials.gov ingestion process "
            "to download trial records."
        )

        st.code(
            ".\\.venv\\Scripts\\python.exe "
            "-m src.simulator.generate_clinical_trials",
            language="powershell",
        )