from __future__ import annotations

import streamlit as st

from src.frontend.data_loader import (
    load_data_dictionary_columns,
    load_data_dictionary_tables,
    load_table_profile,
)


TABLE_DESCRIPTIONS = {
    "quality_issues": (
        "Detected healthcare data-quality exceptions, "
        "including severity, impact, and remediation guidance."
    ),
    "dataset_trust_summary": (
        "Latest dataset-level trust scores and exception counts."
    ),
    "dataset_trust_history": (
        "Historical trust metrics for each quality pipeline run."
    ),
    "cms_hospitals": (
        "Public CMS hospital general-information records."
    ),
}


def format_table_name(table_name: str) -> str:
    """Convert a database table name into a display label."""

    return table_name.replace("_", " ").title()


def render_data_dictionary() -> None:
    """Render the HealthFlow Data Dictionary."""

    st.title("Data Dictionary")

    st.caption(
        "Review healthcare datasets, table structures, "
        "column definitions, and analytics metadata."
    )

    tables = load_data_dictionary_tables()

    if tables.empty:
        st.info(
            "No DuckDB tables were found. Run the analytics "
            "loader before opening the Data Dictionary."
        )
        return

    table_names = tables["table_name"].tolist()

    selected_table = st.selectbox(
        "Dataset",
        table_names,
        format_func=format_table_name,
    )

    profile = load_table_profile(selected_table).iloc[0]
    columns = load_data_dictionary_columns(selected_table)

    metric_1, metric_2, metric_3 = st.columns(3)

    metric_1.metric(
        "Records",
        f"{int(profile['record_count']):,}",
    )

    metric_2.metric(
        "Columns",
        f"{int(profile['column_count']):,}",
    )

    metric_3.metric(
        "Storage Layer",
        "DuckDB",
    )

    st.divider()

    st.subheader("Dataset Description")

    st.write(
        TABLE_DESCRIPTIONS.get(
            selected_table,
            "HealthFlow analytics dataset.",
        )
    )

    st.divider()

    st.subheader("Column Definitions")

    display_columns = columns.copy()

    display_columns["is_nullable"] = (
        display_columns["is_nullable"]
        .map(
            {
                "YES": "Yes",
                "NO": "No",
            }
        )
        .fillna(display_columns["is_nullable"])
    )

    st.dataframe(
        display_columns[
            [
                "ordinal_position",
                "column_name",
                "data_type",
                "is_nullable",
            ]
        ],
        use_container_width=True,
        hide_index=True,
        column_config={
            "ordinal_position": "Position",
            "column_name": "Column",
            "data_type": "Data Type",
            "is_nullable": "Nullable",
        },
    )

    st.download_button(
        label="Download Column Definitions",
        data=display_columns.to_csv(index=False),
        file_name=(
            f"healthflow_{selected_table}_dictionary.csv"
        ),
        mime="text/csv",
    )