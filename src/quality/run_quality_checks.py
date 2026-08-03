from datetime import date
from pathlib import Path

import pandas as pd

from src.quality.appointment_rules import check_appointments
from src.quality.claim_rules import check_claims
from src.quality.insurance_rules import check_insurance
from src.quality.issue_enrichment import enrich_issues
from src.quality.lab_rules import check_labs
from src.quality.patient_rules import check_patients
from src.quality.platform_report import (
    build_dataset_summary,
    print_platform_report,
)
from src.quality.quality_report import print_quality_report
from src.quality.run_metadata import create_run_metadata


INGESTED_DATA_PATH = Path("data/ingested")
OUTPUT_PATH = Path("data/quality_results")


def load_dataset(dataset_name: str) -> pd.DataFrame:
    """Load one ingested dataset."""

    dataset_path = INGESTED_DATA_PATH / f"{dataset_name}.csv"

    if not dataset_path.exists():
        raise FileNotFoundError(
            f"Ingested {dataset_name}.csv was not found. "
            "Run the ingestion process first."
        )

    return pd.read_csv(dataset_path)


def main() -> None:
    run_metadata = create_run_metadata()

    patients = load_dataset("patients")
    appointments = load_dataset("appointments")
    labs = load_dataset("labs")
    claims = load_dataset("claims")
    insurance = load_dataset("insurance")

    patient_issues = check_patients(patients)

    appointment_issues = check_appointments(
        appointments=appointments,
        patients=patients,
    )

    lab_issues = check_labs(
        labs=labs,
        patients=patients,
    )

    claim_issues = check_claims(
        claims=claims,
        patients=patients,
    )

    insurance_issues = check_insurance(
        insurance=insurance,
        patients=patients,
    )

    all_issues = pd.concat(
        [
            patient_issues,
            appointment_issues,
            lab_issues,
            claim_issues,
            insurance_issues,
        ],
        ignore_index=True,
    )

    all_issues = enrich_issues(all_issues)

    all_issues.insert(
        0,
        "run_timestamp",
        run_metadata.run_timestamp,
    )

    all_issues.insert(
        0,
        "run_id",
        run_metadata.run_id,
    )

    dataset_rows = {
        "patients": len(patients),
        "appointments": len(appointments),
        "labs": len(labs),
        "claims": len(claims),
        "insurance": len(insurance),
    }

    dataset_summary = build_dataset_summary(
        dataset_rows=dataset_rows,
        all_issues=all_issues,
    )

    dataset_summary.insert(
        0,
        "run_timestamp",
        run_metadata.run_timestamp,
    )

    dataset_summary.insert(
        0,
        "run_id",
        run_metadata.run_id,
    )

    OUTPUT_PATH.mkdir(
        parents=True,
        exist_ok=True,
    )

    history_path = OUTPUT_PATH / "history"

    history_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = (
        OUTPUT_PATH / "all_quality_issues.csv"
    )

    summary_file = (
        OUTPUT_PATH / "dataset_trust_summary.csv"
    )

    run_date = date.today().isoformat()

    issue_history_file = (
        history_path
        / f"issues_{run_date}_{run_metadata.run_id}.csv"
    )

    summary_history_file = (
        history_path
        / f"summary_{run_date}_{run_metadata.run_id}.csv"
    )

    all_issues.to_csv(
        output_file,
        index=False,
    )

    dataset_summary.to_csv(
        summary_file,
        index=False,
    )

    all_issues.to_csv(
        issue_history_file,
        index=False,
    )

    dataset_summary.to_csv(
        summary_history_file,
        index=False,
    )

    print_quality_report(
        dataset_name="Patients",
        row_count=len(patients),
        issues=patient_issues,
    )

    print()

    print_quality_report(
        dataset_name="Appointments",
        row_count=len(appointments),
        issues=appointment_issues,
    )

    print()

    print_quality_report(
        dataset_name="Labs",
        row_count=len(labs),
        issues=lab_issues,
    )

    print()

    print_quality_report(
        dataset_name="Claims",
        row_count=len(claims),
        issues=claim_issues,
    )

    print()

    print_quality_report(
        dataset_name="Insurance",
        row_count=len(insurance),
        issues=insurance_issues,
    )

    print_platform_report(dataset_summary)

    print(f"\nRun ID: {run_metadata.run_id}")
    print(f"Run timestamp: {run_metadata.run_timestamp}")

    print(
        f"\nCombined issue results written to: "
        f"{output_file}"
    )

    print(
        f"Dataset trust summary written to: "
        f"{summary_file}"
    )

    print(
        f"Issue history written to: "
        f"{issue_history_file}"
    )

    print(
        f"Summary history written to: "
        f"{summary_history_file}"
    )


if __name__ == "__main__":
    main()