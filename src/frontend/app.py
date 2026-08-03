from __future__ import annotations
from src.frontend.views.data_sources import (
    render_data_sources,
)

import streamlit as st

from src.frontend.data_loader import (
    load_issues,
    load_summary,
)
from src.frontend.styles import apply_ehr_styles

from src.frontend.data_loader import (
    load_issues,
    load_summary,
    load_summary_history,
)

from src.frontend.views.trends import render_trends
from src.frontend.views.about import render_about
from src.frontend.views.dashboard import render_dashboard
from src.frontend.views.issues import render_issues


def main() -> None:
    st.set_page_config(
        page_title="HealthFlow",
        page_icon="H",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    apply_ehr_styles()

    try:
        summary = load_summary()
        issues = load_issues()
        summary_history = load_summary_history()
    except FileNotFoundError as error:
        st.error(str(error))
        st.info(
            "Run the ingestion and quality pipelines before "
            "starting the frontend."
        )
        st.stop()

    def dashboard_page() -> None:
        render_dashboard(
            summary=summary,
            issues=issues,
        )

    def trends_page() -> None:
        render_trends(summary_history)

    def issues_page() -> None:
        render_issues(issues)

    def api_sources_page() -> None:
        st.title("API Sources")
        st.info(
            "Public CMS healthcare API connectivity will be "
            "added in an upcoming milestone."
        )

    def rule_explorer_page() -> None:
        st.title("Rule Explorer")
        st.info(
            "Data-quality rule documentation and configuration "
            "will be added in an upcoming milestone."
        )

    def pipeline_runs_page() -> None:
        st.title("Pipeline Runs")
        st.info(
            "Pipeline run history and operational logs will be "
            "added in an upcoming milestone."
        )

    def api_sources_page() -> None:
        render_data_sources()

    def about_page() -> None:
        render_about()

    pages = [
        st.Page(
            dashboard_page,
            title="Dashboard",
            icon=":material/dashboard:",
            default=True,
        ),
        st.Page(
            trends_page,
            title="Trust Trends",
            icon=":material/monitoring:",
        ),
        st.Page(
            issues_page,
            title="Issue Explorer",
            icon=":material/search:",
        ),
        st.Page(
            api_sources_page,
            title="API Sources",
            icon=":material/cloud_sync:",
        ),
        st.Page(
            rule_explorer_page,
            title="Rule Explorer",
            icon=":material/rule:",
        ),
        st.Page(
            pipeline_runs_page,
            title="Pipeline Runs",
            icon=":material/history:",
        ),

        st.Page(
            api_sources_page,
            title="Data Sources",
            icon=":material/database:",
        ),

        st.Page(
            about_page,
            title="About",
            icon=":material/info:",
        ),

    ]

    navigation = st.navigation(
        pages,
        position="sidebar",
    )

    with st.sidebar:
        st.markdown("## HealthFlow")
        st.caption("Healthcare Data Trust Platform")
        st.divider()
        st.caption("DATA GOVERNANCE MODULE")
        st.divider()
        st.caption("Version 0.2")

    navigation.run()


if __name__ == "__main__":
    main()