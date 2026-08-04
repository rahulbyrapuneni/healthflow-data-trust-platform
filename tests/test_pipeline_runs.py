import pandas as pd

import src.frontend.data_loader as loader
from src.utils.datetime_utils import format_timestamp


def test_pipeline_runs_returns_empty_when_table_missing(
    monkeypatch,
):
    monkeypatch.setattr(
        loader,
        "table_exists",
        lambda table_name: False,
    )

    result = loader.load_pipeline_runs()

    assert result.empty


def test_pipeline_run_details_uses_selected_run_id(
    monkeypatch,
):
    captured: dict = {}

    monkeypatch.setattr(
        loader,
        "table_exists",
        lambda table_name: True,
    )

    def fake_execute_query(
        query: str,
        parameters: list | None = None,
    ) -> pd.DataFrame:
        captured["query"] = query
        captured["parameters"] = parameters

        return pd.DataFrame(
            [
                {
                    "dataset": "patients",
                    "rows_checked": 100,
                }
            ]
        )

    monkeypatch.setattr(
        loader,
        "execute_query",
        fake_execute_query,
    )

    result = loader.load_pipeline_run_details(
        "run-123"
    )

    assert len(result) == 1
    assert "WHERE run_id = ?" in captured["query"]
    assert captured["parameters"] == ["run-123"]


def test_timestamp_is_formatted_for_display():
    result = format_timestamp(
        "2026-08-04T18:15:00+00:00"
    )

    assert result == "Aug 04, 2026 • 02:15 PM EDT"


def test_invalid_timestamp_returns_not_available():
    result = format_timestamp(
        "invalid timestamp"
    )

    assert result == "Not available"