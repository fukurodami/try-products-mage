import os
from mage_ai.io.file import FileIO
from pandas import DataFrame

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_loader
def load_data_from_api(**kwargs) -> DataFrame:
    PRODUCTS_PATH = '/home/ilya/Product.csv.gz'
    print("Текущая рабочая директория:", os.getcwd())
    print("Проверка наличия файла:", os.path.exists(PRODUCTS_PATH))

    try:
        data = FileIO().load(
            PRODUCTS_PATH,
            format='csv',
            compression='gzip',
            sep='\t',
            quotechar='"',
            on_bad_lines='skip'
        )
        print("Файл успешно загружен")
        return data
    except FileNotFoundError:
        print(f"Файл не найден: {PRODUCTS_PATH}")
        return DataFrame()
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return DataFrame()