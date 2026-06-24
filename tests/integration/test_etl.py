import pytest
import duckdb
import os

def test_duckdb_connection():
    """
    Integration test to ensure DuckDB is accessible and tables exist.
    """
    db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'warehouse', 'skytrax_lite.duckdb')
    if os.path.exists(db_path):
        con = duckdb.connect(db_path, read_only=True)
        tables = con.execute("SHOW TABLES").df()
        assert not tables.empty
        assert 'dim_airlines' in tables['name'].values
        con.close()
    else:
        pytest.skip(f"Database not found at {db_path}")
