import pandas as pd

from src.frontend.views.rule_catalog import (
    filter_rule_catalog,
)


def sample_catalog() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "rule": "DUPLICATE_MRN",
                "dataset": "patients",
                "severity": "Critical",
                "category": "Uniqueness",
                "source_system": "Registration",
                "business_impact": (
                    "Duplicate patient identities."
                ),
                "recommendation": (
                    "Merge duplicate patient records."
                ),
                "issue_count": 2,
            },
            {
                "rule": "INVALID_ZIP_CODE",
                "dataset": "cms_hospitals",
                "severity": "Medium",
                "category": "Validity",
                "source_system": "CMS",
                "business_impact": (
                    "Geographic reporting may be inaccurate."
                ),
                "recommendation": (
                    "Validate ZIP code format."
                ),
                "issue_count": 1,
            },
        ]
    )


def test_catalog_filters_by_dataset():
    result = filter_rule_catalog(
        catalog=sample_catalog(),
        dataset="patients",
    )

    assert len(result) == 1
    assert result.iloc[0]["rule"] == "DUPLICATE_MRN"


def test_catalog_filters_by_severity():
    result = filter_rule_catalog(
        catalog=sample_catalog(),
        severity="Medium",
    )

    assert len(result) == 1
    assert result.iloc[0]["rule"] == "INVALID_ZIP_CODE"


def test_catalog_searches_business_impact():
    result = filter_rule_catalog(
        catalog=sample_catalog(),
        search_text="geographic",
    )

    assert len(result) == 1
    assert result.iloc[0]["dataset"] == "cms_hospitals"


def test_catalog_returns_empty_for_no_match():
    result = filter_rule_catalog(
        catalog=sample_catalog(),
        search_text="nonexistent rule",
    )

    assert result.empty