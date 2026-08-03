from __future__ import annotations

import pandas as pd

from src.quality.models import Issue


VALID_APPOINTMENT_STATUSES = {
    "Scheduled",
    "Completed",
    "No Show",
    "Cancelled",
}


def check_appointments(
    appointments: pd.DataFrame,
    patients: pd.DataFrame,
) -> pd.DataFrame:
    """Run data-quality checks against appointment data."""

    issues: list[Issue] = []

    valid_patient_ids = set(patients["patient_id"])

    for _, row in appointments.iterrows():
        appointment_id = row["appointment_id"]
        patient_id = row["patient_id"]

        if patient_id not in valid_patient_ids:
            issues.append(
                Issue(
                    dataset="appointments",
                    record_id=appointment_id,
                    field="patient_id",
                    rule="ORPHAN_PATIENT",
                    severity="Critical",
                    message=(
                        f"Appointment references patient ID "
                        f"'{patient_id}', which does not exist."
                    ),
                )
            )

        if row["status"] not in VALID_APPOINTMENT_STATUSES:
            issues.append(
                Issue(
                    dataset="appointments",
                    record_id=appointment_id,
                    field="status",
                    rule="INVALID_APPOINTMENT_STATUS",
                    severity="Medium",
                    message=(
                        f"Appointment status "
                        f"'{row['status']}' is invalid."
                    ),
                )
            )

        if pd.isna(row["department"]) or not str(
            row["department"]
        ).strip():
            issues.append(
                Issue(
                    dataset="appointments",
                    record_id=appointment_id,
                    field="department",
                    rule="MISSING_DEPARTMENT",
                    severity="Low",
                    message="Appointment department is missing.",
                )
            )

        scheduled_at = pd.to_datetime(
            row["scheduled_at"],
            errors="coerce",
        )

        if pd.isna(scheduled_at):
            issues.append(
                Issue(
                    dataset="appointments",
                    record_id=appointment_id,
                    field="scheduled_at",
                    rule="INVALID_SCHEDULED_DATE",
                    severity="High",
                    message="Appointment scheduled date is invalid.",
                )
            )

    issue_records = [issue.to_dict() for issue in issues]

    return pd.DataFrame(
        issue_records,
        columns=[
            "dataset",
            "record_id",
            "field",
            "rule",
            "severity",
            "message",
        ],
    )