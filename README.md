# 🏥 HealthFlow

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Live-red)
![DuckDB](https://img.shields.io/badge/Database-DuckDB-orange)
![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)

## Enterprise Healthcare Data Trust Platform

HealthFlow is an enterprise-style healthcare data governance platform that ingests healthcare datasets, performs automated data quality validation, calculates trust scores, tracks historical quality metrics, and provides interactive dashboards for monitoring healthcare data reliability.

The platform demonstrates modern healthcare data engineering concepts including automated quality validation, data governance, pipeline monitoring, lineage tracking, audit logging, and analytical reporting.

---

## 🚀 Live Demo

**HealthFlow Application**

https://healthflow-data-trust-platform-kwkfypzkt4qibaueasxrel.streamlit.app/

---

## ✨ Key Features

### Executive Dashboard
- Enterprise healthcare trust score
- Dataset health monitoring
- Quality exception tracking
- Executive KPI cards

### Trust Trends
- Historical trust score monitoring
- Pipeline execution history
- Trend visualization
- Dataset-level quality history

### Issue Explorer
- Searchable quality issues
- Severity filtering
- Business impact analysis
- Recommended remediation

### Data Sources
- Connected healthcare datasets
- Source system monitoring
- Refresh status
- Data availability overview

### Rule Catalog
- Healthcare data quality rules
- Validation categories
- Rule severity
- Business rationale

### Pipeline Runs
- Historical execution monitoring
- Run-level metrics
- Dataset execution details
- Downloadable execution reports

### Audit Logs
- Operational logging
- Component-level monitoring
- Error and warning tracking
- Searchable audit history

### Data Lineage
- End-to-end healthcare data flow
- Data ingestion architecture
- Validation pipeline
- Analytics lifecycle

---

# 🏗 Platform Architecture

```
              External Healthcare Sources
                        │
        ┌───────────────┴────────────────┐
        │                                │
        ▼                                ▼
     CMS API                   Local Data Simulator
        │                                │
        └───────────────┬────────────────┘
                        ▼
               Data Ingestion Layer
                        │
                        ▼
           Healthcare Quality Validation
                        │
          ┌─────────────┴─────────────┐
          ▼                           ▼
    Quality Issues           Trust Summary
          │                           │
          └─────────────┬─────────────┘
                        ▼
               DuckDB Analytics Store
                        │
        ┌───────────────┼──────────────────────┐
        ▼               ▼                      ▼
   Dashboard      Trust Trends        Audit Logs
                        │
                        ▼
             Executive Decision Support
```

---

# 🛠 Technology Stack

| Category | Technology |
|-----------|------------|
| Language | Python |
| Dashboard | Streamlit |
| Database | DuckDB |
| API Integration | CMS Healthcare API |
| Data Processing | Pandas |
| Testing | Pytest |
| Version Control | Git & GitHub |
| Deployment | Streamlit Community Cloud |

---

# 📊 Platform Capabilities

- Enterprise Healthcare Dashboard
- Automated Data Quality Validation
- Healthcare Trust Score Calculation
- Historical Trend Monitoring
- Rule-Based Validation Engine
- Audit Logging
- Pipeline Monitoring
- Data Lineage
- Data Governance
- Interactive Analytics
- Executive Reporting

---

# 📁 Project Structure

```
healthflow-data-trust-platform/

├── data/
│   ├── analytics/
│   ├── quality_results/
│   └── source_data/
│
├── src/
│   ├── analytics/
│   ├── api/
│   ├── frontend/
│   ├── quality/
│   ├── simulator/
│   └── utils/
│
├── tests/
│
├── requirements.txt
├── streamlit_app.py
└── README.md
```

---

# ⚙ Installation

Clone the repository

```bash
git clone https://github.com/rahulbyrapuneni/healthflow-data-trust-platform.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run quality validation

```bash
python -m src.quality.run_quality_checks
```

Load the analytics database

```bash
python -m src.analytics.load_analytics_store
```

Launch the application

```bash
streamlit run streamlit_app.py
```

---

# 🧪 Testing

Execute the automated test suite

```bash
pytest
```

HealthFlow includes automated tests covering:

- Data ingestion
- Healthcare quality rules
- API integration
- Analytics layer
- Pipeline execution
- Frontend utilities
- Audit logging


---

# 🚧 Roadmap

Upcoming enhancements

- ClinicalTrials.gov integration
- openFDA integration
- AI-powered Quality Assistant
- Executive PDF reports
- Advanced analytics
- Multi-source healthcare monitoring

---

# 👨‍💻 About

HealthFlow was developed as an enterprise healthcare data governance platform to demonstrate practical data engineering, quality assurance, analytics, and governance concepts using publicly available healthcare datasets.

The project showcases an end-to-end healthcare data platform—from ingestion and validation to monitoring, reporting, and operational oversight.