from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
import streamlit as st

from src.utils.datetime_utils import format_timestamp


LOG_DIRECTORY = Path("logs")

LOG_FILES = {
    "Application": LOG_DIRECTORY / "application.log",
    "API": LOG_DIRECTORY / "api.log",
    "Quality": LOG_DIRECTORY / "quality.log",
    "Pipeline": LOG_DIRECTORY / "pipeline.log",
    "Frontend": LOG_DIRECTORY / "frontend.log",
}

LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"
    r"\s+\|\s+"
    r"(?P<level>[A-Z]+)"
    r"\s+\|\s+"
    r"(?P<logger>[^|]+)"
    r"\s+\|\s+"
    r"(?P<message>.*)$"
)


def parse_log_file(
    component: str,
    file_path: Path,
) -> list[dict]:
    """Parse one HealthFlow log file."""

    if not file_path.exists():
        return []

    rows: list[dict] = []

    with file_path.open(
        "r",
        encoding="utf-8",
        errors="replace",
    ) as log_file:
        for line in log_file:
            match = LOG_PATTERN.match(line.strip())

            if not match:
                continue

            rows.append(
                {
                    "component": component,
                    "timestamp": match.group("timestamp"),
                    "level": match.group("level").strip(),
                    "logger": match.group("logger").strip(),
                    "message": match.group("message").strip(),
                }
            )

    return rows


def load_audit_logs() -> pd.DataFrame:
    """Load all HealthFlow operational logs."""

    rows: list[dict] = []

    for component, file_path in LOG_FILES.items():
        rows.extend(
            parse_log_file(
                component=component,
                file_path=file_path,
            )
        )

    if not rows:
        return pd.DataFrame(
            columns=[
                "component",
                "timestamp",
                "level",
                "logger",
                "message",
            ]
        )

    logs = pd.DataFrame(rows)

    logs["timestamp"] = pd.to_datetime(
        logs["timestamp"],
        utc=True,
        errors="coerce",
    )

    return logs.sort_values(
        "timestamp",
        ascending=False,
    ).reset_index(drop=True)


def render_audit_logs() -> None:
    """Render HealthFlow operational audit logs."""

    st.title("Audit Logs")

    st.caption(
        "Review operational events from API ingestion, "
        "quality validation, pipeline execution, and application services."
    )

    logs = load_audit_logs()

    if logs.empty:
        st.info(
            "No application logs were found. Run the CMS ingestion "
            "or quality pipeline to generate log entries."
        )
        return

    component_1, component_2, component_3 = st.columns(3)

    with component_1:
        selected_component = st.selectbox(
            "Component",
            [
                "All",
                *sorted(
                    logs["component"]
                    .dropna()
                    .unique()
                    .tolist()
                ),
            ],
        )

    with component_2:
        selected_level = st.selectbox(
            "Log Level",
            [
                "All",
                *sorted(
                    logs["level"]
                    .dropna()
                    .unique()
                    .tolist()
                ),
            ],
        )

    with component_3:
        max_rows = st.selectbox(
            "Rows",
            [50, 100, 250, 500],
            index=1,
        )

    search_text = st.text_input(
        "Search logs",
        placeholder="Search logger or message",
    )

    filtered = logs.copy()

    if selected_component != "All":
        filtered = filtered[
            filtered["component"] == selected_component
        ]

    if selected_level != "All":
        filtered = filtered[
            filtered["level"] == selected_level
        ]

    if search_text.strip():
        search_value = search_text.strip().lower()

        filtered = filtered[
            filtered["logger"]
            .fillna("")
            .str.lower()
            .str.contains(
                search_value,
                regex=False,
            )
            |
            filtered["message"]
            .fillna("")
            .str.lower()
            .str.contains(
                search_value,
                regex=False,
            )
        ]

    filtered = filtered.head(max_rows).copy()

    filtered["timestamp"] = (
        filtered["timestamp"]
        .apply(format_timestamp)
    )

    metric_1, metric_2, metric_3 = st.columns(3)

    metric_1.metric(
        "Visible Events",
        f"{len(filtered):,}",
    )

    metric_2.metric(
        "Errors",
        f"{int((filtered['level'] == 'ERROR').sum()):,}",
    )

    metric_3.metric(
        "Warnings",
        f"{int((filtered['level'] == 'WARNING').sum()):,}",
    )

    st.divider()

    st.dataframe(
        filtered[
            [
                "timestamp",
                "component",
                "level",
                "logger",
                "message",
            ]
        ],
        use_container_width=True,
        hide_index=True,
        column_config={
            "timestamp": "Event Time",
            "component": "Component",
            "level": "Level",
            "logger": "Logger",
            "message": "Message",
        },
    )

    st.download_button(
        label="Download Audit Logs",
        data=filtered.to_csv(index=False),
        file_name="healthflow_audit_logs.csv",
        mime="text/csv",
    )