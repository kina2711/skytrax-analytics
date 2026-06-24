FROM python:3.11-slim

WORKDIR /opt/dagster/app

# Install Dagster and dbt dependencies
COPY orchestration/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV DAGSTER_HOME=/opt/dagster/dagster_home
RUN mkdir -p $DAGSTER_HOME

COPY orchestration/ .

CMD ["dagster-daemon", "run"]
