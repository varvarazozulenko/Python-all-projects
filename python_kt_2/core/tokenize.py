import re
from .types import Tokens

def _get_words(text: str) -> list[str]:
    """Разбиение на слова (без обработки)"""
    words = re.findall(r'[а-яА-Яa-zA-Z0-9]+', text)
    return words

    # TODO: исправьте регулярку

def _get_paragraphs(text: str) -> list[str]:
        return text.split('\n\n')

def _get_sentences(text: str) -> list[str]:
        sentences = re.split(r'[.!?…]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        return sentences

def tokenize_text(text: str) -> Tokens:

    """Разбиение текста на токены.

    Разбиение текста на токены:
    - параграфы (абзацы),
    - предложения,
    - слова
    """

    # TODO допишите функции _get_paragraphs, _get_sentences
    return {
        "paragraphs": _get_paragraphs(text),
        "sentences": _get_sentences(text),
        "words": _get_words(text),
    }

