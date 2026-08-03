from __future__ import annotations

import re

import pandas as pd

from src.quality.models import Issue


VALID_US_STATE_CODES = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE",
    "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS",
    "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS",
    "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY",
    "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV",
    "WI", "WY", "DC", "PR", "VI", "GU", "AS", "MP",
}

VALID_EMERGENCY_SERVICE_VALUES = {
    "Yes",
    "No",
}

VALID_HOSPITAL_RATINGS = {
    "1",
    "2",
    "3",
    "4",
    "5",
    "Not Available",
}

ZIP_CODE_PATTERN = re.compile(
    r"^\d{5}(?:-\d{4})?$"
)


def check_cms_hospitals(
    hospitals: pd.DataFrame,
) -> pd.DataFrame:
    """Run quality checks against CMS hospital data."""

    issues: list[Issue] = []

    for _, row in hospitals.iterrows():
        facility_id = row.get("facility_id")
        record_id = (
            facility_id
            if not pd.isna(facility_id)
            else "UNKNOWN"
        )

        if pd.isna(facility_id) or not str(
            facility_id
        ).strip():
            issues.append(
                Issue(
                    dataset="cms_hospitals",
                    record_id=record_id,
                    field="facility_id",
                    rule="MISSING_FACILITY_ID",
                    severity="Critical",
                    message="CMS facility ID is missing.",
                )
            )

        if pd.isna(row.get("facility_name")) or not str(
            row.get("facility_name")
        ).strip():
            issues.append(
                Issue(
                    dataset="cms_hospitals",
                    record_id=record_id,
                    field="facility_name",
                    rule="MISSING_FACILITY_NAME",
                    severity="Critical",
                    message="Hospital facility name is missing.",
                )
            )

        if pd.isna(row.get("address")) or not str(
            row.get("address")
        ).strip():
            issues.append(
                Issue(
                    dataset="cms_hospitals",
                    record_id=record_id,
                    field="address",
                    rule="MISSING_HOSPITAL_ADDRESS",
                    severity="High",
                    message="Hospital address is missing.",
                )
            )

        state = row.get("state")

        if pd.isna(state) or str(state).strip() not in (
            VALID_US_STATE_CODES
        ):
            issues.append(
                Issue(
                    dataset="cms_hospitals",
                    record_id=record_id,
                    field="state",
                    rule="INVALID_STATE_CODE",
                    severity="High",
                    message=(
                        f"State value '{state}' is not a valid "
                        "US state or territory code."
                    ),
                )
            )

        zip_code = row.get("zip_code")
        zip_text = (
            ""
            if pd.isna(zip_code)
            else str(zip_code).strip()
        )

        if not ZIP_CODE_PATTERN.fullmatch(zip_text):
            issues.append(
                Issue(
                    dataset="cms_hospitals",
                    record_id=record_id,
                    field="zip_code",
                    rule="INVALID_ZIP_CODE",
                    severity="Medium",
                    message=(
                        f"ZIP code '{zip_code}' is not in a "
                        "valid 5-digit or ZIP+4 format."
                    ),
                )
            )

        emergency_services = row.get(
            "emergency_services"
        )

        if emergency_services not in (
            VALID_EMERGENCY_SERVICE_VALUES
        ):
            issues.append(
                Issue(
                    dataset="cms_hospitals",
                    record_id=record_id,
                    field="emergency_services",
                    rule="INVALID_EMERGENCY_SERVICES_VALUE",
                    severity="Medium",
                    message=(
                        f"Emergency-services value "
                        f"'{emergency_services}' must be Yes or No."
                    ),
                )
            )

        rating = row.get("hospital_overall_rating")
        rating_text = (
            ""
            if pd.isna(rating)
            else str(rating).strip()
        )

        if rating_text not in VALID_HOSPITAL_RATINGS:
            issues.append(
                Issue(
                    dataset="cms_hospitals",
                    record_id=record_id,
                    field="hospital_overall_rating",
                    rule="INVALID_HOSPITAL_RATING",
                    severity="High",
                    message=(
                        f"Hospital rating '{rating}' is not "
                        "within the accepted CMS values."
                    ),
                )
            )

        if pd.isna(row.get("hospital_type")) or not str(
            row.get("hospital_type")
        ).strip():
            issues.append(
                Issue(
                    dataset="cms_hospitals",
                    record_id=record_id,
                    field="hospital_type",
                    rule="MISSING_HOSPITAL_TYPE",
                    severity="High",
                    message="Hospital type is missing.",
                )
            )

        if pd.isna(
            row.get("hospital_ownership")
        ) or not str(
            row.get("hospital_ownership")
        ).strip():
            issues.append(
                Issue(
                    dataset="cms_hospitals",
                    record_id=record_id,
                    field="hospital_ownership",
                    rule="MISSING_HOSPITAL_OWNERSHIP",
                    severity="High",
                    message="Hospital ownership is missing.",
                )
            )

    duplicate_rows = hospitals[
        hospitals.duplicated(
            subset=["facility_id"],
            keep=False,
        )
    ]

    for _, row in duplicate_rows.iterrows():
        issues.append(
            Issue(
                dataset="cms_hospitals",
                record_id=row["facility_id"],
                field="facility_id",
                rule="DUPLICATE_FACILITY_ID",
                severity="Critical",
                message=(
                    f"Facility ID '{row['facility_id']}' "
                    "appears more than once."
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