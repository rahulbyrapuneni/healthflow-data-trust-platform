import random

from faker import Faker

from src.simulator.generate_data import build_patients


def test_patient_generator_creates_requested_minimum_rows():
    fake = Faker()
    rng = random.Random(42)
    patients = build_patients(fake, 25, rng)

    # One controlled duplicate row is intentionally added.
    assert len(patients) == 26
    assert "patient_id" in patients.columns
    assert "mrn" in patients.columns
