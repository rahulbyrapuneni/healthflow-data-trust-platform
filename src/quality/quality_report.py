from __future__ import annotations

import pandas as pd


SEVERITY_WEIGHTS = {
    "Critical": 5,
    "High": 3,
    "Medium": 2,
    "Low": 1,
}


def calculate_trust_score(
    row_count: int,
    issues: pd.DataFrame,
) -> float:
    """Calculate a trust score between 0 and 100."""

    if row_count <= 0:
        return 0.0

    if issues.empty:
        return 100.0

    weighted_issue_count = (
        issues["severity"]
        .map(SEVERITY_WEIGHTS)
        .fillna(0)
        .sum()
    )

    maximum_penalty = row_count * 5
    penalty_percentage = (
        weighted_issue_count / maximum_penalty
    ) * 100

    score = 100 - penalty_percentage

    return round(max(score, 0), 2)


def get_trust_status(score: float) -> str:
    """Convert a numeric trust score into a status."""

    if score >= 98:
        return "Excellent"
    if score >= 95:
        return "Good"
    if score >= 90:
        return "Fair"
    if score >= 80:
        return "Poor"

    return "Critical"


def print_quality_report(
    dataset_name: str,
    row_count: int,
    issues: pd.DataFrame,
) -> None:
    """Print a readable data-quality summary."""

    score = calculate_trust_score(row_count, issues)
    status = get_trust_status(score)

    print("=" * 60)
    print("HEALTHFLOW DATA TRUST REPORT")
    print("=" * 60)
    print(f"Dataset: {dataset_name}")
    print(f"Rows checked: {row_count}")
    print(f"Issues detected: {len(issues)}")
    print()

    if issues.empty:
        print("No data-quality issues were detected.")
        print()
    else:
        print("Issues by rule:")
        print(issues["rule"].value_counts().to_string())
        print()

        print("Issues by severity:")
        print(issues["severity"].value_counts().to_string())
        print()

    print(f"Trust score: {score}%")
    print(f"Status: {status}")
    print("=" * 60)