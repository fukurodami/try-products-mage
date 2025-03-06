from mage_ai.io.file import FileIO
from pandas import DataFrame
import pandas as pd
from os import path
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.postgres import Postgres
from mage_ai.io.config import ConfigFileLoader

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_to_classifier(df: DataFrame, **kwargs):
    schema_name = 'marketplace'
    table_name = 'classifier'
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        loader.export(
            df,
            schema_name,
            table_name,
            index=False,
            if_exists='append',
            unique_conflict_method='UPDATE',
            unique_constraints=["cls_type_id", "code"],
            batch_size=250000,
            auto_clean_name=False  
        )

    # filepath = 'classifier_export.csv'
    # df.to_csv(filepath, index=False)
