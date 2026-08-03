from __future__ import annotations

import pandas as pd

from src.quality.models import Issue


VALID_CLAIM_STATUSES = {
    "Paid",
    "Pending",
    "Denied",
    "Partially Paid",
}


def check_claims(
    claims: pd.DataFrame,
    patients: pd.DataFrame,
) -> pd.DataFrame:
    """Run data-quality checks against claims data."""

    issues: list[Issue] = []
    valid_patient_ids = set(patients["patient_id"])

    for _, row in claims.iterrows():
        claim_id = row["claim_id"]
        patient_id = row["patient_id"]

        if patient_id not in valid_patient_ids:
            issues.append(
                Issue(
                    dataset="claims",
                    record_id=claim_id,
                    field="patient_id",
                    rule="ORPHAN_PATIENT",
                    severity="Critical",
                    message=(
                        f"Claim references patient ID "
                        f"'{patient_id}', which does not exist."
                    ),
                )
            )

        billed_amount = pd.to_numeric(
            row["billed_amount"],
            errors="coerce",
        )

        paid_amount = pd.to_numeric(
            row["paid_amount"],
            errors="coerce",
        )

        if pd.isna(billed_amount):
            issues.append(
                Issue(
                    dataset="claims",
                    record_id=claim_id,
                    field="billed_amount",
                    rule="INVALID_BILLED_AMOUNT",
                    severity="High",
                    message="Billed amount is missing or not numeric.",
                )
            )

        elif billed_amount < 0:
            issues.append(
                Issue(
                    dataset="claims",
                    record_id=claim_id,
                    field="billed_amount",
                    rule="NEGATIVE_BILLED_AMOUNT",
                    severity="Critical",
                    message=(
                        f"Billed amount '{billed_amount}' "
                        "cannot be negative."
                    ),
                )
            )

        if pd.isna(paid_amount):
            issues.append(
                Issue(
                    dataset="claims",
                    record_id=claim_id,
                    field="paid_amount",
                    rule="INVALID_PAID_AMOUNT",
                    severity="High",
                    message="Paid amount is missing or not numeric.",
                )
            )

        elif paid_amount < 0:
            issues.append(
                Issue(
                    dataset="claims",
                    record_id=claim_id,
                    field="paid_amount",
                    rule="NEGATIVE_PAID_AMOUNT",
                    severity="Critical",
                    message=(
                        f"Paid amount '{paid_amount}' "
                        "cannot be negative."
                    ),
                )
            )

        if (
            not pd.isna(billed_amount)
            and not pd.isna(paid_amount)
            and billed_amount >= 0
            and paid_amount > billed_amount
        ):
            issues.append(
                Issue(
                    dataset="claims",
                    record_id=claim_id,
                    field="paid_amount",
                    rule="PAID_EXCEEDS_BILLED",
                    severity="Critical",
                    message=(
                        f"Paid amount '{paid_amount}' exceeds "
                        f"billed amount '{billed_amount}'."
                    ),
                )
            )

        if pd.isna(row["diagnosis_code"]) or not str(
            row["diagnosis_code"]
        ).strip():
            issues.append(
                Issue(
                    dataset="claims",
                    record_id=claim_id,
                    field="diagnosis_code",
                    rule="MISSING_DIAGNOSIS_CODE",
                    severity="High",
                    message="Diagnosis code is missing.",
                )
            )

        if row["claim_status"] not in VALID_CLAIM_STATUSES:
            issues.append(
                Issue(
                    dataset="claims",
                    record_id=claim_id,
                    field="claim_status",
                    rule="INVALID_CLAIM_STATUS",
                    severity="Medium",
                    message=(
                        f"Claim status "
                        f"'{row['claim_status']}' is invalid."
                    ),
                )
            )

        service_date = pd.to_datetime(
            row["service_date"],
            errors="coerce",
        )

        if pd.isna(service_date):
            issues.append(
                Issue(
                    dataset="claims",
                    record_id=claim_id,
                    field="service_date",
                    rule="INVALID_SERVICE_DATE",
                    severity="High",
                    message="Claim service date is invalid.",
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