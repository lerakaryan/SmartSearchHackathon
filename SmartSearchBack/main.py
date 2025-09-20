from typing import List, Dict, Any

from fastapi import FastAPI
from pydantic import BaseModel
from catboost_predictor import IntentPredictor
from entity_extractor import EntityExtractor
import uvicorn
from spellchecker import SpellChecker
import re

predictor = IntentPredictor()
extractor = EntityExtractor()

app = FastAPI(title="Intent & Entity API")

test = SpellChecker(language='ru')
ask_regex = "( |^)(кто|что|где|когда|почему|как|какие|сколько|зачем|чей|куда|откуда)( |$)|\?.*"

def correction(text):
    words = text.split(" ")
    corrected_words = [test.correction(word) for word in words]
    return " ".join(corrected_words)


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

    knowledge_base_articles = []

    ## correction
    text = correction(request)

    #### regex
    is_question = re.search(ask_regex, text.lower())

    if is_question:
        knowledge_base_articles = knowledge_base_search(text)

    #### сделать
    registry_records = registry_search(text)

    #### сделать


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