import pandas as pd

from src.quality.cms_hospital_rules import (
    check_cms_hospitals,
)


def valid_hospital() -> dict:
    return {
        "facility_id": "010001",
        "facility_name": "Example Hospital",
        "address": "100 Main Street",
        "citytown": "Birmingham",
        "state": "AL",
        "zip_code": "35203",
        "countyparish": "Jefferson",
        "telephone_number": "(205) 555-1000",
        "hospital_type": "Acute Care Hospitals",
        "hospital_ownership": "Voluntary non-profit - Private",
        "emergency_services": "Yes",
        "hospital_overall_rating": "4",
    }


def test_valid_cms_hospital_has_no_issues():
    hospitals = pd.DataFrame([valid_hospital()])

    issues = check_cms_hospitals(hospitals)

    assert issues.empty


def test_invalid_state_is_detected():
    hospital = valid_hospital()
    hospital["state"] = "XX"

    issues = check_cms_hospitals(
        pd.DataFrame([hospital])
    )

    assert "INVALID_STATE_CODE" in issues[
        "rule"
    ].tolist()


def test_invalid_zip_is_detected():
    hospital = valid_hospital()
    hospital["zip_code"] = "ABC"

    issues = check_cms_hospitals(
        pd.DataFrame([hospital])
    )

    assert "INVALID_ZIP_CODE" in issues[
        "rule"
    ].tolist()


def test_duplicate_facility_id_is_detected():
    first = valid_hospital()
    second = valid_hospital()
    second["facility_name"] = "Second Hospital"

    issues = check_cms_hospitals(
        pd.DataFrame([first, second])
    )

    duplicates = issues[
        issues["rule"] == "DUPLICATE_FACILITY_ID"
    ]

    assert len(duplicates) == 2


def test_invalid_rating_is_detected():
    hospital = valid_hospital()
    hospital["hospital_overall_rating"] = "9"

    issues = check_cms_hospitals(
        pd.DataFrame([hospital])
    )

    assert "INVALID_HOSPITAL_RATING" in issues[
        "rule"
    ].tolist()