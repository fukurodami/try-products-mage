from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from os import path
from pandas import DataFrame

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def unique_cls(df: DataFrame, *args, **kwargs) -> DataFrame:
    df = clean_empty_like_strings(df)
    df = fill_missing_values_with_median(df)
    
    unique_categories = df[['Category', 'Group', 'Subgroup']].drop_duplicates()

    return unique_categories


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
