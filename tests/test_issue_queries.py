import pandas as pd

import src.frontend.data_loader as loader


def test_query_quality_issues_uses_selected_filters(
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
                    "dataset": "claims",
                    "severity": "Critical",
                }
            ]
        )

    monkeypatch.setattr(
        loader,
        "execute_query",
        fake_execute_query,
    )

    result = loader.query_quality_issues(
        dataset="claims",
        severity="Critical",
    )

    assert len(result) == 1
    assert "dataset = ?" in captured["query"]
    assert "severity = ?" in captured["query"]
    assert captured["parameters"] == [
        "claims",
        "Critical",
    ]


def test_query_quality_issues_returns_empty_when_missing(
    monkeypatch,
):
    monkeypatch.setattr(
        loader,
        "table_exists",
        lambda table_name: False,
    )

    result = loader.query_quality_issues()

    assert result.empty


def test_search_text_uses_parameterized_query(
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
        captured["parameters"] = parameters
        return pd.DataFrame()

    monkeypatch.setattr(
        loader,
        "execute_query",
        fake_execute_query,
    )

    loader.query_quality_issues(
        search_text="duplicate",
    )

    assert captured["parameters"] == [
        "%duplicate%",
        "%duplicate%",
        "%duplicate%",
        "%duplicate%",
    ]