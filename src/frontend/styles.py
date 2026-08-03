from __future__ import annotations

import streamlit as st


def apply_ehr_styles() -> None:
    """Apply the HealthFlow EHR-style visual system."""

    st.markdown(
        """
        <style>
        :root {
            --hf-navy: #17324D;
            --hf-navy-dark: #10283E;
            --hf-white: #FFFFFF;
            --hf-background: #F3F5F7;
            --hf-border: #D6DCE2;
            --hf-muted: #607080;
            --hf-text: #17324D;
        }

        /* Main application */
        .stApp {
            background-color: var(--hf-white);
            color: var(--hf-text);
        }

        .main .block-container {
            max-width: 1450px;
            padding-top: 1.25rem;
            padding-bottom: 3rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: var(--hf-navy);
            border-right: 1px solid var(--hf-navy-dark);
        }

        [data-testid="stSidebar"] * {
            color: var(--hf-white);
        }

        [data-testid="stSidebar"] hr {
            border-color: rgba(255, 255, 255, 0.18);
        }

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            color: rgba(255, 255, 255, 0.76);
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: var(--hf-white);
            border-bottom: none;
        }

        /* Sidebar navigation */
        [data-testid="stSidebarNav"] ul {
            gap: 0.1rem;
        }

        [data-testid="stSidebarNav"] li {
            margin-bottom: 0.1rem;
        }

        [data-testid="stSidebarNav"] a {
            border-left: 4px solid transparent;
            border-radius: 0;
            margin: 0;
            padding-top: 0.55rem;
            padding-bottom: 0.55rem;
            padding-left: 0.8rem;
            transition:
                background-color 0.15s ease,
                border-left-color 0.15s ease;
        }

        [data-testid="stSidebarNav"] a:hover {
            background-color: rgba(255, 255, 255, 0.06);
            border-left-color: rgba(255, 255, 255, 0.35);
        }

        /* Active navigation item */
        [data-testid="stSidebarNav"] a[aria-current="page"] {
            background-color: rgba(255, 255, 255, 0.09);
            border-left: 4px solid var(--hf-white);
            border-radius: 0;
        }

        /* Active page text */
        [data-testid="stSidebarNav"] a[aria-current="page"] span {
            color: var(--hf-white) !important;
            font-weight: 600;
        }

        /* Active page icon */
        [data-testid="stSidebarNav"] a[aria-current="page"] svg,
        [data-testid="stSidebarNav"] a[aria-current="page"] svg path {
            fill: var(--hf-white) !important;
            color: var(--hf-white) !important;
        }

        /* Inactive navigation icons and text */
        [data-testid="stSidebarNav"] a span {
            color: var(--hf-white) !important;
        }

        [data-testid="stSidebarNav"] a svg,
        [data-testid="stSidebarNav"] a svg path {
            fill: var(--hf-white) !important;
            color: var(--hf-white) !important;
        }

        /* Main headings */
        h1,
        h2,
        h3 {
            color: var(--hf-navy);
            letter-spacing: -0.01em;
        }

        h1 {
            font-size: 1.75rem;
            font-weight: 600;
            padding-bottom: 0.45rem;
            border-bottom: 2px solid var(--hf-navy);
        }

        h2 {
            font-size: 1.2rem;
            font-weight: 600;
        }

        h3 {
            font-size: 1rem;
            font-weight: 600;
        }

        /* Paragraph and caption text */
        p,
        label,
        div,
        span {
            font-family:
                Arial,
                Helvetica,
                sans-serif;
        }

        [data-testid="stCaptionContainer"] {
            color: var(--hf-muted);
        }

        /* KPI metric panels */
        [data-testid="stMetric"] {
            background-color: var(--hf-white);
            border: 1px solid var(--hf-border);
            border-top: 3px solid var(--hf-navy);
            border-radius: 2px;
            padding: 1rem 1.1rem;
            min-height: 112px;
            box-shadow: none;
        }

        [data-testid="stMetricLabel"] {
            color: var(--hf-muted);
            font-size: 0.82rem;
            font-weight: 500;
        }

        [data-testid="stMetricValue"] {
            color: var(--hf-navy);
            font-weight: 600;
        }

        [data-testid="stMetricDelta"] {
            color: var(--hf-navy);
        }

        /* Tables */
        [data-testid="stDataFrame"] {
            border: 1px solid var(--hf-border);
            border-radius: 2px;
            overflow: hidden;
        }

        [data-testid="stDataFrame"] * {
            font-size: 0.92rem;
        }

        /* Form controls */
        [data-baseweb="select"] > div {
            border-radius: 2px;
            border-color: var(--hf-border);
        }

        input,
        textarea {
            border-radius: 2px !important;
            border-color: var(--hf-border) !important;
        }

        /* Buttons */
        .stButton > button,
        .stDownloadButton > button {
            background-color: var(--hf-navy);
            color: var(--hf-white);
            border: 1px solid var(--hf-navy);
            border-radius: 2px;
            font-weight: 500;
            box-shadow: none;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover {
            background-color: var(--hf-navy-dark);
            color: var(--hf-white);
            border-color: var(--hf-navy-dark);
        }

        .stButton > button:focus,
        .stDownloadButton > button:focus {
            box-shadow: 0 0 0 2px rgba(23, 50, 77, 0.22);
        }

        /* Alerts */
        [data-testid="stAlert"] {
            border-radius: 2px;
            border-left: 4px solid var(--hf-navy);
            background-color: var(--hf-background);
            color: var(--hf-navy);
        }

        /* Dividers */
        hr {
            border-color: var(--hf-border);
        }

        /* Sidebar collapse button */
        [data-testid="stSidebarCollapseButton"] button {
            color: var(--hf-white);
        }

        [data-testid="stSidebarCollapseButton"] svg,
        [data-testid="stSidebarCollapseButton"] svg path {
            fill: var(--hf-white) !important;
            color: var(--hf-white) !important;
        }

        /* Remove Streamlit chrome */
        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        [data-testid="stDecoration"] {
            display: none;
        }

        /* Responsive layout */
        @media (max-width: 900px) {
            .main .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }

            [data-testid="stMetric"] {
                min-height: auto;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )