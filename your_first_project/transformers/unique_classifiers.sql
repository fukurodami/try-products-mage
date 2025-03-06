import pandas as pd
from pandas import DataFrame
import math

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@transformer
def filter_categories(df: DataFrame, *args, **kwargs) -> DataFrame:
    categories_to_filter = [
        "НАПИТКИ АЛКОГОЛЬНЫЕ",
        "НАПИТКИ СЛАБОАЛКОГОЛЬНЫЕ",
        "ПИВО",
        "ТАБАЧНЫЕ ИЗДЕЛИЯ"
    ]

    filtered_df = df[df['Category'].isin(categories_to_filter)]

    return filtered_df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
