from __future__ import annotations

import pandas as pd

from src.quality.models import Issue


VALID_ACTIVE_VALUES = {
    True,
    False,
    "True",
    "False",
    "true",
    "false",
    1,
    0,
}


def check_insurance(
    insurance: pd.DataFrame,
    patients: pd.DataFrame,
) -> pd.DataFrame:
    """Run data-quality checks against insurance coverage data."""

    issues: list[Issue] = []
    valid_patient_ids = set(patients["patient_id"])

    for _, row in insurance.iterrows():
        coverage_id = row["coverage_id"]
        patient_id = row["patient_id"]

        if patient_id not in valid_patient_ids:
            issues.append(
                Issue(
                    dataset="insurance",
                    record_id=coverage_id,
                    field="patient_id",
                    rule="ORPHAN_PATIENT",
                    severity="Critical",
                    message=(
                        f"Coverage references patient ID "
                        f"'{patient_id}', which does not exist."
                    ),
                )
            )

        if pd.isna(row["payer_name"]) or not str(
            row["payer_name"]
        ).strip():
            issues.append(
                Issue(
                    dataset="insurance",
                    record_id=coverage_id,
                    field="payer_name",
                    rule="MISSING_PAYER_NAME",
                    severity="High",
                    message="Insurance payer name is missing.",
                )
            )

        if pd.isna(row["member_id"]) or not str(
            row["member_id"]
        ).strip():
            issues.append(
                Issue(
                    dataset="insurance",
                    record_id=coverage_id,
                    field="member_id",
                    rule="MISSING_MEMBER_ID",
                    severity="High",
                    message="Insurance member ID is missing.",
                )
            )

        if row["active"] not in VALID_ACTIVE_VALUES:
            issues.append(
                Issue(
                    dataset="insurance",
                    record_id=coverage_id,
                    field="active",
                    rule="INVALID_ACTIVE_STATUS",
                    severity="Medium",
                    message=(
                        f"Insurance active status "
                        f"'{row['active']}' is invalid."
                    ),
                )
            )

    duplicate_rows = insurance[
        insurance.duplicated(
            subset=[
                "patient_id",
                "payer_name",
                "member_id",
            ],
            keep=False,
        )
    ]

    for _, row in duplicate_rows.iterrows():
        issues.append(
            Issue(
                dataset="insurance",
                record_id=row["coverage_id"],
                field="member_id",
                rule="DUPLICATE_COVERAGE",
                severity="High",
                message=(
                    "The same patient, payer, and member ID "
                    "combination appears more than once."
                ),
            )
        )

    return pd.DataFrame(
        [issue.to_dict() for issue in issues],
        columns=[
            "dataset",
            "record_id",
            "field",
            "rule",
            "severity",
            "message",
        ],
    )