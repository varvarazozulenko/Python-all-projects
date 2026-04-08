import re
import pathlib

from ..core.types import TextStats, SymbolStats, Tokens, TokensStats


def stats(text: str, pos: bool = False) -> TextStats:
    """Функция для подсчета статистик.

    Args:
        text: текст для расчета статистик
        pos: опция, добавляет аналитику по частям речи

    Returns:
        Статистика, сгруппированная по токенам, символам и,
        опционально, морфологическим характеристикам

        Например, для строки `\tПроверка!\nНовая строка` это
        будет:
        {
            "tokens": {
                "paragraphs": 2,
                "sentences": 2,
                "words": 3,
            },
            "symbols": {
                "alphas": {
                    "quantity": 19,
                    "percent": 82.61
                },
                "digits": {
                    "quantity": 0,
                    "percent": 0.00
                },
                "spaces": {
                    "quantity": 3,
                    "percent": 13.04
                },
                "punctuation": {
                    "quantity": 1,
                    "percent": 4.35
                }
            }
        }

    """

    return {"tokens": _get_tokens_stats(text), "symbols": _get_symbols_stats(text)}


def _get_symbols_stats(text: str) -> SymbolStats:
    """Посимвольная статистика (количество и процент)."""

    count_alphas = 0
    count_digits = 0
    count_spaces = 0
    count_punctuation = 0

    for symbol in text:
        if symbol.isalpha():
            count_alphas += 1
        elif symbol.isdigit():
            count_digits += 1
        elif symbol.isspace():
            count_spaces += 1
        else:
            count_punctuation += 1

    total = len(text)

    def percent(count):
        if total == 0:
            return 0.0
        return round(count / total * 100, 2)

    return {
        "alphas": {"quantity": count_alphas, "percent": percent(count_alphas)},
        "digits": {"quantity": count_digits, "percent": percent(count_digits)},
        "spaces": {"quantity": count_spaces, "percent": percent(count_spaces)},
        "punctuation": {"quantity": count_punctuation, "percent":percent(count_punctuation)}
    }


def _get_tokens_stats(text: str) -> TokensStats:
    """Подсчет количества токенов."""
    paragraphs = [p for p in text.split('\n\n') if p.strip()]
    paragraphs_count = len(paragraphs)

    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    sentences_count = len(sentences)

    words = re.findall(r'[а-яА-Яa-zA-Z0-9]+', text)
    words_count = len(words)

    return {
        "paragraphs": paragraphs_count,
        "sentences": sentences_count,
        "words": words_count
    }

def _get_pos_stats(text: str):
    """Подсчет pos-аналитики (статистики по частям речи)"""


