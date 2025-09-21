from typing import List, Dict, Any, Optional

import requests
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

from catboost_predictor import IntentPredictor
from entity_extractor import EntityExtractor
from registry_records import UniversalContractSearcher, convert_dataframe_to_json
import uvicorn
import re
predictor = IntentPredictor()
extractor = EntityExtractor()
registry = UniversalContractSearcher()
files = [
    "Контракты_ПП_Тендерхак_20250919.xlsx",
    "Котировочные сессии_ПП_Тендерхак_20250919.xlsx"
]

app = FastAPI(title="Intent & Entity API")

ask_regex = "( |^)(кто|что|где|когда|почему|как|какие|сколько|зачем|чей|куда|откуда)( |$)|\?.*"


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200", "http://localhost:3000"],  # Разрешенные origins
    allow_credentials=True,
    allow_methods=["*"],  # Разрешенные HTTP методы
    allow_headers=["*"],  # Разрешенные заголовки
)


class TextRequest(BaseModel):
    text: str


class RegistryRecord(BaseModel):
    type: str
    hintType: int
    data: Dict[str, str]


class IntentEntity(BaseModel):
    name: str
    entities: Dict[str, Any]


class PredictionResponse(BaseModel):
    registry_records: List[RegistryRecord]
    knowledge_base_articles: List[List[str]]
    intents: Optional[IntentEntity] = None


def knowledge_base_search(text: str) -> List[List[str]]:
    url = "https://zakupki.mos.ru/newapi/api/KnowledgeBase/GetArticlesPreview"
    query = {"filter": {"textPattern": text}}
    resp = requests.get(url, params={"query": str(query)})
    resp.raise_for_status()
    data = resp.json()

    results = []
    for item in data.get("items", []):
        name = item.get("largeName", "")
        static_id = item.get("staticId")
        if static_id:
            article_url = f"https://zakupki.mos.ru/knowledgebase/articles/{static_id}"
            results.append([name, article_url])
    return results


def intent_prediction(text: str) -> IntentEntity:
    return IntentEntity(
        name=predictor.predict(text)[0],
        entities=extractor.extract(text)
    )


@app.post("/predict", response_model=PredictionResponse)
def predict_intent(request: TextRequest):
    knowledge_base_articles = []
    registry_records = []
    intents = None

    text = request.text

    #### regex
    is_question = re.search(ask_regex, text.lower())

    if is_question:
        knowledge_base_articles = knowledge_base_search(text)[:2]
    else:
        if len(text) >= 3:
            registry_records = convert_dataframe_to_json(registry.search_in_files(files, request.text))

        intents = intent_prediction(text)

    return PredictionResponse(
        registry_records=registry_records,
        knowledge_base_articles=knowledge_base_articles,
        intents=intents
    )


@app.post("/predict_mock", response_model=PredictionResponse)
def predict_intent(request: TextRequest):
    mock = {
        "registry_records": [
            {"type": "кс", "data": ["id name бла бла"]},
            {"type": "контракт", "data": ["id namr бла бла"]}
        ],
        "knowledge_base_articles": [
            ["Как создать нового пользователя ?", '213981'],
            ["Как добавить учетную запись", '214532']
        ],
        "intents": {
            "name": "создание контракта",
            "entities": {
                "dates": ["2025-09-20"],
                "money": ["300 тыс."],
                "name": ["канцелярские товары"],
                "addr": ["Москва"]
            }
        }
    }

    return mock


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
