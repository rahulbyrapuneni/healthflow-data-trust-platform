from __future__ import annotations

import pandas as pd
import streamlit as st

from src.frontend.data_loader import calculate_platform_score


def render_dashboard(
    summary: pd.DataFrame,
    issues: pd.DataFrame,
) -> None:
    """Render the executive dashboard."""

    st.title("Enterprise Data Trust Overview")

    st.caption(
       "Enterprise data-quality monitoring for clinical, "
    "operational, and financial healthcare domains."
    )

    platform_score = calculate_platform_score(summary)

    total_rows = int(summary["rows_checked"].sum())
    total_issues = int(summary["issues_detected"].sum())
    critical_issues = int(summary["critical_issues"].sum())

    if platform_score >= 98:
        trust_status = "Excellent"
    elif platform_score >= 95:
        trust_status = "Good"
    elif platform_score >= 90:
        trust_status = "Fair"
    elif platform_score >= 80:
        trust_status = "Poor"
    else:
        trust_status = "Critical"

    metric_1, metric_2, metric_3, metric_4 = st.columns(4)

    metric_1.metric(
        "Platform Trust Score",
        f"{platform_score}%",
    )

    metric_2.metric(
        "Records Evaluated",
        f"{total_rows:,}",
    )

    metric_3.metric(
        "Quality Exceptions",
        f"{total_issues:,}",
    )

    metric_4.metric(
        "Critical Exceptions",
        f"{critical_issues:,}",
    )

    if "run_timestamp" in summary.columns:
        last_run = summary["run_timestamp"].iloc[0]

        st.info(
            f"Platform Status: {trust_status} | "
            f"Last Run: {last_run}"
        )
    else:
        st.info(
            f"Platform Status: {trust_status}"
        )
    
    st.divider()

    st.subheader("Dataset Health")
   

    left_column, right_column = st.columns([2, 1])

    with left_column:
        st.subheader("Dataset Health")

        dataset_health = summary[
            [
                "dataset",
                "rows_checked",
                "issues_detected",
                "trust_score",
                "status",
            ]
        ].copy()

        dataset_health["dataset"] = (
            dataset_health["dataset"]
            .str.replace("_", " ")
            .str.title()
        )

        st.dataframe(
            dataset_health,
            use_container_width=True,
            hide_index=True,
        )

    with right_column:
        st.subheader("Issues by Severity")

        severity_counts = (
            issues["severity"]
            .value_counts()
            .rename_axis("severity")
            .reset_index(name="issue_count")
        )

        st.dataframe(
            severity_counts,
            use_container_width=True,
            hide_index=True,
        )

    st.divider()

    st.subheader("Top Quality Problems")

    top_rules = (
        issues.groupby(
            [
                "rule",
                "severity",
                "source_system",
            ],
            dropna=False,
        )
        .size()
        .reset_index(name="issue_count")
        .sort_values(
            "issue_count",
            ascending=False,
        )
        .head(10)
    )

    st.dataframe(
        top_rules,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    st.subheader("Priority Recommendations")

    priority_issues = issues[
        issues["severity"].isin(
            ["Critical", "High"]
        )
    ].copy()

    recommendation_summary = (
        priority_issues[
            [
                "rule",
                "source_system",
                "business_impact",
                "recommendation",
            ]
        ]
        .drop_duplicates()
        .head(10)
    )

    st.dataframe(
        recommendation_summary,
        use_container_width=True,
        hide_index=True,
    )