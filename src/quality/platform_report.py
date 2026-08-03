from __future__ import annotations

import pandas as pd

from src.quality.quality_report import (
    calculate_trust_score,
    get_trust_status,
)


def build_dataset_summary(
    dataset_rows: dict[str, int],
    all_issues: pd.DataFrame,
) -> pd.DataFrame:
    """Create one trust-score summary row per dataset."""

    summaries: list[dict] = []

    for dataset_name, row_count in dataset_rows.items():
        dataset_issues = all_issues[
            all_issues["dataset"] == dataset_name
        ]

        trust_score = calculate_trust_score(
            row_count=row_count,
            issues=dataset_issues,
        )

        summaries.append(
            {
                "dataset": dataset_name,
                "rows_checked": row_count,
                "issues_detected": len(dataset_issues),
                "critical_issues": int(
                    (
                        dataset_issues["severity"]
                        == "Critical"
                    ).sum()
                ),
                "high_issues": int(
                    (
                        dataset_issues["severity"]
                        == "High"
                    ).sum()
                ),
                "medium_issues": int(
                    (
                        dataset_issues["severity"]
                        == "Medium"
                    ).sum()
                ),
                "low_issues": int(
                    (
                        dataset_issues["severity"]
                        == "Low"
                    ).sum()
                ),
                "trust_score": trust_score,
                "status": get_trust_status(trust_score),
            }
        )

    return pd.DataFrame(summaries)


def calculate_platform_trust_score(
    dataset_summary: pd.DataFrame,
) -> float:
    """
    Calculate a row-weighted trust score across all datasets.
    """

    if dataset_summary.empty:
        return 0.0

    total_rows = dataset_summary["rows_checked"].sum()

    if total_rows <= 0:
        return 0.0

    weighted_scores = (
        dataset_summary["trust_score"]
        * dataset_summary["rows_checked"]
    )

    platform_score = weighted_scores.sum() / total_rows

    return round(float(platform_score), 2)


def print_platform_report(
    dataset_summary: pd.DataFrame,
) -> None:
    """Print an overall platform trust report."""

    platform_score = calculate_platform_trust_score(
        dataset_summary
    )

    platform_status = get_trust_status(platform_score)

    total_rows = int(
        dataset_summary["rows_checked"].sum()
    )

    total_issues = int(
        dataset_summary["issues_detected"].sum()
    )

    print()
    print("=" * 72)
    print("HEALTHFLOW PLATFORM DATA TRUST REPORT")
    print("=" * 72)
    print(f"Total rows checked: {total_rows:,}")
    print(f"Total issues detected: {total_issues:,}")
    print(f"Overall trust score: {platform_score}%")
    print(f"Overall status: {platform_status}")
    print()

    display_columns = [
        "dataset",
        "rows_checked",
        "issues_detected",
        "critical_issues",
        "high_issues",
        "medium_issues",
        "low_issues",
        "trust_score",
        "status",
    ]

    print(
        dataset_summary[
            display_columns
        ].to_string(index=False)
    )

    print("=" * 72)