from __future__ import annotations

import pandas as pd
import streamlit as st

from src.frontend.data_loader import (
    load_pipeline_run_details,
    load_pipeline_runs,
)

from src.utils.datetime_utils import (
    format_timestamp,
)


def render_pipeline_runs() -> None:
    """Render HealthFlow pipeline execution history."""

    st.title("Pipeline Runs")

    st.caption(
        "Review healthcare data validation executions, "
        "trust scores, exceptions, and dataset-level results."
    )

    runs = load_pipeline_runs()

    if runs.empty:
        st.info(
            "No pipeline history was found. Run the quality "
            "pipeline and DuckDB analytics loader first."
        )
        return

    latest = runs.iloc[0]

    total_runs = len(runs)

    successful_runs = int(
        runs["run_status"]
        .str.startswith("Completed")
        .sum()
    )

    latest_score = float(
        latest["platform_trust_score"]
    )

    latest_issues = int(
        latest["issues_detected"]
    )

    metric_1, metric_2, metric_3, metric_4 = st.columns(4)

    metric_1.metric(
        "Recorded Runs",
        f"{total_runs:,}",
    )

    metric_2.metric(
        "Completed Runs",
        f"{successful_runs:,}",
    )

    metric_3.metric(
        "Latest Trust Score",
        f"{latest_score:.2f}%",
    )

    metric_4.metric(
        "Latest Exceptions",
        f"{latest_issues:,}",
    )

    st.caption(
        "Latest execution: "
        f"{format_timestamp(latest['run_timestamp'])}"
    )

    st.divider()

    st.subheader("Execution History")

    display_runs = runs.copy()

    display_runs["run_timestamp"] = (
        display_runs["run_timestamp"]
        .apply(format_timestamp)
    )

    display_runs["short_run_id"] = (
        display_runs["run_id"]
        .astype(str)
        .str.slice(0, 8)
    )

    history_columns = [
        "short_run_id",
        "run_timestamp",
        "datasets_processed",
        "rows_checked",
        "issues_detected",
        "critical_issues",
        "platform_trust_score",
        "run_status",
    ]

    st.dataframe(
        display_runs[history_columns],
        use_container_width=True,
        hide_index=True,
        column_config={
            "short_run_id": "Run ID",
            "run_timestamp": "Run Time",
            "datasets_processed": "Datasets",
            "rows_checked": "Records Evaluated",
            "issues_detected": "Exceptions",
            "critical_issues": "Critical",
            "platform_trust_score": st.column_config.NumberColumn(
                "Trust Score",
                format="%.2f%%",
            ),
            "run_status": "Status",
        },
    )

    st.divider()

    st.subheader("Run Details")

    run_options = {
        (
            f"{format_timestamp(row['run_timestamp'])} "
            f"— {str(row['run_id'])[:8]}"
        ): str(row["run_id"])
        for _, row in runs.iterrows()
    }

    selected_label = st.selectbox(
        "Select pipeline run",
        list(run_options.keys()),
    )

    selected_run_id = run_options[
        selected_label
    ]

    selected_run = runs[
        runs["run_id"].astype(str)
        == selected_run_id
    ].iloc[0]

    detail_1, detail_2, detail_3, detail_4 = st.columns(4)

    detail_1.metric(
        "Datasets Processed",
        int(selected_run["datasets_processed"]),
    )

    detail_2.metric(
        "Records Evaluated",
        f"{int(selected_run['rows_checked']):,}",
    )

    detail_3.metric(
        "Quality Exceptions",
        f"{int(selected_run['issues_detected']):,}",
    )

    detail_4.metric(
        "Trust Score",
        (
            f"{float(selected_run['platform_trust_score']):.2f}%"
        ),
    )

    st.markdown("### Execution Information")

    information = pd.DataFrame(
        [
            {
                "Field": "Run ID",
                "Value": selected_run_id,
            },
            {
                "Field": "Run Time",
                "Value": format_timestamp(
                    selected_run["run_timestamp"]
                ),
            },
            {
                "Field": "Status",
                "Value": selected_run["run_status"],
            },
            {
                "Field": "Critical Exceptions",
                "Value": int(
                    selected_run["critical_issues"]
                ),
            },
        ]
    )

    st.dataframe(
        information,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("### Dataset Results")

    run_details = load_pipeline_run_details(
        selected_run_id
    )

    if run_details.empty:
        st.info(
            "No dataset-level information is available "
            "for this run."
        )
    else:
        st.dataframe(
            run_details,
            use_container_width=True,
            hide_index=True,
            column_config={
                "dataset": "Dataset",
                "rows_checked": "Records Evaluated",
                "issues_detected": "Exceptions",
                "critical_issues": "Critical",
                "high_issues": "High",
                "medium_issues": "Medium",
                "low_issues": "Low",
                "trust_score": st.column_config.NumberColumn(
                    "Trust Score",
                    format="%.2f%%",
                ),
                "status": "Dataset Status",
            },
        )

        st.download_button(
            label="Download Run Details",
            data=run_details.to_csv(index=False),
            file_name=(
                f"healthflow_run_"
                f"{selected_run_id}.csv"
            ),
            mime="text/csv",
        )