import pandas as pd

from src.quality.insurance_rules import check_insurance


def test_missing_member_id_is_detected():
    patients = pd.DataFrame(
        [{"patient_id": 1}]
    )

    insurance = pd.DataFrame(
        [
            {
                "coverage_id": 10,
                "patient_id": 1,
                "payer_name": "Aetna",
                "member_id": None,
                "active": True,
            }
        ]
    )

    issues = check_insurance(
        insurance=insurance,
        patients=patients,
    )

    assert "MISSING_MEMBER_ID" in issues["rule"].tolist()


def test_orphan_insurance_patient_is_detected():
    patients = pd.DataFrame(
        [{"patient_id": 1}]
    )

    insurance = pd.DataFrame(
        [
            {
                "coverage_id": 11,
                "patient_id": 999,
                "payer_name": "Anthem",
                "member_id": "MEM123456",
                "active": True,
            }
        ]
    )

    issues = check_insurance(
        insurance=insurance,
        patients=patients,
    )

    assert "ORPHAN_PATIENT" in issues["rule"].tolist()


def test_duplicate_coverage_is_detected():
    patients = pd.DataFrame(
        [{"patient_id": 1}]
    )

    insurance = pd.DataFrame(
        [
            {
                "coverage_id": 12,
                "patient_id": 1,
                "payer_name": "Cigna",
                "member_id": "MEM100001",
                "active": True,
            },
            {
                "coverage_id": 13,
                "patient_id": 1,
                "payer_name": "Cigna",
                "member_id": "MEM100001",
                "active": True,
            },
        ]
    )

    issues = check_insurance(
        insurance=insurance,
        patients=patients,
    )

    duplicate_issues = issues[
        issues["rule"] == "DUPLICATE_COVERAGE"
    ]

    assert len(duplicate_issues) == 2


def test_valid_insurance_has_no_issues():
    patients = pd.DataFrame(
        [{"patient_id": 1}]
    )

    insurance = pd.DataFrame(
        [
            {
                "coverage_id": 14,
                "patient_id": 1,
                "payer_name": "Medicare",
                "member_id": "MEM200001",
                "active": True,
            }
        ]
    )

    issues = check_insurance(
        insurance=insurance,
        patients=patients,
    )

    assert issues.empty