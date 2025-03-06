import pandas as pd
from pandas import DataFrame
import math

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

def clean_empty_like_strings(df: DataFrame) -> DataFrame:
    for col in df.select_dtypes(include=['object', 'string']).columns:
        df[col] = df[col].replace([r'^\s+$', r'\\n+', r'None'], '', regex=True)
        df[col] = df[col].replace('', pd.NA)
    return df

def fill_missing_values_with_median(df: DataFrame) -> DataFrame:
    for col in df.select_dtypes(include=['number']).columns:
        values = sorted(df[col].dropna().tolist())
        median_value = values[math.floor(len(values) / 2)]
        df[col] = df[col].fillna(median_value)
    return df

def get_next_code(existing_codes: list, prefix: str, level_length: int = 3) -> str:
    filtered_codes = [code for code in existing_codes if code.startswith(prefix)]
    if not filtered_codes:
        return f"{prefix}{'1'.zfill(level_length)}"
    
    numeric_parts = [int(code[len(prefix):]) for code in filtered_codes if code[len(prefix):].isdigit()]
    if not numeric_parts:
        return f"{prefix}{'1'.zfill(level_length)}"

    last_code = max(numeric_parts)
    next_code = last_code + 1
    return f"{prefix}{str(next_code).zfill(level_length)}"

@transformer
def unique_cls(sm_df: DataFrame, lama_df: DataFrame, *args, **kwargs) -> DataFrame:
    lama_df = clean_empty_like_strings(lama_df)
    lama_df = fill_missing_values_with_median(lama_df)

    unique_categories = lama_df[['SKU', 'Category', 'Group', 'Subgroup', 'Sector']].drop_duplicates()
    
    # Сортируем данные
    unique_categories = unique_categories.sort_values(by=['Sector', 'Category', 'Group', 'Subgroup'], na_position='last')

    sm_category_map = sm_df.set_index('full_name')['code'].to_dict()

    def get_or_create_code(name, full_name, level_prefix, level_length=3):
        if full_name in sm_category_map:
            return sm_category_map[full_name]
        
        existing_codes = sm_df['code'].tolist()
        new_code = get_next_code(existing_codes, level_prefix, level_length)
        sm_category_map[full_name] = new_code
        return new_code

    result_rows = []

    for _, row in unique_categories.iterrows():
        sector_name = row['Sector']
        category_name = row['Category']
        group_name = row['Group']
        subgroup_name = row['Subgroup']

        sector_code = get_or_create_code(sector_name, sector_name, '', 1)

        category_full_name = f"{sector_name}.{category_name}" if pd.notna(category_name) else None
        category_code = get_or_create_code(category_name, category_full_name, f"{sector_code}.", 2) if category_full_name else None

        group_full_name = f"{category_full_name}.{group_name}" if pd.notna(group_name) else None
        group_code = get_or_create_code(group_name, group_full_name, f"{category_code}.", 3) if group_full_name else None

        subgroup_full_name = f"{group_full_name}.{subgroup_name}" if pd.notna(subgroup_name) else None
        subgroup_code = get_or_create_code(subgroup_name, subgroup_full_name, f"{group_code}.", 4) if subgroup_full_name else None

        # if (row['Subgroup'] == 'БАД ЗОЖ'):
        #     print(f"Sector: {sector_name}, Code: {sector_code}")
        #     print(f"Category: {category_name}, Code: {category_code}")
        #     print(f"Group: {group_name}, Code: {group_code}")
        #     print(f"Subgroup: {subgroup_name}, Code: {subgroup_code}")


        result_rows.append({
            'name': sector_name,
            'code': sector_code,
            'parent_code': None,
            'cls_type_id': 7
        })
        if pd.notna(category_name):
            result_rows.append({
                'name': category_name,
                'code': category_code,
                'parent_code': sector_code,
                'cls_type_id': 7
            })
        if pd.notna(group_name):
            result_rows.append({
                'name': group_name,
                'code': group_code,
                'parent_code': category_code,
                'cls_type_id': 7
            })
        if pd.notna(subgroup_name):
            result_rows.append({
                'name': subgroup_name,
                'code': subgroup_code,
                'parent_code': group_code,
                'cls_type_id': 7
            })

    final_df = pd.DataFrame(result_rows).drop_duplicates(subset='code')
    return final_df

@test
def test_output(records) -> None:
    assert records is not None, 'The output is undefined'
    # assert all('cls_type_id' in record for record in records), 'Missing cls_type_id in some records'
    # assert all('code' in record for record in records), 'Missing code in some records'
    # assert all('name' in record for record in records), 'Missing name in some records'
    # assert all('level' in record for record in records), 'Missing level in some records'
