from __future__ import annotations

import pandas as pd

from src.quality.rule_metadata import get_rule_metadata


def enrich_issues(issues: pd.DataFrame) -> pd.DataFrame:
    """Add category, source, impact, and recommendation to issues."""

    if issues.empty:
        return issues.copy()

    enriched = issues.copy()

    metadata = enriched["rule"].apply(get_rule_metadata)

    enriched["category"] = metadata.apply(
        lambda value: value["category"]
    )

    enriched["source_system"] = metadata.apply(
        lambda value: value["source_system"]
    )

    enriched["business_impact"] = metadata.apply(
        lambda value: value["business_impact"]
    )

    enriched["recommendation"] = metadata.apply(
        lambda value: value["recommendation"]
    )

    return enriched