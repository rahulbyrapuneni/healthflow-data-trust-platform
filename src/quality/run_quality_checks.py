from datetime import date
import logging
from pathlib import Path

import pandas as pd

from src.core.logging_config import configure_logging
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

logger = logging.getLogger("healthflow.quality")


def load_dataset(dataset_name: str) -> pd.DataFrame:
    """Load one ingested dataset."""

    dataset_path = INGESTED_DATA_PATH / f"{dataset_name}.csv"

    if not dataset_path.exists():
        raise FileNotFoundError(
            f"Ingested {dataset_name}.csv was not found. "
            "Run the ingestion process first."
        )

    logger.info(
        "Loading dataset=%s from path=%s",
        dataset_name,
        dataset_path,
    )

    dataframe = pd.read_csv(dataset_path)

    logger.info(
        "Loaded dataset=%s with rows=%s",
        dataset_name,
        len(dataframe),
    )

    return dataframe


def main() -> None:
    configure_logging()

    logger.info("Starting HealthFlow quality-check execution")

    run_metadata = create_run_metadata()

    logger.info(
        "Created quality run with run_id=%s and timestamp=%s",
        run_metadata.run_id,
        run_metadata.run_timestamp,
    )

    patients = load_dataset("patients")
    appointments = load_dataset("appointments")
    labs = load_dataset("labs")
    claims = load_dataset("claims")
    insurance = load_dataset("insurance")

    logger.info(
        (
            "Loaded all datasets: patients=%s, appointments=%s, "
            "labs=%s, claims=%s, insurance=%s"
        ),
        len(patients),
        len(appointments),
        len(labs),
        len(claims),
        len(insurance),
    )

    patient_issues = check_patients(patients)

    logger.info(
        "Patient quality checks completed with issues=%s",
        len(patient_issues),
    )

    appointment_issues = check_appointments(
        appointments=appointments,
        patients=patients,
    )

    logger.info(
        "Appointment quality checks completed with issues=%s",
        len(appointment_issues),
    )

    lab_issues = check_labs(
        labs=labs,
        patients=patients,
    )

    logger.info(
        "Laboratory quality checks completed with issues=%s",
        len(lab_issues),
    )

    claim_issues = check_claims(
        claims=claims,
        patients=patients,
    )

    logger.info(
        "Claim quality checks completed with issues=%s",
        len(claim_issues),
    )

    insurance_issues = check_insurance(
        insurance=insurance,
        patients=patients,
    )

    logger.info(
        "Insurance quality checks completed with issues=%s",
        len(insurance_issues),
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

    logger.info(
        "Combined quality results contain issues=%s",
        len(all_issues),
    )

    all_issues = enrich_issues(all_issues)

    logger.info("Issue enrichment completed")

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

    logger.info(
        "Dataset trust summary created with rows=%s",
        len(dataset_summary),
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

    output_file = OUTPUT_PATH / "all_quality_issues.csv"
    summary_file = OUTPUT_PATH / "dataset_trust_summary.csv"

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

    logger.info(
        "Quality issue report written to path=%s",
        output_file,
    )

    dataset_summary.to_csv(
        summary_file,
        index=False,
    )

    logger.info(
        "Dataset trust summary written to path=%s",
        summary_file,
    )

    all_issues.to_csv(
        issue_history_file,
        index=False,
    )

    logger.info(
        "Issue history written to path=%s",
        issue_history_file,
    )

    dataset_summary.to_csv(
        summary_history_file,
        index=False,
    )

    logger.info(
        "Summary history written to path=%s",
        summary_history_file,
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

    logger.info(
        "HealthFlow quality-check execution completed successfully"
    )


if __name__ == "__main__":
    main()