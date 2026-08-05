# HealthFlow – Healthcare Data Trust Platform

HealthFlow is a healthcare data quality and governance platform built to demonstrate how healthcare organizations can monitor, validate, and trust their data.

The project combines synthetic healthcare data with public healthcare datasets to simulate a real-world data quality platform. It performs automated quality validation, calculates trust scores, tracks pipeline executions, and provides dashboards for monitoring data health across multiple datasets.

Although HealthFlow is a portfolio project, it was designed using concepts commonly found in enterprise healthcare data engineering and data governance solutions.

---

## Live Demo

https://healthflow-data-trust-platform-kwkfypzkt4qibaueasxrel.streamlit.app/

---

## GitHub Repository

https://github.com/rahulbyrapuneni/healthflow-data-trust-platform

---

## Features

- Executive dashboard with enterprise trust score
- Automated healthcare data quality validation
- Dataset-level trust scoring
- Historical trust trend monitoring
- Quality issue explorer
- Pipeline execution history
- Audit logging
- Data lineage visualization
- Data dictionary
- Healthcare data source inventory
- CMS Hospital dataset integration
- ClinicalTrials.gov dataset integration
- DuckDB analytics backend
- Automated unit testing

---

## Technology Stack

### Languages

- Python
- SQL

### Frameworks & Libraries

- Streamlit
- Pandas
- DuckDB
- Requests
- Faker
- Pytest

### Data Sources

- Synthetic Healthcare Data
- CMS Hospital Data
- ClinicalTrials.gov

---

## Project Architecture

```
Healthcare Data Sources
│
├── Synthetic Healthcare Data
├── CMS Hospital Data
└── ClinicalTrials.gov
        │
        ▼
Data Validation Engine
        │
        ▼
DuckDB Analytics Store
        │
        ▼
HealthFlow Dashboard
```

---

## Application Pages

### Executive Dashboard

Provides a high-level view of platform health, including:

- Platform Trust Score
- Records Evaluated
- Quality Exceptions
- Critical Exceptions
- Dataset monitoring
- Priority recommendations

---

### Trust Trends

Tracks historical platform performance across pipeline executions and displays:

- Trust score trends
- Quality issue trends
- Dataset history

---

### Quality Issue Explorer

Allows users to review validation failures by:

- Dataset
- Severity
- Source system
- Validation rule

---

### Data Sources

Displays the current status of connected healthcare data sources, including record counts, refresh timestamps, and connection status.

---

### Rule Catalog

Lists every validation rule used by the quality engine together with its severity and business purpose.

---

### Pipeline Runs

Maintains a history of quality validation executions, including:

- Pipeline run history
- Trust scores
- Dataset statistics
- Run details

---

### Audit Logs

Captures important platform events to support governance and operational monitoring.

---

### Data Lineage

Illustrates how healthcare data moves through the platform from ingestion to quality validation and reporting.

---

### Data Dictionary

Documents datasets and business definitions used throughout the platform.

---

## Running the Project

Clone the repository

```bash
git clone https://github.com/rahulbyrapuneni/healthflow-data-trust-platform.git
```

Navigate into the project

```bash
cd healthflow-data-trust-platform
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run src/frontend/app.py
```

---

## Running Tests

```bash
pytest
```

---

## Screenshots

### Executive Dashboard

![Dashboard](Screenshots/Developed%20Version%20-%20Dashboard.png)

---

### Trust Trends

![Trust Trends](Screenshots/Developed%20Version%20-%20Trust%20Trends.png)

---

### Quality Issue Explorer

![Issue Explorer](Screenshots/Developed%20Version%20-%20Quality%20issue%20explorer.png)

---

## Future Enhancements

HealthFlow was intentionally built as a portfolio project with room for future enhancements.

Possible next steps include:

- Scheduled data ingestion
- Incremental change detection
- Additional healthcare data sources
- FHIR integration
- Email notifications for critical quality issues
- AI-assisted data quality analysis
- PostgreSQL backend
- Role-based access control

---

## About

I built HealthFlow to strengthen my understanding of healthcare data engineering, data governance, and data quality management while working with healthcare datasets.

The project brings together concepts such as ETL, data validation, trust scoring, audit logging, data lineage, and operational monitoring into a single platform.

While simplified for demonstration purposes, the overall design reflects many of the principles used in enterprise healthcare analytics environments.