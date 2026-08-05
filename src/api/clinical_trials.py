from __future__ import annotations

from typing import Any

import pandas as pd
import requests


BASE_URL = "https://clinicaltrials.gov/api/v2/studies"


def first_value(
    value: Any,
) -> str | None:
    """Return the first value from a list or the value itself."""

    if isinstance(value, list):
        return value[0] if value else None

    if value is None:
        return None

    return str(value)


def fetch_clinical_trials(
    condition: str = "Cancer",
    max_results: int = 100,
) -> pd.DataFrame:
    """Retrieve clinical trials from the ClinicalTrials.gov v2 API."""

    if not condition.strip():
        raise ValueError("condition cannot be empty.")

    if max_results <= 0 or max_results > 1000:
        raise ValueError(
            "max_results must be between 1 and 1000."
        )

    params = {
        "query.term": condition,
        "pageSize": max_results,
        "format": "json",
    }

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    payload = response.json()
    studies = payload.get("studies", [])

    rows: list[dict] = []

    for study in studies:
        protocol = study.get(
            "protocolSection",
            {},
        )

        identification = protocol.get(
            "identificationModule",
            {},
        )

        conditions_module = protocol.get(
            "conditionsModule",
            {},
        )

        design = protocol.get(
            "designModule",
            {},
        )

        sponsor_module = protocol.get(
            "sponsorCollaboratorsModule",
            {},
        )

        status_module = protocol.get(
            "statusModule",
            {},
        )

        phases = design.get(
            "phases",
            [],
        )

        conditions = conditions_module.get(
            "conditions",
            [],
        )

        sponsor = sponsor_module.get(
            "leadSponsor",
            {},
        )

        start_date = status_module.get(
            "startDateStruct",
            {},
        )

        completion_date = status_module.get(
            "completionDateStruct",
            {},
        )

        first_posted = status_module.get(
            "studyFirstPostDateStruct",
            {},
        )

        last_update_posted = status_module.get(
            "lastUpdatePostDateStruct",
            {},
        )

        rows.append(
            {
                "nct_id": identification.get(
                    "nctId"
                ),
                "title": identification.get(
                    "briefTitle"
                ),
                "condition": first_value(
                    conditions
                ),
                "phase": first_value(
                    phases
                ),
                "sponsor": sponsor.get(
                    "name"
                ),
                "status": status_module.get(
                    "overallStatus"
                ),
                "start_date": start_date.get(
                    "date"
                ),
                "completion_date": completion_date.get(
                    "date"
                ),
                "first_posted_date": first_posted.get(
                    "date"
                ),
                "last_update_posted_date": (
                    last_update_posted.get("date")
                ),
            }
        )

    return pd.DataFrame(rows)