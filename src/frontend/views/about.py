import streamlit as st


def render_about() -> None:
    """Render project information."""

    st.title("About HealthFlow")

    st.markdown(
        """
        HealthFlow is an open-source healthcare data trust platform
        designed to identify, prioritize, and explain data-quality
        problems before healthcare information is used for reporting,
        operations, or research.

        ### Current capabilities

        - Synthetic healthcare data generation
        - CSV ingestion and schema validation
        - Patient, appointment, laboratory, claims, and insurance checks
        - Referential-integrity validation
        - Clinical plausibility checks
        - Financial consistency checks
        - Dataset-level trust scores
        - Platform-wide trust scoring
        - Business impact and remediation recommendations
        - Automated testing
        - Structured application logging

        ### Technology stack

        Python, Pandas, Streamlit, Pytest, Git, GitHub, and open-source
        healthcare data tools.

        The platform uses synthetic data for controlled testing and will
        also support public healthcare APIs such as CMS, openFDA, and
        ClinicalTrials.gov.
        """
    )