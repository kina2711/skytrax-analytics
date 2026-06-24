from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets
from pathlib import Path

dbt_project_dir = Path(__file__).joinpath("..", "..", "dbt_skytrax").resolve()

@dbt_assets(manifest=dbt_project_dir.joinpath("target", "manifest.json"))
def skytrax_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
