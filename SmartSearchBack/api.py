from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import io
import json
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware


# Импортируем наши модули
from SmartSearchProcessor import SmartSearchProcessor

app = FastAPI(
    title="Smart Search API",
    description="API для умной поисковой строки с классификацией намерений и извлечением сущностей",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200", "http://localhost:3000"],  # Разрешенные origins
    allow_credentials=True,
    allow_methods=["*"],  # Разрешенные HTTP методы
    allow_headers=["*"],  # Разрешенные заголовки
)

# Инициализируем процессор
processor = SmartSearchProcessor()

# Модель для входных данных
class SearchRequest(BaseModel):
    query: str

# Модель для ответа
class SearchResponse(BaseModel):
    success: bool
    data: Dict[str, Any]
    error: Optional[str] = None
    timestamp: str

@app.post("/api/search", response_model=SearchResponse, summary="Обработать поисковый запрос")
async def process_search(request: SearchRequest):
    """
    Принимает текстовый запрос и возвращает структурированный ответ с:
    - намерением пользователя
    - извлеченными сущностями
    - рекомендациями по действию
    """
    try:
        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Обрабатываем запрос
        result = processor.process_query(request.query)
        result["timestamp"] = datetime.now().isoformat()
        
        return JSONResponse(content=result)
        
    except Exception as e:
        error_response = {
            "success": False,
            "data": {},
            "error": f"Ошибка обработки запроса: {str(e)}"
        }
        return JSONResponse(content=error_response, status_code=500)

@app.get("/api/health", summary="Проверка здоровья сервиса")
async def health_check():
    """Проверяет, что сервис работает корректно"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "smart-search-api"
    }

@app.get("/api/intents", summary="Получить список поддерживаемых намерений")
async def get_available_intents():
    """Возвращает список всех поддерживаемых намерений и их описаний"""
    # Здесь можно вернуть статический список или сгенерировать из classifier
    intents_info = {
        "search_article": "Поиск справочной информации и статей",
        "add_to_cart": "Добавление оферты в корзину",
        "remove_from_cart": "Удаление оферты из корзины",
        "create_ks": "Создание котировочной сессии",
        "create_offer": "Создание оферты",
        "view_contracts": "Просмотр контрактов",
        # ... добавьте остальные намерения
    }
    return {
        "intents": intents_info,
        "count": len(intents_info)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)