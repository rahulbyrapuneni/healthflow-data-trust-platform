from __future__ import annotations

import sys
from pathlib import Path
from src.frontend.views.audit_logs import render_audit_logs


PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.frontend.views.rule_catalog import render_rule_catalog

from src.frontend.views.rule_catalog import (
    render_rule_catalog,
)

import streamlit as st

from src.frontend.data_loader import (
    load_issues,
    load_summary,
    load_summary_history,
)
from src.frontend.views.pipeline_runs import (
    render_pipeline_runs,
)
from src.frontend.views.data_lineage import (
    render_data_lineage,
)
from src.frontend.views.data_dictionary import (
    render_data_dictionary,
)
from src.frontend.styles import apply_ehr_styles
from src.frontend.views.about import render_about
from src.frontend.views.dashboard import render_dashboard
from src.frontend.views.data_sources import render_data_sources
from src.frontend.views.issues import render_issues
from src.frontend.views.trends import render_trends


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
            "Run the quality pipeline and DuckDB analytics loader "
            "before starting the frontend."
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
        render_issues()

    def api_sources_page() -> None:
        st.title("API Sources")
        st.info(
            "Public CMS healthcare API connectivity will be "
            "added in an upcoming milestone."
        )

    def rule_explorer_page() -> None:
        render_rule_catalog()

    def pipeline_runs_page() -> None:
        render_pipeline_runs()

    def api_sources_page() -> None:
        render_data_sources()

    def about_page() -> None:
        render_about()

    def audit_logs_page() -> None:
        render_audit_logs()

    def data_lineage_page() -> None:
        render_data_lineage()

    def data_dictionary_page() -> None:
        render_data_dictionary()
    def main() -> None:
        render_rule_catalog()

    pages = [
    st.Page(
        dashboard_page,
        title="Dashboard",
        icon=":material/dashboard:",
        default=True,
        url_path="dashboard",
    ),
    st.Page(
        trends_page,
        title="Trust Trends",
        icon=":material/monitoring:",
        url_path="trust-trends",
    ),
    st.Page(
        issues_page,
        title="Issue Explorer",
        icon=":material/search:",
        url_path="issue-explorer",
    ),
    st.Page(
        api_sources_page,
        title="Data Sources",
        icon=":material/database:",
        url_path="data-sources",
    ),
    st.Page(
        rule_explorer_page,
        title="Rule Catalog",
        icon=":material/rule:",
        url_path="rule-catalog",
    ),
    st.Page(
        pipeline_runs_page,
        title="Pipeline Runs",
        icon=":material/history:",
        url_path="pipeline-runs",
    ),
    st.Page(
         audit_logs_page,
         title="Audit Logs",
         icon=":material/description:",
         url_path="audit-logs",
     ), 

    st.Page(
        data_lineage_page,
        title="Data Lineage",
        icon=":material/account_tree:",
        url_path="data-lineage",
    ),

    st.Page(
        data_dictionary_page,
        title="Data Dictionary",
        icon=":material/dictionary:",
        url_path="data-dictionary",
    ),
       
    st.Page(
        about_page,
        title="About",
        icon=":material/info:",
        url_path="about",
    ),
  
]

    
    navigation = st.navigation(
        pages,
        position="sidebar",
    )

    with st.sidebar:
        st.markdown("## HealthFlow")
        st.caption("Healthcare Data Trust Platform")
        st.caption("Version 0.5")

    navigation.run()


if __name__ == "__main__":
    main()