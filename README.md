# Skytrax Analytics Platform

An end-to-end Modern Data Stack (MDS) implementation for analyzing global aviation passenger reviews. This repository contains data extraction, transformation, orchestration, and visualization components architected to FAANG-style engineering standards.

## Architecture Overview

The platform leverages the following core components:
- **DuckDB**: Embedded analytical database serving as the core data warehouse.
- **dbt**: Data transformation and modeling layer.
- **Dagster**: Software-defined asset orchestrator for ELT workflows.
- **Apache Superset**: Enterprise-grade business intelligence platform.
- **Streamlit**: Lightweight, interactive executive dashboard.
- **Docker & Docker Compose**: Containerization and local infrastructure orchestration.
- **GitHub Actions**: Automated CI/CD pipelines.

## Project Structure

```text
.
├── .github/workflows/           # CI/CD automation
├── data/                        # Local data storage (raw and warehouse)
├── dbt_project/                 # dbt models, macros, and configuration
├── orchestration/               # Dagster definitions and workspace
├── scripts/                     # Standalone Python scripts for ingestion/export
├── src/apps/streamlit/          # Streamlit dashboard application
├── superset/                    # Superset Docker configuration and init
└── tests/                       # Unit and integration test suites
```

## Setup & Installation

### Prerequisites
- Docker & Docker Compose
- `make` (optional but recommended)

### Quick Start
1. **Initialize infrastructure**:
   ```bash
   make up
   ```
2. **Access the services**:
   - Streamlit Dashboard: `http://localhost:8501`
   - Apache Superset: `http://localhost:8088` (Default credentials: admin/admin)
   - Dagster Webserver: `http://localhost:3000`

### Testing
To run the automated test suite locally:
```bash
make test
```

## CI/CD Pipeline
Continuous Integration is configured via GitHub Actions. On every push to `main` or Pull Request, the pipeline executes:
1. Python unit tests via `pytest`.
2. Pipeline integration tests against an ephemeral DuckDB database.
3. Build verification for all Docker containers.

## License
Proprietary. All rights reserved.
