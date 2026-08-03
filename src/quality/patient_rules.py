from __future__ import annotations

from datetime import date

import pandas as pd

from src.quality.models import Issue


VALID_GENDERS = {"Female", "Male", "Unknown"}


def check_patients(patients: pd.DataFrame) -> pd.DataFrame:
    """Run data-quality checks against the patient dataset."""

    issues: list[Issue] = []

    for _, row in patients.iterrows():
        patient_id = row["patient_id"]

        if pd.isna(row["date_of_birth"]):
            issues.append(
                Issue(
                    dataset="patients",
                    record_id=patient_id,
                    field="date_of_birth",
                    rule="MISSING_DATE_OF_BIRTH",
                    severity="High",
                    message="Patient date of birth is missing.",
                )
            )

        else:
            birth_date = pd.to_datetime(
                row["date_of_birth"],
                errors="coerce",
            )

            if pd.isna(birth_date):
                issues.append(
                    Issue(
                        dataset="patients",
                        record_id=patient_id,
                        field="date_of_birth",
                        rule="INVALID_DATE_OF_BIRTH",
                        severity="High",
                        message="Patient date of birth is not a valid date.",
                    )
                )

            elif birth_date.date() > date.today():
                issues.append(
                    Issue(
                        dataset="patients",
                        record_id=patient_id,
                        field="date_of_birth",
                        rule="FUTURE_DATE_OF_BIRTH",
                        severity="Critical",
                        message="Patient date of birth is in the future.",
                    )
                )

        if row["gender"] not in VALID_GENDERS:
            issues.append(
                Issue(
                    dataset="patients",
                    record_id=patient_id,
                    field="gender",
                    rule="INVALID_GENDER",
                    severity="Medium",
                    message=f"Gender value '{row['gender']}' is invalid.",
                )
            )

        if pd.isna(row["first_name"]) or not str(row["first_name"]).strip():
            issues.append(
                Issue(
                    dataset="patients",
                    record_id=patient_id,
                    field="first_name",
                    rule="MISSING_FIRST_NAME",
                    severity="High",
                    message="Patient first name is missing.",
                )
            )

        if pd.isna(row["last_name"]) or not str(row["last_name"]).strip():
            issues.append(
                Issue(
                    dataset="patients",
                    record_id=patient_id,
                    field="last_name",
                    rule="MISSING_LAST_NAME",
                    severity="High",
                    message="Patient last name is missing.",
                )
            )

    duplicate_rows = patients[
        patients.duplicated(subset=["mrn"], keep=False)
    ]

    for _, row in duplicate_rows.iterrows():
        issues.append(
            Issue(
                dataset="patients",
                record_id=row["patient_id"],
                field="mrn",
                rule="DUPLICATE_MRN",
                severity="Critical",
                message=f"MRN '{row['mrn']}' appears more than once.",
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