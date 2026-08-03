import pandas as pd

from src.quality.lab_rules import check_labs


def test_negative_lab_result_is_detected():
    patients = pd.DataFrame(
        [{"patient_id": 1}]
    )

    labs = pd.DataFrame(
        [
            {
                "lab_id": 10,
                "patient_id": 1,
                "test_name": "HbA1c",
                "result_value": -5,
                "unit": "%",
                "collected_at": "2026-07-01T09:00:00",
            }
        ]
    )

    issues = check_labs(
        labs=labs,
        patients=patients,
    )

    assert "NEGATIVE_LAB_RESULT" in issues["rule"].tolist()


def test_orphan_lab_patient_is_detected():
    patients = pd.DataFrame(
        [{"patient_id": 1}]
    )

    labs = pd.DataFrame(
        [
            {
                "lab_id": 11,
                "patient_id": 999,
                "test_name": "Creatinine",
                "result_value": 1.2,
                "unit": "mg/dL",
                "collected_at": "2026-07-01T09:00:00",
            }
        ]
    )

    issues = check_labs(
        labs=labs,
        patients=patients,
    )

    assert "ORPHAN_PATIENT" in issues["rule"].tolist()


def test_valid_lab_has_no_issues():
    patients = pd.DataFrame(
        [{"patient_id": 1}]
    )

    labs = pd.DataFrame(
        [
            {
                "lab_id": 12,
                "patient_id": 1,
                "test_name": "Creatinine",
                "result_value": 1.1,
                "unit": "mg/dL",
                "collected_at": "2026-07-01T09:00:00",
            }
        ]
    )

    issues = check_labs(
        labs=labs,
        patients=patients,
    )

    assert issues.empty