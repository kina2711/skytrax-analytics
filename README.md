# Skytrax Analytics Platform

This repository contains the data engineering and analytics infrastructure for processing and visualizing global aviation passenger reviews. The system is built on a containerized Modern Data Stack architecture, designed for scalable extraction, transformation, orchestration, and reporting.

## Architecture

The platform integrates the following core systems:
- **DuckDB**: In-process SQL OLAP database managing the data warehouse.
- **dbt**: Data transformation, modeling, and testing layer.
- **Dagster**: Software-defined asset orchestrator governing the ELT pipelines.
- **Apache Superset**: Business intelligence and ad-hoc data exploration.
- **Streamlit**: Application layer for the executive metrics dashboard.
- **Docker**: Containerization runtime managing local microservices.
- **GitHub Actions**: Automated Continuous Integration (CI) workflows.

## Directory Layout

```text
.
├── .github/workflows/           # CI/CD pipeline definitions
├── data/                        # Persistent storage (raw ingestion and warehouse)
├── dbt_project/                 # dbt models, macros, and test configurations
├── orchestration/               # Dagster workspaces, assets, and daemon configurations
├── scripts/                     # Utility scripts for standalone operations
├── src/apps/streamlit/          # Streamlit dashboard application source
├── superset/                    # Superset custom Dockerfile and initialization
└── tests/                       # Automated unit and integration test suites
```

## Local Development

### Prerequisites
- Docker & Docker Compose
- `make` utility

### Deployment
1. **Initialize the stack**:
   ```bash
   make up
   ```
2. **Service Endpoints**:
   - Streamlit Application: `http://localhost:8501`
   - Apache Superset: `http://localhost:8088` (Default credentials: `admin` / `admin`)
   - Dagster Webserver: `http://localhost:3000`

### Testing
Execute the automated test suite locally:
```bash
make test
```

## Continuous Integration
Automated verification is managed via GitHub Actions. Push and Pull Request events to the `main` branch trigger:
1. Python unit testing (`pytest`).
2. Integration testing against ephemeral DuckDB instances.
3. Docker image build validation.

## License
Proprietary. All rights reserved.
