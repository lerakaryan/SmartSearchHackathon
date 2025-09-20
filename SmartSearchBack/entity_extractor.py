from collections import namedtuple

from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,

    NamesExtractor,
    DatesExtractor,
    MoneyExtractor,
    AddrExtractor,
    Doc
)

Match = namedtuple('Match', ['start', 'stop', 'fact'])
Date = namedtuple('Date', ['year', 'month', 'day'])
Money = namedtuple('Money', ['amount', 'currency'])
Name = namedtuple('Name', ['first', 'last', 'middle'])
AddrPart = namedtuple('AddrPart', ['value', 'type'])
Addr = namedtuple('Addr', ['parts'])

class EntityExtractor:
    def __init__(self):
        # Базовые инструменты
        self.segmenter = Segmenter()
        self.morph_vocab = MorphVocab()

        emb = NewsEmbedding()
        self.morph_tagger = NewsMorphTagger(emb)
        self.syntax_parser = NewsSyntaxParser(emb)
        self.ner_tagger = NewsNERTagger(emb)

        # Дополнительные экстракторы
        self.names_extractor = NamesExtractor(self.morph_vocab)
        self.dates_extractor = DatesExtractor(self.morph_vocab)
        self.money_extractor = MoneyExtractor(self.morph_vocab)
        self.addr_extractor = AddrExtractor(self.morph_vocab)

    def extract(self, text: str):
        results = {}

        for match in self.dates_extractor(text):
            d = match.fact
            results['dates'] = results.get('dates', []) + [f"Date(year={d.year}, month={d.month}, day={d.day})"]

        for match in self.money_extractor(text):
            m = match.fact
            results['money'] = results.get('money', []) + [
                f"Money(amount={m.amount}, currency='{m.currency}')"
            ]

            # --- Addresses ---
        match = self.addr_extractor.find(text)
        if match:
            parts = ", ".join([f"AddrPart(value='{p.value}', type='{p.type}')" for p in match.fact.parts])
            results['addr'] = f"Addr(parts=[{parts}])"

        match = self.names_extractor.find(text)
        if match:
            first = match.fact.first
            last = match.fact.last
            middle = getattr(match.fact, "middle", None)
            results['names'] = (
                f"Name(first='{first}', last='{last}', middle={middle})"
            )

        return results

