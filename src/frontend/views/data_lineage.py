from __future__ import annotations

import streamlit as st


def render_data_lineage() -> None:
    """Render the HealthFlow data lineage."""

    st.title("Data Lineage")

    st.caption(
        "Visualization represents how healthcare data moves through the "
        "HealthFlow platform."
    )

    st.divider()

    st.markdown(
    """
```text
                External Healthcare Sources
                        │
        ┌───────────────┴───────────────┐
        │                               │
        ▼                               ▼
     CMS API                  Local CSV Simulator
        │                               │
        └───────────────┬───────────────┘
                        ▼
                Data Ingestion Layer
                        │
                        ▼
          Data Quality Validation Engine
                        │
          ┌─────────────┴─────────────┐
          ▼                           ▼
     Quality Issues             Dataset Summary
          │                           │
          └─────────────┬─────────────┘
                        ▼
              DuckDB Analytics Store
                        │
        ┌───────────────┼────────────────┐
        ▼               ▼                ▼
    Dashboard       Trust Trends    Issue Explorer
        │               │                │
        └───────────────┼────────────────┘
                        ▼
               Executive Reporting
    """
    )

    
    st.divider()

    st.subheader("Platform Components")

    lineage = {
        "External Sources": [
            "CMS API",
            "Healthcare Simulator",
        ],
        "Ingestion": [
            "API Clients",
            "CSV Loader",
        ],
        "Validation": [
            "Quality Rules",
            "Business Rules",
            "Issue Enrichment",
        ],
        "Storage": [
            "DuckDB",
            "History Tables",
            "Quality Issues",
        ],
        "Presentation": [
            "Dashboard",
            "Trust Trends",
            "Rule Catalog",
            "Pipeline Runs",
            "Audit Logs",
        ],
    }

    for section, items in lineage.items():
        with st.expander(section, expanded=True):
            for item in items:
                st.write(f"• {item}")