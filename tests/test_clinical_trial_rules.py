import pandas as pd

from src.quality.clinical_trial_rules import (
    check_clinical_trials,
)


def valid_trial() -> dict:
    return {
        "nct_id": "NCT00000001",
        "title": "Example Cancer Study",
        "condition": "Cancer",
        "phase": "PHASE2",
        "sponsor": "Example Research Center",
        "status": "RECRUITING",
        "start_date": "2026-01-01",
        "completion_date": "2027-01-01",
    }


def test_valid_trial_has_no_issues():
    issues = check_clinical_trials(
        pd.DataFrame([valid_trial()])
    )

    assert issues.empty


def test_missing_nct_id_is_detected():
    trial = valid_trial()
    trial["nct_id"] = None

    issues = check_clinical_trials(
        pd.DataFrame([trial])
    )

    assert "MISSING_NCT_ID" in issues["rule"].tolist()


def test_duplicate_nct_id_is_detected():
    first = valid_trial()
    second = valid_trial()
    second["title"] = "Second Study"

    issues = check_clinical_trials(
        pd.DataFrame([first, second])
    )

    duplicates = issues[
        issues["rule"] == "DUPLICATE_NCT_ID"
    ]

    assert len(duplicates) == 2


def test_invalid_status_is_detected():
    trial = valid_trial()
    trial["status"] = "INVALID_STATUS"

    issues = check_clinical_trials(
        pd.DataFrame([trial])
    )

    assert "INVALID_TRIAL_STATUS" in issues[
        "rule"
    ].tolist()


def test_completion_before_start_is_detected():
    trial = valid_trial()
    trial["start_date"] = "2027-01-01"
    trial["completion_date"] = "2026-01-01"

    issues = check_clinical_trials(
        pd.DataFrame([trial])
    )

    assert "COMPLETION_BEFORE_START_DATE" in issues[
        "rule"
    ].tolist()