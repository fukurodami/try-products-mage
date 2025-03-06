from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from os import path
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_postgres(*args, **kwargs):

    query = """
            WITH RECURSIVE full_classifier as (
                SELECT
                    code as code,
                    name as name,
                    level as level,
                    parent_code AS parent_code,
                    CAST(name AS VARCHAR) as full_name
                FROM marketplace.classifier
                WHERE parent_code IS NULL and cls_type_id = 7

                UNION ALL

                SELECT
                    c.code AS code,
                    c.name AS name,
                    c.level as level,
                    c.parent_code AS parent_code,
                    CONCAT(fc.full_name, '.', c.name) AS full_name
                FROM marketplace.classifier c
                INNER JOIN full_classifier fc ON c.parent_code = fc.code
                where c.cls_type_id = 7
            )
            SELECT
                code,
                name,
                level,
                parent_code,
                full_name
            FROM full_classifier;
            """

    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        return loader.load(query)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
