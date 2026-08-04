from __future__ import annotations

import pandas as pd
import streamlit as st

from src.frontend.data_loader import (
    load_rule_catalog,
)


SEVERITY_ORDER = {
    "Critical": 1,
    "High": 2,
    "Medium": 3,
    "Low": 4,
}


def filter_rule_catalog(
    catalog: pd.DataFrame,
    dataset: str | None = None,
    severity: str | None = None,
    category: str | None = None,
    search_text: str | None = None,
) -> pd.DataFrame:
    """Filter the Rule Catalog using user selections."""

    filtered = catalog.copy()

    if dataset:
        filtered = filtered[
            filtered["dataset"] == dataset
        ]

    if severity:
        filtered = filtered[
            filtered["severity"] == severity
        ]

    if category:
        filtered = filtered[
            filtered["category"] == category
        ]

    if search_text and search_text.strip():
        search_value = search_text.strip().lower()

        searchable_columns = [
            "rule",
            "dataset",
            "category",
            "source_system",
            "business_impact",
            "recommendation",
        ]

        search_mask = pd.Series(
            False,
            index=filtered.index,
        )

        for column in searchable_columns:
            search_mask = (
                search_mask
                | filtered[column]
                .fillna("")
                .astype(str)
                .str.lower()
                .str.contains(
                    search_value,
                    regex=False,
                )
            )

        filtered = filtered[search_mask]

    filtered = filtered.copy()

    filtered["severity_order"] = (
        filtered["severity"]
        .map(SEVERITY_ORDER)
        .fillna(99)
    )

    return (
        filtered
        .sort_values(
            [
                "severity_order",
                "dataset",
                "rule",
            ]
        )
        .drop(columns=["severity_order"])
        .reset_index(drop=True)
    )


def render_rule_catalog() -> None:
    """Render the healthcare data-quality Rule Catalog."""

    st.title("Rule Catalog")

    st.caption(
        "Review the validation rules used to assess healthcare "
        "data quality, risk, and recommended remediation."
    )

    catalog = load_rule_catalog()

    if catalog.empty:
        st.info(
            "No executed quality rules were found. Run the "
            "quality pipeline and DuckDB analytics loader first."
        )
        return

    total_rules = int(catalog["rule"].nunique())
    critical_rules = int(
        catalog.loc[
            catalog["severity"] == "Critical",
            "rule",
        ].nunique()
    )
    datasets_covered = int(
        catalog["dataset"].nunique()
    )
    categories_covered = int(
        catalog["category"].nunique()
    )

    metric_1, metric_2, metric_3, metric_4 = st.columns(4)

    metric_1.metric(
        "Documented Rules",
        total_rules,
    )

    metric_2.metric(
        "Critical Rules",
        critical_rules,
    )

    metric_3.metric(
        "Datasets Covered",
        datasets_covered,
    )

    metric_4.metric(
        "Quality Categories",
        categories_covered,
    )

    st.divider()

    filter_1, filter_2, filter_3 = st.columns(3)

    dataset_options = [
        "All",
        *sorted(
            catalog["dataset"]
            .dropna()
            .unique()
            .tolist()
        ),
    ]

    severity_options = [
        "All",
        *sorted(
            catalog["severity"]
            .dropna()
            .unique()
            .tolist()
        ),
    ]

    category_options = [
        "All",
        *sorted(
            catalog["category"]
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
        selected_category = st.selectbox(
            "Category",
            category_options,
        )

    search_text = st.text_input(
        "Search rules",
        placeholder=(
            "Search by rule, category, source system, "
            "impact, or recommendation"
        ),
    )

    filtered_catalog = filter_rule_catalog(
        catalog=catalog,
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
        category=(
            None
            if selected_category == "All"
            else selected_category
        ),
        search_text=search_text,
    )

    st.write(
        f"Showing **{len(filtered_catalog):,}** "
        "rule records"
    )

    if filtered_catalog.empty:
        st.info(
            "No rules match the selected filters."
        )
        return

    summary_columns = [
        "rule",
        "dataset",
        "severity",
        "category",
        "source_system",
        "issue_count",
    ]

    st.dataframe(
        filtered_catalog[summary_columns],
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    st.subheader("Rule Details")

    rule_labels = filtered_catalog.apply(
        lambda row: (
            f"{row['rule']} — "
            f"{str(row['dataset']).replace('_', ' ').title()}"
        ),
        axis=1,
    ).tolist()

    selected_label = st.selectbox(
        "Select a rule",
        rule_labels,
    )

    selected_position = rule_labels.index(
        selected_label
    )

    selected_rule = filtered_catalog.iloc[
        selected_position
    ]

    detail_1, detail_2, detail_3 = st.columns(3)

    detail_1.metric(
        "Severity",
        selected_rule["severity"],
    )

    detail_2.metric(
        "Category",
        selected_rule["category"],
    )

    detail_3.metric(
        "Detected Exceptions",
        int(selected_rule["issue_count"]),
    )

    st.markdown("### Rule")

    st.code(
        str(selected_rule["rule"]),
        language=None,
    )

    st.markdown("### Source System")

    st.write(selected_rule["source_system"])

    st.markdown("### Business Impact")

    st.write(selected_rule["business_impact"])

    st.markdown("### Recommended Remediation")

    st.write(selected_rule["recommendation"])

    st.download_button(
        label="Download Rule Catalog",
        data=filtered_catalog.to_csv(index=False),
        file_name="healthflow_rule_catalog.csv",
        mime="text/csv",
    )