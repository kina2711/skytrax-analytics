FROM apache/superset:3.1.2

USER root

# Install duckdb-engine so Superset can connect to DuckDB
RUN pip install --no-cache-dir duckdb-engine duckdb==1.1.2 psycopg2-binary

USER superset
