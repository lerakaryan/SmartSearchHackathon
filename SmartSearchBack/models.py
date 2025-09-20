from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# Модель для входящего запроса от фронтенда
class SearchQuery(BaseModel):
    query_text: str = Field(..., description="Текст запроса, введенный пользователем в поисковую строку.")
   

# Модель для извлеченной сущности (Entity)
class Entity(BaseModel):
    type: str = Field(..., description="Тип сущности, например, 'ИНН', 'ФИО', 'компания'.")
    value: str = Field(..., description="Значение сущности, например, '1234567890', 'Иван Иванов'.")
    confidence: Optional[float] = Field(None, description="Уверенность модели в извлечении (от 0 до 1).")

# Модель для ответа от бэкенда
class SearchResponse(BaseModel):
    original_query: str = Field(..., description="Оригинальный запрос пользователя.")
    normalized_query: str = Field(..., description="Запрос после коррекции опечаток и нормализации.")
    intent: str = Field(..., description="Определенное намерение пользователя, например, 'search_counterparty'.")
    confidence: float = Field(..., description="Уверенность классификатора в намерении (от 0 до 1).")
    entities: List[Entity] = Field(..., description="Список извлеченных из запроса сущностей.")
    response_data: Optional[Dict[str, Any]] = Field(None, description="Дополнительные структурированные данные для ответа.")
    # output_text: Optional[str] = Field(None, description="Текстовый ответ, который можно зачитать пользователю.") # Можно добавить позже