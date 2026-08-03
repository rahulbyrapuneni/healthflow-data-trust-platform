import pandas as pd

from src.quality.appointment_rules import (
    check_appointments,
)


def test_orphan_patient_is_detected():
    patients = pd.DataFrame(
        [
            {
                "patient_id": 1,
            }
        ]
    )

    appointments = pd.DataFrame(
        [
            {
                "appointment_id": 100,
                "patient_id": 999,
                "scheduled_at": "2026-07-01T09:00:00",
                "status": "Scheduled",
                "department": "Cardiology",
            }
        ]
    )

    issues = check_appointments(
        appointments=appointments,
        patients=patients,
    )

    assert len(issues) == 1
    assert issues.iloc[0]["rule"] == "ORPHAN_PATIENT"
    assert issues.iloc[0]["severity"] == "Critical"


def test_valid_appointment_has_no_issues():
    patients = pd.DataFrame(
        [
            {
                "patient_id": 1,
            }
        ]
    )

    appointments = pd.DataFrame(
        [
            {
                "appointment_id": 100,
                "patient_id": 1,
                "scheduled_at": "2026-07-01T09:00:00",
                "status": "Completed",
                "department": "Primary Care",
            }
        ]
    )

    issues = check_appointments(
        appointments=appointments,
        patients=patients,
    )

    assert issues.empty