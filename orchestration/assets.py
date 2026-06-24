from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets

import os

dbt_project_dir = os.path.join(os.path.dirname(__file__), "..", "dbt_project")
dbt = DbtCliResource(project_dir=dbt_project_dir)

@dbt_assets(manifest=os.path.join(dbt_project_dir, "target", "manifest.json"))
def skytrax_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
