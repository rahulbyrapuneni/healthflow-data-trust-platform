# HealthFlow Data Trust Platform

An open-source healthcare data quality platform that answers one practical question:

> Can we trust the data used for healthcare reporting, operations, and research?

The platform generates synthetic healthcare data, detects quality problems, scores data trustworthiness, and explains issues in a reproducible local environment.

## Core problem

Healthcare organizations combine data from registration, scheduling, laboratory, billing, insurance, and clinical systems. The resulting datasets often contain duplicate patients, missing demographics, invalid clinical codes, orphan records, inconsistent dates, and conflicting values.

These problems reduce confidence in dashboards, delay reporting, and force analysts and researchers to spend substantial time manually validating data.

## Initial scope

Version 1 focuses on five datasets:

- Patients
- Appointments
- Laboratory results
- Claims
- Insurance coverage

The first quality rules detect:

- Duplicate patient records
- Missing dates of birth
- Invalid gender values
- Future birth dates
- Orphan appointments and laboratory records
- Appointments before birth
- Negative claim amounts
- Paid amounts greater than billed amounts
- Missing insurance coverage
- Impossible laboratory values

## Technology principles

- Free and open-source
- Runs locally
- No cloud subscription
- No proprietary healthcare access
- No paid APIs
- Synthetic data only
- Reproducible setup
- Every tool must solve a real problem

## Initial stack

- Python
- Pandas
- Faker
- DuckDB
- Pytest
- Git and GitHub
- Streamlit later, when the quality engine is stable
- PySpark later, only when the dataset and transformations justify it

## Run the simulator

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Generate data:

```bash
python src/simulator/generate_data.py
```

The generated CSV files will appear in `data/raw/`.

## Project roadmap

1. Sprint 0: problem definition, architecture, quality rules, repository setup
2. Sprint 1: synthetic healthcare data generator
3. Sprint 2: data profiling and validation engine
4. Sprint 3: trust score and issue prioritization
5. Sprint 4: DuckDB analytics layer
6. Sprint 5: monitoring dashboard
7. Sprint 6: optional local AI explanations
8. Sprint 7: tests, Docker, CI/CD, documentation, and final demo

## Portfolio outcome

This project demonstrates healthcare data engineering, data quality, governance, analytics engineering, SQL, Python, testing, architecture, and technical communication without relying on restricted systems or paid services.
