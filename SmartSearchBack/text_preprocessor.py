import re
from symspellpy import SymSpell, Verbosity
import pkg_resources
from pymorphy3 import MorphAnalyzer
from nltk.corpus import stopwords
import nltk

# Скачиваем стоп-слова при первом запуске
nltk.download('stopwords')

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

# Пример использования
if __name__ == "__main__":
    preprocessor = TextPreprocessor()
    
    test_phrases = [
        "сделай кс закупку",
        "cltkfq rc pfregre",
        "оформи тендер на поставку",
        "создай котировочную сессию",
        "найди контрагента по инн",
        "покажи мои запки на прямые закупки",  # Здесь есть опечатка "запки"
        "удали оферту из корзины",
        "сгенерируй отчет по кс"
    ]
    
    for phrase in test_phrases:
        print(f"\nОригинал: {phrase}")
        result = preprocessor.full_preprocess(phrase)
        print(f"Результат: {result}")
        print("-" * 50)