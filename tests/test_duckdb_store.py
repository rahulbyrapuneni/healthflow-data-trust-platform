from pathlib import Path

import pandas as pd

import src.analytics.duckdb_store as store


def test_replace_and_read_table(
    tmp_path: Path,
    monkeypatch,
):
    database_path = tmp_path / "test.duckdb"

    monkeypatch.setattr(
        store,
        "DATABASE_PATH",
        database_path,
    )

    dataframe = pd.DataFrame(
        [
            {"id": 1, "name": "First"},
            {"id": 2, "name": "Second"},
        ]
    )

    store.replace_table(
        table_name="example_table",
        dataframe=dataframe,
    )

    result = store.read_table("example_table")

    assert len(result) == 2
    assert result["name"].tolist() == [
        "First",
        "Second",
    ]


def test_table_exists(
    tmp_path: Path,
    monkeypatch,
):
    database_path = tmp_path / "test.duckdb"

    monkeypatch.setattr(
        store,
        "DATABASE_PATH",
        database_path,
    )

    store.replace_table(
        table_name="example_table",
        dataframe=pd.DataFrame([{"id": 1}]),
    )

    assert store.table_exists("example_table") is True
    assert store.table_exists("missing_table") is False


def test_invalid_table_name_is_rejected():
    dataframe = pd.DataFrame([{"id": 1}])

    try:
        store.replace_table(
            table_name="bad table",
            dataframe=dataframe,
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Expected invalid table name to fail."
        )