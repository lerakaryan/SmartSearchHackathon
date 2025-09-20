import re
from typing import Dict, List, Any
from sentence_transformers import SentenceTransformer
import numpy as np

class IntentClassifier:
    def __init__(self):
        # Модель для семантического сравнения
        self.model = SentenceTransformer('sentence-trsansformers/paraphrase-multilingual-MiniLM-L12-v2')
        
        # Маппинг намерений и их описаний
        self.intents = {
            # Вопросы (поиск статей)
            "search_article": {
                "description": "Поиск справочной информации и статей в базе знаний",
                "examples": ["как создать", "как добавить", "как найти", "как работает", "инструкция"],
                "type": "question"
            },
            
            # Действия заказчика
            "add_to_cart": {
                "description": "Добавление оферты в корзину",
                "examples": ["добавить в корзину", "положить в корзину", "добавь оферту"],
                "type": "action"
            },
            "remove_from_cart": {
                "description": "Удаление оферты из корзины",
                "examples": ["удалить из корзины", "убрать из корзины", "удали оферту"],
                "type": "action"
            },
            "create_direct_purchase": {
                "description": "Создание заявки на прямую закупку",
                "examples": ["создать заявку", "прямая закупка", "заявка на закупку"],
                "type": "action"
            },
            "create_ks": {
                "description": "Создание котировочной сессии",
                "examples": ["создать котировочную сессию", "запустить кс", "организовать тендер"],
                "type": "action"
            },
            "view_contracts": {
                "description": "Просмотр контрактов своей организации",
                "examples": ["показать контракты", "мои контракты", "посмотреть договоры"],
                "type": "action"
            },
            
            # Действия администратора
            "create_user": {
                "description": "Создание пользователей компании",
                "examples": ["создать пользователя", "добавить сотрудника", "новый пользователь"],
                "type": "action"
            },
            "block_user": {
                "description": "Блокирование пользователя",
                "examples": ["заблокировать пользователя", "отключить доступ", "блокировка"],
                "type": "action"
            },
            
            # Действия поставщика
            "create_offer": {
                "description": "Создание, изменение и публикация оферты",
                "examples": ["создать оферту", "добавить предложение", "новая оферта"],
                "type": "action"
            },
            "create_bid": {
                "description": "Создание ставки в котировочной сессии",
                "examples": ["сделать ставку", "участвовать в тендере", "подать заявку"],
                "type": "action"
            },
            
            # Запасной вариант
            "unknown": {
                "description": "Не удалось определить намерение",
                "examples": [],
                "type": "error"
            }
        }
        
        # Подготовка эмбеддингов для быстрого поиска
        self.intent_embeddings = None
        self.intent_descriptions = []
        self.prepare_intents()
    
    def prepare_intents(self):
        """Подготавливает эмбеддинги для всех намерений"""
        self.intent_descriptions = []
        self.intent_ids = []
        
        for intent_id, intent_data in self.intents.items():
            # Добавляем описание и примеры
            self.intent_descriptions.append(intent_data["description"])
            for example in intent_data["examples"]:
                self.intent_descriptions.append(example)
            self.intent_ids.extend([intent_id] * (1 + len(intent_data["examples"])))
        
        # Создаем эмбеддинги
        if self.intent_descriptions:
            self.intent_embeddings = self.model.encode(self.intent_descriptions)
    
    def rule_based_classification(self, text: str) -> Dict[str, Any]:
        """Правиловая классификация с использованием ключевых слов"""
        rules = {
            "add_to_cart": [r"добавь?.*корзин", r"положи.*корзин", r"в корзин"],
            "remove_from_cart": [r"удали?.*корзин", r"убери.*корзин", r"из корзин"],
            "create_ks": [r"создай?.*кс", r"создай?.*котировоч", r"создай?.*тендер", 
                         r"запусти.*кс", r"организуй.*закупк"],
            "create_offer": [r"создай?.*оферт", r"добавь.*оферт", r"новая.*оферт"],
            "search_article": [r"как.*созда", r"как.*добав", r"как.*найт", r"инструкция", r"помощь"],
        }
        
        for intent_id, patterns in rules.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    return {
                        "intent": intent_id,
                        "confidence": 0.9,
                        "method": "rule_based",
                        "type": self.intents[intent_id]["type"]
                    }
        
        return None
    
    def semantic_classification(self, text: str, top_k: int = 3) -> Dict[str, Any]:
        """Семантическая классификация с использованием эмбеддингов"""
        if self.intent_embeddings is None:
            return None
            
        text_embedding = self.model.encode([text])
        similarities = np.dot(self.intent_embeddings, text_embedding.T).flatten()
        
        # Группируем результаты по intent_id
        intent_scores = {}
        for i, similarity in enumerate(similarities):
            intent_id = self.intent_ids[i]
            if intent_id not in intent_scores:
                intent_scores[intent_id] = []
            intent_scores[intent_id].append(similarity)
        
        # Усредняем score для каждого intent
        averaged_scores = {}
        for intent_id, scores in intent_scores.items():
            averaged_scores[intent_id] = np.mean(scores)
        
        # Находим лучшее совпадение
        if not averaged_scores:
            return None
            
        best_intent = max(averaged_scores.items(), key=lambda x: x[1])
        
        return {
            "intent": best_intent[0],
            "confidence": float(best_intent[1]),
            "method": "semantic",
            "type": self.intents[best_intent[0]]["type"]
        }
    
    def classify_intent(self, text: str) -> Dict[str, Any]:
        """Основной метод классификации намерения"""
        if not text.strip():
            return {
                "intent": "unknown",
                "confidence": 0.0,
                "method": "empty",
                "type": "error"
            }
        
        # 1. Сначала пробуем rule-based подход
        rule_result = self.rule_based_classification(text)
        if rule_result and rule_result["confidence"] > 0.7:
            return rule_result
        
        # 2. Если rule-based не сработал, используем semantic
        semantic_result = self.semantic_classification(text)
        if semantic_result and semantic_result["confidence"] > 0.6:
            return semantic_result
        
        # 3. Если оба метода не сработали
        return {
            "intent": "unknown",
            "confidence": 0.0,
            "method": "fallback",
            "type": "error"
        }
    
    def determine_sentence_type(self, text: str) -> str:
        """Определяет общий тип предложения (вопрос/действие)"""
        # Быстрая проверка по правилам
        question_patterns = [
            r'^как', r'^где', r'^кто', r'^что', r'^почему', r'^зачем',
            r'^когда', r'^сколько', r'^какой', r'^можно ли', r'^возможно ли',
            r'\?$', r'как сделать', r'как создать', r'как добавить'
        ]
        
        for pattern in question_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return "question"
        
        # Если не вопрос, то скорее всего действие
        return "action"

# Пример использования
if __name__ == "__main__":
    classifier = IntentClassifier()
    
    test_cases = [
        "как создать котировочную сессию",
        "сделай кс на 100000 рублей",
        "добавь оферту 123 в корзину",
        "покажи мои контракты",
        "хочу пиццы с ананасами"  # Неизвестный запрос
    ]
    
    for text in test_cases:
        print(f"\nТекст: '{text}'")
        result = classifier.classify_intent(text)
        print(f"Намерение: {result['intent']}")
        print(f"Тип: {result['type']}")
        print(f"Уверенность: {result['confidence']:.2f}")
        print(f"Метод: {result['method']}")
        print("-" * 50)