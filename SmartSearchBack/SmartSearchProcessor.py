import re
from typing import Dict, List, Any
from sentence_transformers import SentenceTransformer
import numpy as np
from symspellpy import SymSpell, Verbosity
import pkg_resources
from pymorphy3 import MorphAnalyzer
from nltk.corpus import stopwords
import nltk

class TextPreprocessor:
    def __init__(self):
        # Инициализируем корректор опечаток
        self.sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
        
        # Пока используем заглушку
        self.sym_spell.load_dictionary(pkg_resources.resource_filename(
            "symspellpy", "ru-100k.txt"), term_index=0, count_index=1)
        
        # Инициализируем морфологический анализатор
        self.morph = MorphAnalyzer()
        self.russian_stopwords = stopwords.words('russian')

        # Словари для преобразования раскладки
        self.eng_to_rus = {
            'q': 'й', 'w': 'ц', 'e': 'у', 'r': 'к', 't': 'е', 'y': 'н', 'u': 'г',
            'i': 'ш', 'o': 'щ', 'p': 'з', '[': 'х', ']': 'ъ', 'a': 'ф', 's': 'ы',
            'd': 'в', 'f': 'а', 'g': 'п', 'h': 'р', 'j': 'о', 'k': 'л', 'l': 'д',
            ';': 'ж', "'": 'э', 'z': 'я', 'x': 'ч', 'c': 'с', 'v': 'м', 'b': 'и',
            'n': 'т', 'm': 'ь', ',': 'б', '.': 'ю', '/': '.', '`': 'ё', '&': '?',
            '@': '"', '#': '№', '$': ';', '^': ':', '?': ','
        }
        
        self.rus_to_eng = {v: k for k, v in self.eng_to_rus.items()}
        
        # Словарь синонимов для вашей предметной области
        self.synonyms_dict = {
            # Синонимы для создания закупок
            'сделай': 'создать', 'оформи': 'создать', 'запусти': 'создать',
            'организуй': 'создать', 'инициируй': 'создать', 'начни': 'создать',
            
            # Синонимы для котировочных сессий
            'кс': 'котировочная сессия', 'тендер': 'котировочная сессия',
            'конкурс': 'котировочная сессия', 'закупка': 'котировочная сессия',
            'торги': 'котировочная сессия',
            
            # Синонимы для поиска/просмотра
            'найди': 'найти', 'ищи': 'найти', 'отыщи': 'найти', 'подбери': 'найти',
            'покажи': 'показать', 'выведи': 'показать', 'открой': 'показать',
            'посмотри': 'просмотреть', 'глянь': 'просмотреть', 'проверь': 'просмотреть',
            
            # Синонимы для удаления/отмены
            'удали': 'удалить', 'сотри': 'удалить', 'убей': 'удалить', 'ликвидируй': 'удалить',
            'отмени': 'отменить', 'аннулируй': 'отменить', 'прекрати': 'отменить',
            
            # Синонимы для добавления
            'добавь': 'добавить', 'внеси': 'добавить', 'включи': 'добавить',
            'положи': 'добавить', 'помести': 'добавить',
            
            # Другие частые синонимы
            'создай': 'создать', 'сгенерируй': 'создать', 'построй': 'создать',
            'измени': 'изменить', 'поправь': 'изменить', 'скорректируй': 'изменить',
            'отправь': 'отправить', 'передай': 'отправить', 'направь': 'отправить',
            
            # Сокращения и аббревиатуры
            'инн': 'инн', 'огрн': 'огрн', 'кпп': 'кпп', 'фio': 'фио',
            'дог': 'договор', 'дог-р': 'договор', 'контр': 'контрагент',
        }

    def fix_keyboard_layout(self, text: str) -> str:
        """Исправляет текст, набранный в неправильной раскладке"""
        result = []
        for char in text:
            lower_char = char.lower()
            # Пробуем преобразовать из английской в русскую раскладку
            if lower_char in self.eng_to_rus:
                fixed_char = self.eng_to_rus[lower_char]
                # Сохраняем регистр
                result.append(fixed_char.upper() if char.isupper() else fixed_char)
            # Пробуем преобразовать из русской в английскую раскладку
            elif lower_char in self.rus_to_eng:
                fixed_char = self.rus_to_eng[lower_char]
                result.append(fixed_char.upper() if char.isupper() else fixed_char)
            else:
                result.append(char)
        return ''.join(result)
    
    def detect_and_fix_layout(self, text: str) -> str:
        """Определяет, нужно ли исправлять раскладку, и исправляет если нужно"""
        # Если текст содержит много английских букв там, где должны быть русские
        english_letters = sum(1 for char in text.lower() if char in self.eng_to_rus)
        russian_letters = sum(1 for char in text.lower() if char in self.rus_to_eng)
        
        # Если английских букв значительно больше, чем русских
        if english_letters > russian_letters + 2:
            return self.fix_keyboard_layout(text)
        return text
    
    def correct_spelling(self, text: str) -> str:
        """Исправляет опечатки в тексте"""
        try:
            suggestions = self.sym_spell.lookup_compound(text, max_edit_distance=2)
            if suggestions:
                return suggestions[0].term
            return text
        except:
            # Если SymSpell не сработал, возвращаем оригинальный текст
            return text
    
    def replace_synonyms(self, text: str) -> str:
        """Заменяет синонимы на стандартные термины"""
        words = text.split()
        replaced_words = []
        
        for word in words:
            # Ищем синоним в словаре (регистронезависимо)
            lowercase_word = word.lower()
            if lowercase_word in self.synonyms_dict:
                replaced_words.append(self.synonyms_dict[lowercase_word])
            else:
                replaced_words.append(word)
        
        return ' '.join(replaced_words)
    
    def normalize_text(self, text: str) -> str:
        """Нормализует текст: нижний регистр, лемматизация, очистка"""
        # Приводим к нижнему регистру
        text = text.lower()
        
        # Удаляем спецсимволы (оставляем буквы, цифры и пробелы)
        text = re.sub(r'[^а-яё\s]', ' ', text)
        
        # Заменяем множественные пробелы на одинарные
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Разбиваем на слова
        words = text.split()
        
        # Лемматизируем и удаляем стоп-слова
        normalized_words = []
        for word in words:
            if word not in self.russian_stopwords and len(word) > 1:
                try:
                    parsed = self.morph.parse(word)[0]
                    normalized_word = parsed.normal_form
                    normalized_words.append(normalized_word)
                except:
                    normalized_words.append(word)
        
        return ' '.join(normalized_words)
    
    def full_preprocess(self, text: str) -> str:
        """Полный цикл предобработки текста"""
        if not text or not isinstance(text, str):
            return ""
        
        # 1. Исправление раскладки клавиатуры
        layout_fixed = self.detect_and_fix_layout(text)
        print(f"После исправления раскладки: {layout_fixed}")

        # 1. Коррекция опечаток
        corrected = self.correct_spelling(layout_fixed)
        print(f"После коррекции опечаток: {corrected}")
        
        # 2. Замена синонимов
        with_synonyms = self.replace_synonyms(corrected)
        print(f"После замены синонимов: {with_synonyms}")
        
        # 3. Нормализация
        normalized = self.normalize_text(with_synonyms)
        print(f"После нормализации: {normalized}")
        
        return normalized

class IntentClassifier:
    def __init__(self):
        # Модель для семантического сравнения
        self.model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
        # Исправлено: 'sentence-transformers' вместо 'sentence-trsansformers'
        
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


class SmartSearchProcessor:
    def __init__(self):
        self.classifier = IntentClassifier()  # Атрибут экземпляра
        self.preprocessor = TextPreprocessor()  # Атрибут экземпляра
    
    def process_query(self, text: str) -> str:
        result = self.preprocessor.full_preprocess(text)  # Правильно через self
        result = self.classifier.classify_intent(result)  # Правильно через self
        return result
