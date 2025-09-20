import re
import pandas as pd
from typing import List

class ContractQueryParser:
    def __init__(self):
        self.id_pattern = re.compile(r'\b(\d{6,9})\b')
        
    def parse_query(self, query: str) -> dict:
        query = query.lower()
        
        # Поиск ID
        id_matches = self.id_pattern.findall(query)
        search_id = id_matches[0] if id_matches else None
        
        # Определяем тип документа
        if any(word in query for word in ['котировочная', 'кс', 'сессия']):
            document_type = 'ks'
        elif any(word in query for word in ['контракт', 'договор', 'дог']):
            document_type = 'contract'
        else:
            document_type = 'any'
        
        # Извлекаем текст для поиска по названию
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
    
    def search_in_files(self, file_paths: List[str], query: str) -> pd.DataFrame:
        parsed_query = self.parser.parse_query(query)
        all_results = []
        
        for file_path in file_paths:
            try:
                xls = pd.ExcelFile(file_path)
                
                for sheet_name in xls.sheet_names:
                    if 'скрипт' in sheet_name.lower():
                        continue
                    
                    df = pd.read_excel(file_path, sheet_name=sheet_name)
                    is_ks_data = 'ID КС' in df.columns
                    
                    # Проверяем совместимость типа документа
                    if (parsed_query['document_type'] == 'ks' and not is_ks_data) or \
                       (parsed_query['document_type'] == 'contract' and is_ks_data):
                        continue
                    
                    # Определяем колонки для поиска
                    id_col = 'ID КС' if is_ks_data else 'ID контракта'
                    name_col = 'Наименование КС' if is_ks_data else 'Наименование контракта'
                    
                    # Фильтрация данных
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
                        all_results.append(results)
                        
            except Exception as e:
                print(f"Ошибка при обработке файла {file_path}: {e}")
        
        return pd.concat(all_results, ignore_index=True) if all_results else pd.DataFrame()
def convert_dataframe_to_json(df):
    """
    Преобразует DataFrame в JSON структуру для фронтенда
    """
    result = []
    
    for _, row in df.iterrows():
        # Определяем тип записи (контракт или КС)
        # Если есть дата завершения - это КС (hintType=2), иначе контракт (hintType=1)
        if pd.notna(row.get('Дата завершения КС')) and row.get('Дата завершения КС') != '':
            item = {
                "type": "registry",
                "hintType": 2,
                "data": {
                    "ksName": row.get('Наименование КС', ''),
                    "ksId": row.get('ID КС', ''),
                    "ksAmount": str(row.get('Сумма КС', '')),
                    "creationDate": row.get('Дата создания КС', ''),
                    "completionDate": row.get('Дата завершения КС', ''),
                    "category": row.get('Категория ПП первой позиции спецификации', ''),
                    "customerName": row.get('Наименование заказчика', ''),
                    "customerINN": row.get('ИНН заказчика', ''),
                    "supplierName": row.get('Наименование поставщика', ''),
                    "supplierINN": row.get('ИНН поставщика', ''),
                    "lawBasis": row.get('Закон-основание', '')
                }
            }
        else:
            item = {
                "type": "registry",
                "hintType": 1,
                "data": {
                    "contractName": row.get('Наименование КС', ''),
                    "contractId": row.get('ID КС', ''),
                    "contractAmount": str(row.get('Сумма КС', '')),
                    "contractDate": row.get('Дата создания КС', ''),
                    "category": row.get('Категория ПП первой позиции спецификации', ''),
                    "customerName": row.get('Наименование заказчика', ''),
                    "customerINN": row.get('ИНН заказчика', ''),
                    "supplierName": row.get('Наименование поставщика', ''),
                    "supplierINN": row.get('ИНН поставщика', ''),
                    "lawBasis": row.get('Закон-основание', '')
                }
            }
        
        result.append(item)
    
    return json.dumps(result, ensure_ascii=False, indent=2)