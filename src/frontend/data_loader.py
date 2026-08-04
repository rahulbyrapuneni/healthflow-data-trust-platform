from __future__ import annotations

import pandas as pd

from src.analytics.duckdb_store import (
    execute_query,
    read_table,
    table_exists,
)

from src.quality.rule_metadata import get_rule_metadata

def load_summary() -> pd.DataFrame:
    """Load the latest dataset trust summary from DuckDB."""

    if not table_exists("dataset_trust_summary"):
        raise FileNotFoundError(
            "DuckDB table 'dataset_trust_summary' was not found. "
            "Run the analytics loader first."
        )

    return read_table("dataset_trust_summary")


def load_issues() -> pd.DataFrame:
    """Load quality issues from DuckDB."""

    if not table_exists("quality_issues"):
        raise FileNotFoundError(
            "DuckDB table 'quality_issues' was not found. "
            "Run the analytics loader first."
        )

    return read_table("quality_issues")


def load_summary_history() -> pd.DataFrame:
    """Load dataset trust history from DuckDB."""

    if not table_exists("dataset_trust_history"):
        return pd.DataFrame()

    history = read_table("dataset_trust_history")

    if "run_timestamp" in history.columns:
        history["run_timestamp"] = pd.to_datetime(
            history["run_timestamp"],
            errors="coerce",
        )

    return history


def load_cms_hospitals() -> pd.DataFrame:
    """Load CMS hospital records from DuckDB."""

    if not table_exists("cms_hospitals"):
        return pd.DataFrame()

    return read_table("cms_hospitals")


def calculate_platform_score(summary: pd.DataFrame) -> float:
    """Calculate a row-weighted platform trust score."""

    total_rows = summary["rows_checked"].sum()

    if total_rows <= 0:
        return 0.0

    weighted_score = (
        summary["trust_score"]
        * summary["rows_checked"]
    ).sum()

    return round(
        float(weighted_score / total_rows),
        2,
    )


