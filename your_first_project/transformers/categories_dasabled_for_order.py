import pandas as pd
from pandas import DataFrame
import math

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@transformer
def filter_categories(sm_df: DataFrame, *args, **kwargs) -> DataFrame:
    categories_to_filter = [
        "НАПИТКИ АЛКОГОЛЬНЫЕ",
        "НАПИТКИ СЛАБОАЛКОГОЛЬНЫЕ",
        "ПИВО",
        "ТАБАЧНЫЕ ИЗДЕЛИЯ"
    ]

    filtered_df = sm_df[sm_df['name'].str.contains('|'.join(categories_to_filter), case=False, na=False)]

    result_rows = []

    for _, row in filtered_df.iterrows():
        result_rows.append({
            'cls_code': row['code'],
            'cls_type_id': 7,
            'age_restriction': 18,
        })

    final_df = pd.DataFrame(result_rows)

    return final_df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
