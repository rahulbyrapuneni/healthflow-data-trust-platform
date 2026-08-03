from __future__ import annotations

import pandas as pd

from src.quality.models import Issue


PLAUSIBLE_RANGES = {
    "HbA1c": (2.0, 25.0),
    "Hemoglobin": (3.0, 25.0),
    "Creatinine": (0.1, 20.0),
    "Sodium": (90.0, 200.0),
}


def check_labs(
    labs: pd.DataFrame,
    patients: pd.DataFrame,
) -> pd.DataFrame:
    """Run data-quality checks against laboratory data."""

    issues: list[Issue] = []
    valid_patient_ids = set(patients["patient_id"])

    for _, row in labs.iterrows():
        lab_id = row["lab_id"]
        patient_id = row["patient_id"]
        test_name = row["test_name"]

        if patient_id not in valid_patient_ids:
            issues.append(
                Issue(
                    dataset="labs",
                    record_id=lab_id,
                    field="patient_id",
                    rule="ORPHAN_PATIENT",
                    severity="Critical",
                    message=(
                        f"Lab result references patient ID "
                        f"'{patient_id}', which does not exist."
                    ),
                )
            )

        result_value = pd.to_numeric(
            row["result_value"],
            errors="coerce",
        )

        if pd.isna(result_value):
            issues.append(
                Issue(
                    dataset="labs",
                    record_id=lab_id,
                    field="result_value",
                    rule="INVALID_LAB_RESULT",
                    severity="High",
                    message="Lab result is missing or not numeric.",
                )
            )

        elif result_value < 0:
            issues.append(
                Issue(
                    dataset="labs",
                    record_id=lab_id,
                    field="result_value",
                    rule="NEGATIVE_LAB_RESULT",
                    severity="Critical",
                    message=(
                        f"Lab result value '{result_value}' "
                        "cannot be negative."
                    ),
                )
            )

        elif test_name in PLAUSIBLE_RANGES:
            minimum, maximum = PLAUSIBLE_RANGES[test_name]

            if not minimum <= result_value <= maximum:
                issues.append(
                    Issue(
                        dataset="labs",
                        record_id=lab_id,
                        field="result_value",
                        rule="IMPLAUSIBLE_LAB_RESULT",
                        severity="High",
                        message=(
                            f"{test_name} result '{result_value}' "
                            f"is outside the plausible range "
                            f"{minimum}–{maximum}."
                        ),
                    )
                )

        if pd.isna(row["unit"]) or not str(row["unit"]).strip():
            issues.append(
                Issue(
                    dataset="labs",
                    record_id=lab_id,
                    field="unit",
                    rule="MISSING_LAB_UNIT",
                    severity="Medium",
                    message="Lab result unit is missing.",
                )
            )

        collected_at = pd.to_datetime(
            row["collected_at"],
            errors="coerce",
        )

        if pd.isna(collected_at):
            issues.append(
                Issue(
                    dataset="labs",
                    record_id=lab_id,
                    field="collected_at",
                    rule="INVALID_COLLECTION_DATE",
                    severity="High",
                    message="Lab collection date is invalid.",
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