# Skytrax Analytics Platform

This repository contains the end-to-end data engineering and analytics infrastructure for processing, transforming, and visualizing global aviation passenger reviews. The system is built on a containerized **Modern Data Stack (MDS)** architecture designed for scalable execution, robust orchestration, and enterprise-grade reporting.

---

## 1. Project Context & Business Value

![Executive BI Dashboard Preview](assets/dashboard_preview.png)


### 1.1. The Dataset
The core dataset consists of over **215,000 verified passenger reviews** scraped from Skytrax. The data captures comprehensive customer feedback across multiple dimensions:
- **Demographics & Trip Info:** Airline, Aircraft Type, Seat Type, Route, Date Flown.
- **Quantitative Ratings (1-5 stars):** Seat Comfort, Cabin Staff Service, Food & Beverages, Inflight Entertainment, Ground Service, Wifi & Connectivity, Value for Money.
- **Qualitative Metrics:** Recommended (Boolean), Verified Review (Boolean).

### 1.2. Business Questions
This analytical platform was built to answer high-impact business questions for airline executives and strategy directors:
1. **Key Drivers of Loyalty:** Which specific service attributes (e.g., Wifi vs. Cabin Staff) mathematically drive the highest probability of a passenger recommending the airline?
2. **Post-COVID Service Degradation:** How has the wave of post-pandemic cost-cutting impacted specific service domains like Food & Beverages across the industry?
3. **Competitor Benchmarking:** How do Tier-1 airlines (e.g., Emirates, Qatar Airways, Singapore Airlines) benchmark against each other across the 7 core service pillars?

### 1.3. Problem Solving Approach
To move beyond ad-hoc scripts and fragmented CSV analysis, we engineered a scalable data platform:
- **Centralized OLAP Storage:** Utilized **DuckDB** as a high-performance, embedded analytical database.
- **Dimensional Modeling:** Implemented a Star Schema (Fact and Dimension tables) using **dbt (data build tool)** to ensure data quality and standardized metrics.
- **Software-Defined Orchestration:** Replaced manual cron jobs with **Dagster** to orchestrate the entire ELT pipeline, tracking data lineage and handling failures gracefully.
- **Dual-Layer BI:** 
  - **Apache Superset:** For data analysts to perform ad-hoc slices and self-serve exploration.
  - **Streamlit:** For C-level executives to consume curated, real-time insights via an interactive dashboard.

---

## 2. Architecture & Data Flow

![MDS Architecture Diagram](assets/architecture_diagram.png)


The pipeline follows a standard **E-L-T (Extract, Load, Transform)** paradigm:

1. **Extraction & Loading (Scripts):** Raw parquet/csv data is ingested and loaded into the `raw` schema of the DuckDB warehouse (`skytrax_warehouse.duckdb`).
2. **Transformation (dbt):** 
   - **Staging (`stg_*.sql`):** Cleans raw data, casts data types, and standardizes column names.
   - **Marts (`dim_*.sql`, `fact_*.sql`):** Builds the dimensional Star Schema optimized for BI querying.
3. **Orchestration (Dagster):** Dagster defines the dbt models as software-defined assets, orchestrating the build process and ensuring dependencies are respected.
4. **Serving (Superset & Streamlit):** Both BI applications connect directly to the DuckDB warehouse using read-only connections to render visualizations.

---

## 3. Directory Tree

```text
.
├── .github/
│   └── workflows/           # CI/CD pipeline definitions (GitHub Actions)
├── data/                    # Local data storage 
│   ├── raw/                 # Raw datasets prior to ingestion
│   └── warehouse/           # DuckDB database files (skytrax_warehouse.duckdb)
├── dbt_project/             # Data transformation layer
│   ├── models/
│   │   ├── staging/         # Base views mapping to raw tables
│   │   └── marts/           # Final dimensional models (facts & dimensions)
│   ├── dbt_project.yml      # dbt configuration
│   └── profiles.yml         # dbt connection profiles to DuckDB
├── orchestration/           # Dagster configuration and assets
│   ├── assets.py            # Software-defined assets wrapping dbt models
│   ├── workspace.yaml       # Dagster workspace definition
│   ├── Dockerfile           # Custom image for Dagster + dbt + DuckDB
│   └── requirements.txt
├── reports/                 # Static management reports
│   └── aviation_executive_report.md
├── scripts/                 # Standalone ETL utilities
│   ├── extract_load.py      # Ingests raw data to DuckDB
│   └── build_marts.py       # Helper script to create a lightweight DB extract
├── src/
│   └── apps/
│       └── streamlit/       # Streamlit executive dashboard source code
│           ├── app.py
│           ├── Dockerfile
│           └── requirements.txt
├── superset/                # Apache Superset configuration
│   ├── Dockerfile           # Extends Superset to include duckdb-engine
│   └── superset_config.py   # Feature flags and DB URI configuration
├── tests/                   # Automated test suites
│   ├── integration/         # Tests for database connectivity and ETL outputs
│   └── unit/                # Unit tests for application logic
├── docker-compose.yml       # Local infrastructure orchestration
├── Makefile                 # Standardized CLI entry points
└── README.md                # Project documentation
```

---

## 4. Local Development & Deployment

### Prerequisites
- Docker & Docker Compose
- `make` utility

### Initialize the Platform
Spin up the entire containerized stack in detached mode:
```bash
make up
# OR (if 'make' is not installed, e.g., on Windows)
docker compose up -d
```

### Access Service Endpoints
Once the containers are healthy, you can access the following services:
- **Streamlit Dashboard:** `http://localhost:8501`
- **Apache Superset:** `http://localhost:8088` *(Default credentials: `admin` / `admin`)*
- **Dagster Webserver:** `http://localhost:3000`

### Teardown & Clean
To stop the services and clean up dangling volumes/cache:
```bash
make clean
# OR (if 'make' is not installed)
docker compose down -v
```

---

## 5. Continuous Integration (CI/CD)
Automated verification is managed via GitHub Actions. Push and Pull Request events to the `main` branch trigger:
1. Python unit testing (`pytest`).
2. Integration testing against ephemeral DuckDB instances.
3. Docker image build validation.

---
*Proprietary. All rights reserved.*
