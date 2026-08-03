import pandas as pd

from src.quality.claim_rules import check_claims


def test_negative_billed_amount_is_detected():
    patients = pd.DataFrame(
        [{"patient_id": 1}]
    )

    claims = pd.DataFrame(
        [
            {
                "claim_id": 10,
                "patient_id": 1,
                "service_date": "2026-07-01",
                "diagnosis_code": "I10",
                "billed_amount": -100,
                "paid_amount": 0,
                "claim_status": "Denied",
            }
        ]
    )

    issues = check_claims(
        claims=claims,
        patients=patients,
    )

    assert "NEGATIVE_BILLED_AMOUNT" in issues["rule"].tolist()


def test_paid_amount_exceeding_billed_is_detected():
    patients = pd.DataFrame(
        [{"patient_id": 1}]
    )

    claims = pd.DataFrame(
        [
            {
                "claim_id": 11,
                "patient_id": 1,
                "service_date": "2026-07-01",
                "diagnosis_code": "E11.9",
                "billed_amount": 500,
                "paid_amount": 650,
                "claim_status": "Paid",
            }
        ]
    )

    issues = check_claims(
        claims=claims,
        patients=patients,
    )

    assert "PAID_EXCEEDS_BILLED" in issues["rule"].tolist()


def test_valid_claim_has_no_issues():
    patients = pd.DataFrame(
        [{"patient_id": 1}]
    )

    claims = pd.DataFrame(
        [
            {
                "claim_id": 12,
                "patient_id": 1,
                "service_date": "2026-07-01",
                "diagnosis_code": "J44.9",
                "billed_amount": 500,
                "paid_amount": 400,
                "claim_status": "Paid",
            }
        ]
    )

    issues = check_claims(
        claims=claims,
        patients=patients,
    )

    assert issues.empty