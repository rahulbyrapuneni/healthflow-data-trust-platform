from __future__ import annotations

from pathlib import Path

import pandas as pd


QUALITY_RESULTS_PATH = Path("data/quality_results")
SUMMARY_FILE = QUALITY_RESULTS_PATH / "dataset_trust_summary.csv"
ISSUES_FILE = QUALITY_RESULTS_PATH / "all_quality_issues.csv"


def load_summary() -> pd.DataFrame:
    """Load the latest dataset-level trust summary."""

    if not SUMMARY_FILE.exists():
        raise FileNotFoundError(
            "dataset_trust_summary.csv was not found. "
            "Run the quality engine first."
        )

    return pd.read_csv(SUMMARY_FILE)


def load_issues() -> pd.DataFrame:
    """Load the latest quality issue results."""

    if not ISSUES_FILE.exists():
        raise FileNotFoundError(
            "all_quality_issues.csv was not found. "
            "Run the quality engine first."
        )

    return pd.read_csv(ISSUES_FILE)


def calculate_platform_score(summary: pd.DataFrame) -> float:
    """Calculate a row-weighted platform trust score."""

    total_rows = summary["rows_checked"].sum()

    if total_rows <= 0:
        return 0.0

    weighted_score = (
        summary["trust_score"]
        * summary["rows_checked"]
    ).sum()

    return round(float(weighted_score / total_rows), 2)

def load_summary_history() -> pd.DataFrame:
    """Load and combine all historical trust-summary files."""

    history_path = QUALITY_RESULTS_PATH / "history"

    if not history_path.exists():
        return pd.DataFrame()

    history_files = sorted(
        history_path.glob("summary_*.csv")
    )

    if not history_files:
        return pd.DataFrame()

    frames = [
        pd.read_csv(file_path)
        for file_path in history_files
    ]

    history = pd.concat(
        frames,
        ignore_index=True,
    )

    if "run_timestamp" in history.columns:
        history["run_timestamp"] = pd.to_datetime(
            history["run_timestamp"],
            errors="coerce",
        )

    return history


def build_platform_history(
    summary_history: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate one platform score for every quality run."""

    if summary_history.empty:
        return pd.DataFrame()

    rows: list[dict] = []

    for run_id, run_data in summary_history.groupby("run_id"):
        total_rows = run_data["rows_checked"].sum()

        if total_rows <= 0:
            platform_score = 0.0
        else:
            platform_score = (
                run_data["trust_score"]
                * run_data["rows_checked"]
            ).sum() / total_rows

        rows.append(
            {
                "run_id": run_id,
                "run_timestamp": run_data[
                    "run_timestamp"
                ].iloc[0],
                "platform_trust_score": round(
                    float(platform_score),
                    2,
                ),
                "rows_checked": int(total_rows),
                "issues_detected": int(
                    run_data["issues_detected"].sum()
                ),
                "critical_issues": int(
                    run_data["critical_issues"].sum()
                ),
            }
        )

    result = pd.DataFrame(rows)

    return result.sort_values("run_timestamp")