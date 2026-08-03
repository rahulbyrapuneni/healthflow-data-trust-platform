from __future__ import annotations

import streamlit as st

from src.frontend.data_loader import (
    load_issue_filter_options,
    query_quality_issues,
)


def render_issues() -> None:
    """Render the DuckDB-backed quality issue explorer."""

    st.title("Quality Issue Explorer")

    st.caption(
        "Investigate healthcare data-quality exceptions "
        "using filters executed directly in DuckDB."
    )

    options = load_issue_filter_options()

    filter_1, filter_2, filter_3 = st.columns(3)

    with filter_1:
        selected_dataset = st.selectbox(
            "Dataset",
            ["All", *options["datasets"]],
        )

    with filter_2:
        selected_severity = st.selectbox(
            "Severity",
            ["All", *options["severities"]],
        )

    with filter_3:
        selected_source = st.selectbox(
            "Source system",
            ["All", *options["source_systems"]],
        )

    search_text = st.text_input(
        "Search issues",
        placeholder=(
            "Search by record ID, rule, message, "
            "or recommendation"
        ),
    )

    filtered_issues = query_quality_issues(
        dataset=(
            None
            if selected_dataset == "All"
            else selected_dataset
        ),
        severity=(
            None
            if selected_severity == "All"
            else selected_severity
        ),
        source_system=(
            None
            if selected_source == "All"
            else selected_source
        ),
        search_text=search_text,
    )

    st.metric(
        "Matching Exceptions",
        f"{len(filtered_issues):,}",
    )

    if filtered_issues.empty:
        st.info(
            "No quality issues match the selected filters."
        )
        return

    display_columns = [
        "dataset",
        "record_id",
        "field",
        "rule",
        "severity",
        "category",
        "source_system",
        "message",
        "business_impact",
        "recommendation",
    ]

    st.dataframe(
        filtered_issues[display_columns],
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        label="Download filtered exceptions",
        data=filtered_issues.to_csv(index=False),
        file_name="healthflow_quality_exceptions.csv",
        mime="text/csv",
    )