import os
from dagster import Definitions
from dagster_dbt import DbtCliResource
from .assets import skytrax_dbt_assets, dbt_project_dir

defs = Definitions(
    assets=[skytrax_dbt_assets],
    resources={
        "dbt": DbtCliResource(project_dir=os.fspath(dbt_project_dir)),
    },
)
