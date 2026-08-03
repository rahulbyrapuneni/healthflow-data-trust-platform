import pandas as pd

from src.quality.platform_report import (
    build_dataset_summary,
    calculate_platform_trust_score,
)


def test_dataset_summary_contains_all_datasets():
    dataset_rows = {
        "patients": 100,
        "appointments": 200,
    }

    issues = pd.DataFrame(
        [
            {
                "dataset": "patients",
                "record_id": 1,
                "field": "mrn",
                "rule": "DUPLICATE_MRN",
                "severity": "Critical",
                "message": "Duplicate MRN.",
            }
        ]
    )

    summary = build_dataset_summary(
        dataset_rows=dataset_rows,
        all_issues=issues,
    )

    assert len(summary) == 2
    assert set(summary["dataset"]) == {
        "patients",
        "appointments",
    }


def test_dataset_without_issues_scores_100():
    dataset_rows = {
        "patients": 100,
    }

    issues = pd.DataFrame(
        columns=[
            "dataset",
            "record_id",
            "field",
            "rule",
            "severity",
            "message",
        ]
    )

    summary = build_dataset_summary(
        dataset_rows=dataset_rows,
        all_issues=issues,
    )

    assert summary.iloc[0]["trust_score"] == 100.0
    assert summary.iloc[0]["status"] == "Excellent"


def test_platform_score_is_row_weighted():
    summary = pd.DataFrame(
        [
            {
                "dataset": "patients",
                "rows_checked": 100,
                "trust_score": 100.0,
            },
            {
                "dataset": "labs",
                "rows_checked": 300,
                "trust_score": 80.0,
            },
        ]
    )

    score = calculate_platform_trust_score(summary)

    assert score == 85.0