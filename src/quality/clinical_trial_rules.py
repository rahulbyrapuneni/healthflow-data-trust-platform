from __future__ import annotations

import pandas as pd

from src.quality.models import Issue


VALID_TRIAL_STATUSES = {
    "NOT_YET_RECRUITING",
    "RECRUITING",
    "ENROLLING_BY_INVITATION",
    "ACTIVE_NOT_RECRUITING",
    "SUSPENDED",
    "TERMINATED",
    "COMPLETED",
    "WITHDRAWN",
    "UNKNOWN",
}

VALID_PHASES = {
    "EARLY_PHASE1",
    "PHASE1",
    "PHASE2",
    "PHASE3",
    "PHASE4",
    "NA",
}


def is_missing(value: object) -> bool:
    """Return whether a trial field is missing or blank."""

    return pd.isna(value) or not str(value).strip()


def check_clinical_trials(
    trials: pd.DataFrame,
) -> pd.DataFrame:
    """Run quality checks against ClinicalTrials.gov records."""

    issues: list[Issue] = []

    for _, row in trials.iterrows():
        nct_id = row.get("nct_id")

        record_id = (
            str(nct_id).strip()
            if not is_missing(nct_id)
            else "UNKNOWN"
        )

        if is_missing(nct_id):
            issues.append(
                Issue(
                    dataset="clinical_trials",
                    record_id=record_id,
                    field="nct_id",
                    rule="MISSING_NCT_ID",
                    severity="Critical",
                    message="Clinical trial NCT identifier is missing.",
                )
            )

        if is_missing(row.get("title")):
            issues.append(
                Issue(
                    dataset="clinical_trials",
                    record_id=record_id,
                    field="title",
                    rule="MISSING_TRIAL_TITLE",
                    severity="High",
                    message="Clinical trial title is missing.",
                )
            )

        if is_missing(row.get("condition")):
            issues.append(
                Issue(
                    dataset="clinical_trials",
                    record_id=record_id,
                    field="condition",
                    rule="MISSING_TRIAL_CONDITION",
                    severity="High",
                    message="Clinical trial condition is missing.",
                )
            )

        if is_missing(row.get("sponsor")):
            issues.append(
                Issue(
                    dataset="clinical_trials",
                    record_id=record_id,
                    field="sponsor",
                    rule="MISSING_LEAD_SPONSOR",
                    severity="High",
                    message="Clinical trial lead sponsor is missing.",
                )
            )

        status = row.get("status")

        if is_missing(status):
            issues.append(
                Issue(
                    dataset="clinical_trials",
                    record_id=record_id,
                    field="status",
                    rule="MISSING_TRIAL_STATUS",
                    severity="High",
                    message="Clinical trial recruitment status is missing.",
                )
            )
        elif str(status).strip() not in VALID_TRIAL_STATUSES:
            issues.append(
                Issue(
                    dataset="clinical_trials",
                    record_id=record_id,
                    field="status",
                    rule="INVALID_TRIAL_STATUS",
                    severity="Medium",
                    message=(
                        f"Clinical trial status '{status}' is not "
                        "an accepted ClinicalTrials.gov status."
                    ),
                )
            )

        phase = row.get("phase")

        if not is_missing(phase):
            phase_values = {
                value.strip()
                for value in str(phase).split("|")
                if value.strip()
            }

            invalid_phases = (
                phase_values - VALID_PHASES
            )

            if invalid_phases:
                issues.append(
                    Issue(
                        dataset="clinical_trials",
                        record_id=record_id,
                        field="phase",
                        rule="INVALID_TRIAL_PHASE",
                        severity="Medium",
                        message=(
                            "Clinical trial phase contains invalid "
                            f"value(s): {sorted(invalid_phases)}."
                        ),
                    )
                )

        start_date = pd.to_datetime(
            row.get("start_date"),
            errors="coerce",
        )

        completion_date = pd.to_datetime(
            row.get("completion_date"),
            errors="coerce",
        )

        if (
            pd.notna(start_date)
            and pd.notna(completion_date)
            and completion_date < start_date
        ):
            issues.append(
                Issue(
                    dataset="clinical_trials",
                    record_id=record_id,
                    field="completion_date",
                    rule="COMPLETION_BEFORE_START_DATE",
                    severity="High",
                    message=(
                        "Clinical trial completion date occurs "
                        "before the start date."
                    ),
                )
            )

    valid_nct_ids = trials[
        trials["nct_id"].notna()
        & trials["nct_id"].astype(str).str.strip().ne("")
    ]

    duplicate_rows = valid_nct_ids[
        valid_nct_ids.duplicated(
            subset=["nct_id"],
            keep=False,
        )
    ]

    for _, row in duplicate_rows.iterrows():
        issues.append(
            Issue(
                dataset="clinical_trials",
                record_id=str(row["nct_id"]),
                field="nct_id",
                rule="DUPLICATE_NCT_ID",
                severity="Critical",
                message=(
                    f"NCT identifier '{row['nct_id']}' "
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