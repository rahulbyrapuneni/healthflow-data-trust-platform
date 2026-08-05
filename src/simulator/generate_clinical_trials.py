from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.api.clinical_trials import (
    fetch_clinical_trials,
)
from src.pipelines.clinical_trials_changes import (
    append_change_history,
    detect_clinical_trial_changes,
)


OUTPUT_DIRECTORY = Path(
    "data/source_data"
)

OUTPUT_FILE = (
    OUTPUT_DIRECTORY / "clinical_trials.csv"
)


def main() -> None:
    """Download trials and detect source changes."""

    previous = pd.DataFrame()

    if OUTPUT_FILE.exists():
        previous = pd.read_csv(
            OUTPUT_FILE,
            dtype=str,
        )

    latest = fetch_clinical_trials(
        condition="Cancer",
        max_results=100,
    )

    changes, metrics = (
        detect_clinical_trial_changes(
            previous=previous,
            latest=latest,
        )
    )

    append_change_history(changes)

    OUTPUT_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    latest.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print("=" * 60)
    print("CLINICALTRIALS.GOV CHANGE-AWARE INGESTION")
    print("=" * 60)
    print(f"Records downloaded: {len(latest):,}")
    print(f"New trials: {metrics['new']:,}")
    print(f"Updated trials: {metrics['updated']:,}")
    print(
        f"Unchanged trials: "
        f"{metrics['unchanged']:,}"
    )
    print(f"Current file: {OUTPUT_FILE}")
    print(
        "Change history: "
        "data/history/clinical_trials_changes.csv"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()