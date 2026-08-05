from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


CURRENT_FILE = Path(
    "data/source_data/clinical_trials.csv"
)

CHANGE_HISTORY_FILE = Path(
    "data/history/clinical_trials_changes.csv"
)

MONITORED_COLUMNS = [
    "title",
    "condition",
    "phase",
    "sponsor",
    "status",
    "start_date",
    "completion_date",
    "first_posted_date",
    "last_update_posted_date",
]


def normalize_value(value: object) -> str:
    """Normalize a field before comparing snapshots."""

    if pd.isna(value):
        return ""

    return str(value).strip()


def changed_fields(
    previous_row: pd.Series,
    latest_row: pd.Series,
) -> list[str]:
    """Return the fields that changed for one trial."""

    changes: list[str] = []

    for column in MONITORED_COLUMNS:
        previous_value = normalize_value(
            previous_row.get(column)
        )

        latest_value = normalize_value(
            latest_row.get(column)
        )

        if previous_value != latest_value:
            changes.append(column)

    return changes


def detect_clinical_trial_changes(
    previous: pd.DataFrame,
    latest: pd.DataFrame,
) -> tuple[pd.DataFrame, dict[str, int]]:
    """Identify new, updated, and unchanged trials."""

    change_columns = [
        "detected_at",
        "change_type",
        "nct_id",
        "changed_fields",
        "previous_status",
        "current_status",
        "previous_last_update_posted_date",
        "current_last_update_posted_date",
    ]

    if latest.empty:
        return (
            pd.DataFrame(columns=change_columns),
            {
                "new": 0,
                "updated": 0,
                "unchanged": 0,
            },
        )

    previous = previous.copy()
    latest = latest.copy()

    previous["nct_id"] = (
        previous["nct_id"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    latest["nct_id"] = (
        latest["nct_id"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    previous = previous[
        previous["nct_id"] != ""
    ].drop_duplicates(
        subset=["nct_id"],
        keep="last",
    )

    latest = latest[
        latest["nct_id"] != ""
    ].drop_duplicates(
        subset=["nct_id"],
        keep="last",
    )

    previous_indexed = previous.set_index(
        "nct_id"
    )

    latest_indexed = latest.set_index(
        "nct_id"
    )

    detected_at = datetime.now(
        timezone.utc
    ).isoformat()

    rows: list[dict] = []

    new_count = 0
    updated_count = 0
    unchanged_count = 0

    for nct_id, latest_row in latest_indexed.iterrows():
        if nct_id not in previous_indexed.index:
            new_count += 1

            rows.append(
                {
                    "detected_at": detected_at,
                    "change_type": "NEW",
                    "nct_id": nct_id,
                    "changed_fields": (
                        ",".join(MONITORED_COLUMNS)
                    ),
                    "previous_status": None,
                    "current_status": latest_row.get(
                        "status"
                    ),
                    "previous_last_update_posted_date": None,
                    "current_last_update_posted_date": (
                        latest_row.get(
                            "last_update_posted_date"
                        )
                    ),
                }
            )

            continue

        previous_row = previous_indexed.loc[
            nct_id
        ]

        fields = changed_fields(
            previous_row,
            latest_row,
        )

        if fields:
            updated_count += 1

            rows.append(
                {
                    "detected_at": detected_at,
                    "change_type": "UPDATED",
                    "nct_id": nct_id,
                    "changed_fields": ",".join(
                        fields
                    ),
                    "previous_status": (
                        previous_row.get("status")
                    ),
                    "current_status": (
                        latest_row.get("status")
                    ),
                    "previous_last_update_posted_date": (
                        previous_row.get(
                            "last_update_posted_date"
                        )
                    ),
                    "current_last_update_posted_date": (
                        latest_row.get(
                            "last_update_posted_date"
                        )
                    ),
                }
            )
        else:
            unchanged_count += 1

    changes = pd.DataFrame(
        rows,
        columns=change_columns,
    )

    metrics = {
        "new": new_count,
        "updated": updated_count,
        "unchanged": unchanged_count,
    }

    return changes, metrics


def append_change_history(
    changes: pd.DataFrame,
) -> None:
    """Append detected changes to the history file."""

    if changes.empty:
        return

    CHANGE_HISTORY_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    write_header = not CHANGE_HISTORY_FILE.exists()

    changes.to_csv(
        CHANGE_HISTORY_FILE,
        mode="a",
        header=write_header,
        index=False,
    )