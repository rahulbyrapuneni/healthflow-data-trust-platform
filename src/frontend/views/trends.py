from __future__ import annotations

import pandas as pd
import streamlit as st

from src.frontend.data_loader import build_platform_history
from src.utils.datetime_utils import format_timestamp


def render_trends(
    summary_history: pd.DataFrame,
) -> None:
    """Render historical trust-score monitoring."""

    st.title("Trust Trends")

    st.caption(
        "Monitor platform and dataset-level data quality "
        "across repeated pipeline executions."
    )

    if summary_history.empty:
        st.info(
            "No historical quality runs were found. "
            "Run the quality engine multiple times to create history."
        )
        return

    platform_history = build_platform_history(
        summary_history
    )

    latest = platform_history.iloc[-1]
    previous = (
        platform_history.iloc[-2]
        if len(platform_history) > 1
        else None
    )

    score_change = None

    if previous is not None:
        score_change = round(
            latest["platform_trust_score"]
            - previous["platform_trust_score"],
            2,
        )

    column_1, column_2, column_3, column_4 = st.columns(4)

    column_1.metric(
        "Latest Trust Score",
        f"{latest['platform_trust_score']}%",
    )

    column_2.metric(
        "Recorded Runs",
        f"{len(platform_history):,}",
    )

    column_3.metric(
        "Latest Issues",
        f"{int(latest['issues_detected']):,}",
    )

    column_4.metric(
        "Score Change",
        (
            f"{score_change:+.2f}%"
            if score_change is not None
            else "Not available"
        ),
    )

    st.caption(
        "Latest quality run: "
        f"{format_timestamp(latest['run_timestamp'])}"
    )

    st.divider()

    st.subheader("Platform Trust Score History")

    score_chart = platform_history[
        [
            "run_timestamp",
            "platform_trust_score",
        ]
    ].set_index("run_timestamp")

    st.line_chart(
        score_chart,
        y="platform_trust_score",
        height=320,
    )

    st.divider()

    st.subheader("Quality Exceptions by Run")

    issue_chart = platform_history[
        [
            "run_timestamp",
            "issues_detected",
        ]
    ].set_index("run_timestamp")

    st.line_chart(
        issue_chart,
        y="issues_detected",
        height=280,
    )

    st.divider()

    st.subheader("Dataset-Level History")

    dataset_options = sorted(
        summary_history["dataset"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_dataset = st.selectbox(
        "Dataset",
        dataset_options,
    )

    dataset_history = summary_history[
        summary_history["dataset"]
        == selected_dataset
    ].sort_values("run_timestamp")

    dataset_chart = dataset_history[
        [
            "run_timestamp",
            "trust_score",
        ]
    ].set_index("run_timestamp")

    st.line_chart(
        dataset_chart,
        y="trust_score",
        height=300,
    )

    display_columns = [
        "run_timestamp",
        "rows_checked",
        "issues_detected",
        "critical_issues",
        "high_issues",
        "medium_issues",
        "low_issues",
        "trust_score",
        "status",
    ]

    display_history = dataset_history[
        display_columns
    ].copy()

    display_history["run_timestamp"] = (
        display_history["run_timestamp"]
        .apply(format_timestamp)
    )

    st.dataframe(
        display_history,
        use_container_width=True,
        hide_index=True,
    )