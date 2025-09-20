from typing import List, Dict, Any

from fastapi import FastAPI
from pydantic import BaseModel
from catboost_predictor import IntentPredictor
from entity_extractor import EntityExtractor
from registry_records import UniversalContractSearcher, convert_dataframe_to_json
import uvicorn
import pandas as pd
import json

predictor = IntentPredictor()
extractor = EntityExtractor()
registry = UniversalContractSearcher()
files = [
    "Контракты_ПП_Тендерхак_20250919.xlsx",
    "Котировочные сессии_ПП_Тендерхак_20250919.xlsx"
]

app = FastAPI(title="Intent & Entity API")

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
    data: List[str]


class IntentEntity(BaseModel):
    name: str
    entities: Dict[str, Any]


class PredictionResponse(BaseModel):
    registry_records: List[RegistryRecord]
    knowledge_base_articles: List[List[str]]
    intents: IntentEntity


def registry_search(text: str) -> List[RegistryRecord]:
    return [
        RegistryRecord(type="кс", data=[text]),
        RegistryRecord(type="контракт", data=[f"Обработанный: {text}"])
    ]


def knowledge_base_search(text: str) -> List[List[str]]:
    return [
        ["Как создать нового пользователя ?", "213981"],
        ["Как добавить учетную запись", "214532"]
    ]


def intent_prediction(text: str) -> IntentEntity:
    return IntentEntity(
            name=predictor.predict(text)[0],
            entities=extractor.extract(text)
        )



@app.post("/predict", response_model=PredictionResponse)
def predict_intent(request: TextRequest):


    #### сделать
    is_question = False ## Regex

    if is_question:
        # база знаний
        pass


    #### сделать
    registry_records = convert_dataframe_to_json(registry.search_in_files(files, request.text))

    #### сделать
    knowledge_base_articles = knowledge_base_search(request.text)

    intents = intent_prediction(request.text)

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

