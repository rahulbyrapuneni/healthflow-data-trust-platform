import pandas as pd

from src.quality.issue_enrichment import enrich_issues


def test_known_rule_receives_business_metadata():
    issues = pd.DataFrame(
        [
            {
                "dataset": "patients",
                "record_id": 1,
                "field": "mrn",
                "rule": "DUPLICATE_MRN",
                "severity": "Critical",
                "message": "Duplicate MRN detected.",
            }
        ]
    )

    enriched = enrich_issues(issues)

    assert enriched.iloc[0]["category"] == "Uniqueness"
    assert (
        enriched.iloc[0]["source_system"]
        == "Registration System"
    )
    assert enriched.iloc[0]["recommendation"]


def test_unknown_rule_receives_default_metadata():
    issues = pd.DataFrame(
        [
            {
                "dataset": "patients",
                "record_id": 1,
                "field": "example",
                "rule": "UNKNOWN_RULE",
                "severity": "Low",
                "message": "Unknown issue.",
            }
        ]
    )

    enriched = enrich_issues(issues)

    assert enriched.iloc[0]["category"] == "Data Quality"
    assert enriched.iloc[0]["source_system"] == "Unknown"


def test_empty_issue_dataframe_remains_empty():
    issues = pd.DataFrame()

    enriched = enrich_issues(issues)

    assert enriched.empty