def build_platform_history(
    summary_history: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate one platform score for each quality run."""

    if summary_history.empty:
        return pd.DataFrame()

    rows: list[dict] = []

    for run_id, run_data in summary_history.groupby(
        "run_id"
    ):
        total_rows = run_data["rows_checked"].sum()

        if total_rows <= 0:
            platform_score = 0.0
        else:
            platform_score = (
                run_data["trust_score"]
                * run_data["rows_checked"]
            ).sum() / total_rows

        rows.append(
            {
                "run_id": run_id,
                "run_timestamp": run_data[
                    "run_timestamp"
                ].iloc[0],
                "platform_trust_score": round(
                    float(platform_score),
                    2,
                ),
                "rows_checked": int(total_rows),
                "issues_detected": int(
                    run_data[
                        "issues_detected"
                    ].sum()
                ),
                "critical_issues": int(
                    run_data[
                        "critical_issues"
                    ].sum()
                ),
            }
        )

    return (
        pd.DataFrame(rows)
        .sort_values("run_timestamp")
        .reset_index(drop=True)
    )

def load_issue_filter_options() -> dict[str, list[str]]:
    """Load distinct Issue Explorer filter values."""

    if not table_exists("quality_issues"):
        return {
            "datasets": [],
            "severities": [],
            "source_systems": [],
        }

    datasets = execute_query(
        """
        SELECT DISTINCT dataset
        FROM quality_issues
        WHERE dataset IS NOT NULL
        ORDER BY dataset
        """
    )

    severities = execute_query(
        """
        SELECT DISTINCT severity
        FROM quality_issues
        WHERE severity IS NOT NULL
        ORDER BY severity
        """
    )

    source_systems = execute_query(
        """
        SELECT DISTINCT source_system
        FROM quality_issues
        WHERE source_system IS NOT NULL
        ORDER BY source_system
        """
    )

    return {
        "datasets": datasets["dataset"].tolist(),
        "severities": severities["severity"].tolist(),
        "source_systems": source_systems[
            "source_system"
        ].tolist(),
    }


def query_quality_issues(
    dataset: str | None = None,
    severity: str | None = None,
    source_system: str | None = None,
    search_text: str | None = None,
) -> pd.DataFrame:
    """Query quality issues using optional filters."""

    if not table_exists("quality_issues"):
        return pd.DataFrame()

    conditions: list[str] = []
    parameters: list[str] = []

    if dataset:
        conditions.append("dataset = ?")
        parameters.append(dataset)

    if severity:
        conditions.append("severity = ?")
        parameters.append(severity)

    if source_system:
        conditions.append("source_system = ?")
        parameters.append(source_system)

    if search_text and search_text.strip():
        conditions.append(
            """
            (
                LOWER(CAST(record_id AS VARCHAR)) LIKE ?
                OR LOWER(rule) LIKE ?
                OR LOWER(message) LIKE ?
                OR LOWER(recommendation) LIKE ?
            )
            """
        )

        search_value = f"%{search_text.strip().lower()}%"

        parameters.extend(
            [
                search_value,
                search_value,
                search_value,
                search_value,
            ]
        )

    where_clause = ""

    if conditions:
        where_clause = (
            "WHERE " + " AND ".join(conditions)
        )

    query = f"""
        SELECT
            dataset,
            record_id,
            field,
            rule,
            severity,
            category,
            source_system,
            message,
            business_impact,
            recommendation,
            run_id,
            run_timestamp
        FROM quality_issues
        {where_clause}
        ORDER BY
            CASE severity
                WHEN 'Critical' THEN 1
                WHEN 'High' THEN 2
                WHEN 'Medium' THEN 3
                WHEN 'Low' THEN 4
                ELSE 5
            END,
            dataset,
            rule
    """

    return execute_query(
        query=query,
        parameters=parameters,
    )

def load_rule_catalog() -> pd.DataFrame:
    """Build a catalog of quality rules executed by HealthFlow."""

    columns = [
        "rule",
        "dataset",
        "severity",
        "category",
        "source_system",
        "business_impact",
        "recommendation",
        "issue_count",
    ]

    if not table_exists("quality_issues"):
        return pd.DataFrame(columns=columns)

    rules = execute_query(
        """
        SELECT
            rule,
            dataset,
            severity,
            COUNT(*) AS issue_count
        FROM quality_issues
        WHERE rule IS NOT NULL
        GROUP BY
            rule,
            dataset,
            severity
        ORDER BY
            CASE severity
                WHEN 'Critical' THEN 1
                WHEN 'High' THEN 2
                WHEN 'Medium' THEN 3
                WHEN 'Low' THEN 4
                ELSE 5
            END,
            dataset,
            rule
        """
    )

    if rules.empty:
        return pd.DataFrame(columns=columns)

    metadata = rules["rule"].apply(get_rule_metadata)

    rules["category"] = metadata.apply(
        lambda value: value.get(
            "category",
            "Uncategorized",
        )
    )

    rules["source_system"] = metadata.apply(
        lambda value: value.get(
            "source_system",
            "Not specified",
        )
    )

    rules["business_impact"] = metadata.apply(
        lambda value: value.get(
            "business_impact",
            "Not documented",
        )
    )

    rules["recommendation"] = metadata.apply(
        lambda value: value.get(
            "recommendation",
            "Not documented",
        )
    )

    return rules[columns]


def load_rule_filter_options() -> dict[str, list[str]]:
    """Return distinct Rule Catalog filter options."""

    catalog = load_rule_catalog()

    if catalog.empty:
        return {
            "datasets": [],
            "severities": [],
            "categories": [],
        }

    return {
        "datasets": sorted(
            catalog["dataset"]
            .dropna()
            .unique()
            .tolist()
        ),
        "severities": sorted(
            catalog["severity"]
            .dropna()
            .unique()
            .tolist()
        ),
        "categories": sorted(
            catalog["category"]
            .dropna()
            .unique()
            .tolist()
        ),
    }

def load_pipeline_runs() -> pd.DataFrame:
    """Return one summarized record for each quality pipeline run."""

    columns = [
        "run_id",
        "run_timestamp",
        "datasets_processed",
        "rows_checked",
        "issues_detected",
        "critical_issues",
        "platform_trust_score",
        "run_status",
    ]

    if not table_exists("dataset_trust_history"):
        return pd.DataFrame(columns=columns)

    runs = execute_query(
        """
        SELECT
            run_id,
            MIN(run_timestamp) AS run_timestamp,
            COUNT(DISTINCT dataset) AS datasets_processed,
            SUM(rows_checked) AS rows_checked,
            SUM(issues_detected) AS issues_detected,
            SUM(critical_issues) AS critical_issues,

            ROUND(
                SUM(trust_score * rows_checked)
                / NULLIF(SUM(rows_checked), 0),
                2
            ) AS platform_trust_score,

            CASE
                WHEN SUM(critical_issues) > 0
                    THEN 'Completed with critical issues'
                ELSE 'Completed'
            END AS run_status

        FROM dataset_trust_history

        GROUP BY run_id

        ORDER BY MIN(run_timestamp) DESC
        """
    )

    if "run_timestamp" in runs.columns:
        runs["run_timestamp"] = pd.to_datetime(
            runs["run_timestamp"],
            errors="coerce",
        )

    return runs[columns]

def load_pipeline_run_details(
    run_id: str,
) -> pd.DataFrame:
    """Return dataset-level details for one pipeline run."""

    if not run_id:
        return pd.DataFrame()

    if not table_exists("dataset_trust_history"):
        return pd.DataFrame()

    return execute_query(
        """
        SELECT
            dataset,
            rows_checked,
            issues_detected,
            critical_issues,
            high_issues,
            medium_issues,
            low_issues,
            trust_score,
            status
        FROM dataset_trust_history
        WHERE run_id = ?
        ORDER BY dataset
        """,
        [run_id],
    )

def load_data_dictionary_tables() -> pd.DataFrame:
    """Return available HealthFlow analytics tables."""

    return execute_query(
        """
        SELECT
            table_name
        FROM information_schema.tables
        WHERE table_schema = 'main'
        ORDER BY table_name
        """
    )


def load_data_dictionary_columns(
    table_name: str,
) -> pd.DataFrame:
    """Return column metadata for one DuckDB table."""

    if not table_name:
        return pd.DataFrame()

    return execute_query(
        """
        SELECT
            column_name,
            data_type,
            is_nullable,
            ordinal_position
        FROM information_schema.columns
        WHERE table_schema = 'main'
          AND table_name = ?
        ORDER BY ordinal_position
        """,
        [table_name],
    )


def load_table_profile(
    table_name: str,
) -> pd.DataFrame:
    """Return basic record and column counts for a table."""

    allowed_tables = load_data_dictionary_tables()

    if table_name not in allowed_tables["table_name"].tolist():
        raise ValueError("Unknown analytics table.")

    return execute_query(
        f"""
        SELECT
            COUNT(*) AS record_count,
            {len(load_data_dictionary_columns(table_name))}
                AS column_count
        FROM {table_name}
        """
    )