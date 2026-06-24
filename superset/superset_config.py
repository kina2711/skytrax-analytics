import os

FEATURE_FLAGS = {
    "ENABLE_TEMPLATE_PROCESSING": True,
}

ENABLE_PROXY_FIX = True
SECRET_KEY = os.environ.get("SUPERSET_SECRET_KEY", "your_secret_key_here_skytrax_analytics")
SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:////app/superset.db")

# Allow DuckDB driver
PREVENT_UNSAFE_DB_CONNECTIONS = False
