from __future__ import annotations
from typing import Any
from pathlib import Path

import duckdb
import pandas as pd


DATABASE_PATH = Path("data/healthflow.duckdb")


def get_connection() -> duckdb.DuckDBPyConnection:
    """Open the local HealthFlow DuckDB database."""

    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    return duckdb.connect(str(DATABASE_PATH))


def replace_table(
    table_name: str,
    dataframe: pd.DataFrame,
) -> None:
    """Replace one DuckDB table with a DataFrame."""

    if not table_name.replace("_", "").isalnum():
        raise ValueError("Invalid table name.")

    connection = get_connection()

    try:
        connection.register(
            "incoming_dataframe",
            dataframe,
        )

        connection.execute(
            f"""
            CREATE OR REPLACE TABLE {table_name} AS
            SELECT *
            FROM incoming_dataframe
            """
        )
    finally:
        connection.close()


def read_table(table_name: str) -> pd.DataFrame:
    """Read an entire DuckDB table into a DataFrame."""

    if not table_name.replace("_", "").isalnum():
        raise ValueError("Invalid table name.")

    connection = get_connection()

    try:
        return connection.execute(
            f"SELECT * FROM {table_name}"
        ).fetchdf()
    finally:
        connection.close()


def table_exists(table_name: str) -> bool:
    """Return whether a DuckDB table exists."""

    connection = get_connection()

    try:
        result = connection.execute(
            """
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_name = ?
            """,
            [table_name],
        ).fetchone()

        return bool(result and result[0] > 0)
    finally:
        connection.close()

def execute_query(
    query: str,
    parameters: list[Any] | None = None,
) -> pd.DataFrame:
    """Execute a parameterized SQL query and return a DataFrame."""

    connection = get_connection()

    try:
        return connection.execute(
            query,
            parameters or [],
        ).fetchdf()
    finally:
        connection.close()