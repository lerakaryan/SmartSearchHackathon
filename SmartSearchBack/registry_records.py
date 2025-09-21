import re
import pandas as pd
from typing import List
import json


class ContractQueryParser:
    def __init__(self):
        self.id_pattern = re.compile(r'\b(\d{6,9})\b')

    def parse_query(self, query: str) -> dict:
        query = query.lower()

        # поиск ID
        id_matches = self.id_pattern.findall(query)
        search_id = id_matches[0] if id_matches else None

        # тип документа
        if any(word in query for word in ['котировочная', 'кс', 'сессия']):
            document_type = 'ks'
        elif any(word in query for word in ['контракт', 'договор', 'дог']):
            document_type = 'contract'
        else:
            document_type = 'any'

        # текст для поиска по названию
        clean_query = query
        if search_id:
            clean_query = clean_query.replace(search_id, '')

        service_words = ['кс', 'котировочная', 'сессия', 'контракт', 'договор', 'дог']
        for word in service_words:
            clean_query = clean_query.replace(word, '')

        search_name = clean_query.strip() if clean_query.strip() else None

        return {
            'search_id': search_id,
            'search_name': search_name,
            'document_type': document_type
        }


import re
import pandas as pd
from typing import List, Dict, Tuple

class ContractQueryParser:
    def __init__(self):
        self.id_pattern = re.compile(r'\b(\d{6,9})\b')

    def parse_query(self, query: str) -> dict:
        query = query.lower()

        # поиск ID
        id_matches = self.id_pattern.findall(query)
        search_id = id_matches[0] if id_matches else None

        # тип документа
        if any(word in query for word in ['котировочная', 'кс', 'сессия']):
            document_type = 'ks'
        elif any(word in query for word in ['контракт', 'договор', 'дог']):
            document_type = 'contract'
        else:
            document_type = 'any'

        # текст для поиска по названию
        clean_query = query
        if search_id:
            clean_query = clean_query.replace(search_id, '')

        service_words = ['кс', 'котировочная', 'сессия', 'контракт', 'договор', 'дог']
        for word in service_words:
            clean_query = clean_query.replace(word, '')

        search_name = clean_query.strip() if clean_query.strip() else None

        return {
            'search_id': search_id,
            'search_name': search_name,
            'document_type': document_type
        }


class UniversalContractSearcher:
    def __init__(self):
        self.parser = ContractQueryParser()

    def search_in_files(self, file_paths: List[str], query: str) -> dict[str, pd.DataFrame]:
        """
        Поиск в файлах с возвращением отдельных датафреймов для КС и контрактов
        """
        parsed_query = self.parser.parse_query(query)
        ks_results = []
        contract_results = []

        for file_path in file_paths:
            try:
                xls = pd.ExcelFile(file_path)

                for sheet_name in xls.sheet_names:
                    if 'скрипт' in sheet_name.lower():
                        continue

                    df = pd.read_excel(file_path, sheet_name=sheet_name)
                    is_ks_data = 'ID КС' in df.columns
                    
                    # Проверяем, соответствует ли тип данных запросу
                    if parsed_query['document_type'] == 'ks' and not is_ks_data:
                        continue
                    if parsed_query['document_type'] == 'contract' and is_ks_data:
                        continue
                    
                    id_col = 'ID КС' if is_ks_data else 'ID контракта'
                    name_col = 'Наименование КС' if is_ks_data else 'Наименование контракта'

                    mask = pd.Series([False] * len(df))

                    if parsed_query['search_id']:
                        mask = mask | (df[id_col].astype(str) == parsed_query['search_id'])
                    if parsed_query['search_name']:
                        name_mask = df[name_col].astype(str).str.lower().str.contains(
                            parsed_query['search_name'].lower(), na=False
                        )
                        mask = mask | name_mask
                    
                    results = df[mask].copy()
                    if not results.empty:
                        results['Тип документа'] = 'КС' if is_ks_data else 'Контракт'
                        
                        # Разделяем результаты по типам
                        if is_ks_data:
                            ks_results.append(results)
                        else:
                            contract_results.append(results)

            except Exception as e:
                print(f"Ошибка при обработке файла {file_path}: {e}")

        # Создаем отдельные датафреймы для каждого типа
        ks_df = pd.concat(ks_results, ignore_index=True) if ks_results else pd.DataFrame()
        contract_df = pd.concat(contract_results, ignore_index=True) if contract_results else pd.DataFrame()
        
        return {
            'ks': ks_df,
            'contract': contract_df
        }

    def search_in_files_with_list(self, file_paths: List[str], query: str) -> List[pd.DataFrame]:
        """
        список датафреймов [КС, Контракты]
        """
        result_dict = self.search_in_files(file_paths, query)
        return [result_dict['ks'], result_dict['contract']]

