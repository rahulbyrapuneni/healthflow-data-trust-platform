import pandas as pd

import src.frontend.data_loader as loader
from src.frontend.views.data_dictionary import (
    format_table_name,
)


def test_format_table_name():
    assert (
        format_table_name("dataset_trust_summary")
        == "Dataset Trust Summary"
    )


def test_dictionary_columns_use_selected_table(
    monkeypatch,
):
    captured: dict = {}

    def fake_execute_query(
        query: str,
        parameters: list | None = None,
    ) -> pd.DataFrame:
        captured["parameters"] = parameters

        return pd.DataFrame(
            [
                {
                    "column_name": "dataset",
                    "data_type": "VARCHAR",
                    "is_nullable": "YES",
                    "ordinal_position": 1,
                }
            ]
        )

    monkeypatch.setattr(
        loader,
        "execute_query",
        fake_execute_query,
    )

    result = loader.load_data_dictionary_columns(
        "quality_issues"
    )

    assert len(result) == 1
    assert captured["parameters"] == [
        "quality_issues"
    ]


def test_empty_table_name_returns_empty():
    result = loader.load_data_dictionary_columns("")

    assert result.empty