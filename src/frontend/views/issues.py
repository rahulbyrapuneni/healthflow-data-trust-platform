from __future__ import annotations

import pandas as pd
import streamlit as st


def render_issues(issues: pd.DataFrame) -> None:
    """Render the interactive quality issue explorer."""

    st.title("Quality Issue Explorer")

    st.caption(
        "Filter, review, and export detected healthcare "
        "data-quality issues."
    )

    filter_1, filter_2, filter_3 = st.columns(3)

    dataset_options = [
        "All",
        *sorted(
            issues["dataset"]
            .dropna()
            .unique()
            .tolist()
        ),
    ]

    severity_options = [
        "All",
        *sorted(
            issues["severity"]
            .dropna()
            .unique()
            .tolist()
        ),
    ]

    source_options = [
        "All",
        *sorted(
            issues["source_system"]
            .dropna()
            .unique()
            .tolist()
        ),
    ]

    with filter_1:
        selected_dataset = st.selectbox(
            "Dataset",
            dataset_options,
        )

    with filter_2:
        selected_severity = st.selectbox(
            "Severity",
            severity_options,
        )

    with filter_3:
        selected_source = st.selectbox(
            "Source system",
            source_options,
        )

    filtered = issues.copy()

    if selected_dataset != "All":
        filtered = filtered[
            filtered["dataset"]
            == selected_dataset
        ]

    if selected_severity != "All":
        filtered = filtered[
            filtered["severity"]
            == selected_severity
        ]

    if selected_source != "All":
        filtered = filtered[
            filtered["source_system"]
            == selected_source
        ]

    st.metric(
        "Matching Issues",
        f"{len(filtered):,}",
    )

    display_columns = [
        "dataset",
        "record_id",
        "field",
        "rule",
        "severity",
        "source_system",
        "message",
        "business_impact",
        "recommendation",
    ]

    st.dataframe(
        filtered[display_columns],
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        label="Download filtered issues",
        data=filtered.to_csv(index=False),
        file_name="healthflow_quality_issues.csv",
        mime="text/csv",
    )