""""
def convert_dataframe_to_json(df):
    result = []
    for _, row in df.iterrows():
        # КС (hintType=2), контракт (hintType=1)
        if pd.notna(row.get(4)) and row.get(5) != '':
            item = {
                "type": "registry",
                "hintType": 2,
                "data": {
                    "ksName": str(row.get(1, '')),
                    "ksId": str(row.get(2, '')),
                    "ksAmount": str(row.get(3, '')),
                    "creationDate": str(row.get(4, '')),
                    "completionDate": str(row.get(5, '')),
                    "category": str(row.get(6, '')),
                    "customerName": str(row.get(7, '')),
                    "customerINN": str(row.get(8, '')),
                    "supplierName": str(row.get(9, '')),
                    "supplierINN": str(row.get(10, '')),
                    "lawBasis": str(row.get(11, ''))
                }
            }
        else:
            item = {
                "type": "registry",
                "hintType": 1,
                "data": {
                    "contractName": str(row.get(1, '')),
                    "contractId": str(row.get(2, '')),
                    "contractAmount": str(row.get(3, '')),
                    "contractDate": str(row.get(4, '')),
                    "category": str(row.get(5, '')),
                    "customerName": str(row.get(6, '')),
                    "customerINN": str(row.get(7, '')),
                    "supplierName": str(row.get(8, '')),
                    "supplierINN": str(row.get(9, '')),
                    "lawBasis": str(row.get(10, ''))
                }
            }
        result.append(item)
    return result
"""
def convert_dataframes_to_json(results_list):
    """
    Безопасная версия с дополнительными проверками для списка датафреймов
    results_list: [ks_dataframe, contract_dataframe]
    """
    result = []
    
    def get_value_safe(row, index, default=''):
        """Безопасное получение значения по индексу с обработкой исключений"""
        try:
            # Проверяем, что индекс существует и значение не NaN/пустое
            if index < len(row):
                value = row.iloc[index]
                if pd.isna(value) or (isinstance(value, str) and value.strip() == ''):
                    return default
                return str(value)
            return default
        except Exception as e:
            print(f"Ошибка при получении значения по индексу {index}: {e}")
            return default
    
    # Проверяем и обрабатываем КС (первый элемент списка)
    if len(results_list) > 0:
        ks_data = results_list[0]
        if isinstance(ks_data, pd.DataFrame) and not ks_data.empty:
            print(f"Обрабатываем КС, строк: {len(ks_data)}")
            for idx, row in ks_data.iterrows():
                try:
                    item = {
                        "type": "registry",
                        "hintType": 2,
                        "data": {
                            "ksName": get_value_safe(row, 1),
                            "ksId": get_value_safe(row, 2),
                            "ksAmount": get_value_safe(row, 3),
                            "creationDate": get_value_safe(row, 4),
                            "completionDate": get_value_safe(row, 5),
                            "category": get_value_safe(row, 6),
                            "customerName": get_value_safe(row, 7),
                            "customerINN": get_value_safe(row, 8),
                            "supplierName": get_value_safe(row, 9),
                            "supplierINN": get_value_safe(row, 10),
                            "lawBasis": get_value_safe(row, 11)
                        }
                    }
                    result.append(item)
                except Exception as e:
                    print(f"Ошибка при обработке строки КС {idx}: {e}")
    
    # Проверяем и обрабатываем контракты (второй элемент списка)
    if len(results_list) > 1:
        contract_data = results_list[1]
        if isinstance(contract_data, pd.DataFrame) and not contract_data.empty:
            print(f"Обрабатываем контракты, строк: {len(contract_data)}")
            for idx, row in contract_data.iterrows():
                try:
                    item = {
                        "type": "registry",
                        "hintType": 1,
                        "data": {
                            "contractName": get_value_safe(row, 1),
                            "contractId": get_value_safe(row, 2),
                            "contractAmount": get_value_safe(row, 3),
                            "contractDate": get_value_safe(row, 4),
                            "category": get_value_safe(row, 5),
                            "customerName": get_value_safe(row, 6),
                            "customerINN": get_value_safe(row, 7),
                            "supplierName": get_value_safe(row, 8),
                            "supplierINN": get_value_safe(row, 9),
                            "lawBasis": get_value_safe(row, 10)
                        }
                    }
                    result.append(item)
                except Exception as e:
                    print(f"Ошибка при обработке строки контракта {idx}: {e}")
    
    return result