from typing import Literal
from ..core.preprocess import filter_stopwords, clean_words
from python_kt_2.core.tokenize import tokenize_text


def _count_words(words: list[str]) -> dict[str, int]:
    """Подсчет количества вхождений слов.
    """
    counter = {}
    for word in words:
        if word in counter:
            counter[word] += 1
        else:
            counter[word] = 1

    # TODO реализуйте подсчет слов

    return counter

def _sort_by_count(item: tuple[str, int]) -> int:
    """Сортирует по количеству вхождений,
    от большего к меньшему
    """

    # TODO исправьте ошибку
    return -item[1]


def top_words(
    text: str, 
    normalize_mode: Literal["stemming", "lemmatization"] = "stemming", 
) -> list[tuple[str, int]]:

    """Подсчет топ-N-важных слов.

    Получает текст, разбивает на слова, убирает пунктуацию и пробельные символы,
    фильтрует стоп-слова, нормализует (либо стемминг, либо лемматизация),
    подсчитывает и возвращает список кортежей для топ-N-важных слов.
    """

    # TODO допишите / исправьте ошибки

    initial_words = tokenize_text(text)["words"]
    words_after_clean = clean_words(initial_words)
    words_after_filter = filter_stopwords(words_after_clean)

    word_counts = _count_words(words_after_filter)

    return sorted(word_counts.items(), key=_sort_by_count)
    # return sorted(_count_words(words_after_filter).items(), key=_sort_by_count)
    