from __future__ import annotations

import argparse
import random
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd
from faker import Faker


def build_patients(fake: Faker, count: int, rng: random.Random) -> pd.DataFrame:
    rows = []
    for patient_id in range(1, count + 1):
        birth_date = fake.date_of_birth(minimum_age=0, maximum_age=95)
        rows.append(
            {
                "patient_id": patient_id,
                "mrn": f"MRN{patient_id:07d}",
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "date_of_birth": birth_date.isoformat(),
                "gender": rng.choice(["Female", "Male", "Unknown"]),
                "phone": fake.phone_number(),
                "postal_code": fake.postcode(),
            }
        )

    df = pd.DataFrame(rows)

    # Controlled quality defects
    if count >= 20:
        df.loc[2, "date_of_birth"] = None
        df.loc[5, "gender"] = "X-invalid"
        df.loc[8, "date_of_birth"] = (date.today() + timedelta(days=30)).isoformat()
        duplicate = df.iloc[[10]].copy()
        duplicate["patient_id"] = count + 1
        df = pd.concat([df, duplicate], ignore_index=True)

    return df


def build_appointments(
    fake: Faker,
    patients: pd.DataFrame,
    count: int,
    rng: random.Random,
) -> pd.DataFrame:
    valid_ids = patients["patient_id"].tolist()
    rows = []

    for appointment_id in range(1, count + 1):
        scheduled_at = fake.date_time_between(start_date="-180d", end_date="+60d")
        rows.append(
            {
                "appointment_id": appointment_id,
                "patient_id": rng.choice(valid_ids),
                "scheduled_at": scheduled_at.isoformat(),
                "status": rng.choice(
                    ["Scheduled", "Completed", "No Show", "Cancelled"]
                ),
                "department": rng.choice(
                    ["Primary Care", "Cardiology", "Pulmonology", "Endocrinology"]
                ),
            }
        )

    df = pd.DataFrame(rows)
    if count >= 20:
        df.loc[3, "patient_id"] = max(valid_ids) + 999  # orphan record
    return df


def build_labs(
    fake: Faker,
    patients: pd.DataFrame,
    count: int,
    rng: random.Random,
) -> pd.DataFrame:
    valid_ids = patients["patient_id"].tolist()
    tests = {
        "HbA1c": (4.0, 12.0, "%"),
        "Hemoglobin": (8.0, 18.0, "g/dL"),
        "Creatinine": (0.4, 3.0, "mg/dL"),
        "Sodium": (125.0, 150.0, "mmol/L"),
    }

    rows = []
    for lab_id in range(1, count + 1):
        test_name = rng.choice(list(tests))
        low, high, unit = tests[test_name]
        rows.append(
            {
                "lab_id": lab_id,
                "patient_id": rng.choice(valid_ids),
                "test_name": test_name,
                "result_value": round(rng.uniform(low, high), 2),
                "unit": unit,
                "collected_at": fake.date_time_between(
                    start_date="-365d", end_date="now"
                ).isoformat(),
            }
        )

    df = pd.DataFrame(rows)
    if count >= 20:
        df.loc[4, "result_value"] = -25
        df.loc[9, "patient_id"] = max(valid_ids) + 500
    return df


def build_insurance(
    patients: pd.DataFrame,
    rng: random.Random,
) -> pd.DataFrame:
    payers = ["Aetna", "Anthem", "Cigna", "Medicare", "Medicaid", "Self Pay"]
    rows = []

    for coverage_id, patient_id in enumerate(
        patients["patient_id"].tolist(), start=1
    ):
        if rng.random() < 0.08:
            continue
        rows.append(
            {
                "coverage_id": coverage_id,
                "patient_id": patient_id,
                "payer_name": rng.choice(payers),
                "member_id": f"MEM{rng.randint(100000, 999999)}",
                "active": rng.choice([True, True, True, False]),
            }
        )

    return pd.DataFrame(rows)


def build_claims(
    fake: Faker,
    patients: pd.DataFrame,
    count: int,
    rng: random.Random,
) -> pd.DataFrame:
    valid_ids = patients["patient_id"].tolist()
    rows = []

    for claim_id in range(1, count + 1):
        billed = round(rng.uniform(75, 5000), 2)
        paid = round(billed * rng.uniform(0.35, 1.0), 2)
        rows.append(
            {
                "claim_id": claim_id,
                "patient_id": rng.choice(valid_ids),
                "service_date": fake.date_between(
                    start_date="-365d", end_date="today"
                ).isoformat(),
                "diagnosis_code": rng.choice(
                    ["E11.9", "I10", "J44.9", "Z00.00", "M54.50"]
                ),
                "billed_amount": billed,
                "paid_amount": paid,
                "claim_status": rng.choice(
                    ["Paid", "Pending", "Denied", "Partially Paid"]
                ),
            }
        )

    df = pd.DataFrame(rows)
    if count >= 20:
        df.loc[6, "billed_amount"] = -100
        df.loc[12, "paid_amount"] = df.loc[12, "billed_amount"] + 250
    return df


def write_dataset(df: pd.DataFrame, output_dir: Path, name: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{name}.csv"
    df.to_csv(path, index=False)
    print(f"Wrote {len(df):,} rows to {path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate synthetic healthcare data with controlled defects."
    )
    parser.add_argument("--patients", type=int, default=500)
    parser.add_argument("--appointments", type=int, default=1500)
    parser.add_argument("--labs", type=int, default=2500)
    parser.add_argument("--claims", type=int, default=1200)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/raw"),
    )
    args = parser.parse_args()

    rng = random.Random(args.seed)
    Faker.seed(args.seed)
    fake = Faker()

    patients = build_patients(fake, args.patients, rng)
    appointments = build_appointments(fake, patients, args.appointments, rng)
    labs = build_labs(fake, patients, args.labs, rng)
    insurance = build_insurance(patients, rng)
    claims = build_claims(fake, patients, args.claims, rng)

    write_dataset(patients, args.output_dir, "patients")
    write_dataset(appointments, args.output_dir, "appointments")
    write_dataset(labs, args.output_dir, "labs")
    write_dataset(insurance, args.output_dir, "insurance")
    write_dataset(claims, args.output_dir, "claims")

    manifest = {
        "generated_at": datetime.now().isoformat(),
        "seed": args.seed,
        "row_counts": {
            "patients": len(patients),
            "appointments": len(appointments),
            "labs": len(labs),
            "insurance": len(insurance),
            "claims": len(claims),
        },
    }
    manifest_path = args.output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Wrote manifest to {manifest_path}")


if __name__ == "__main__":
    import json
    main()
