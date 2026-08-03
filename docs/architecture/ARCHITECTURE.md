# Initial Architecture

```text
Synthetic Healthcare Data Generator
                |
                v
           Raw CSV Files
                |
                v
        Data Profiling Layer
                |
                v
       Rule Validation Engine
                |
                v
       Quality Results Store
                |
        +-------+--------+
        |                |
        v                v
 DuckDB Analytics   Streamlit UI
        |
        v
 Remediation Reports
```

## Why this architecture

The first version deliberately avoids Spark, Airflow, Kafka, and other distributed tools. The initial data volume does not justify them. Starting with Python, Pandas, and DuckDB makes the project easy to run, test, and explain.

Distributed processing can be introduced later when a measured bottleneck or scale requirement exists.
