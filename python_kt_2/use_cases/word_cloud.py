from typing import Literal
from wordcloud import WordCloud
from ..core.preprocess import filter_stopwords

def word_cloud(
    text: str, 
    preprocess_mode: Literal["basic", "stemming", "lemmatization"] = "stemming" 
):
    """Построение облака важных слов.

    Получает текст, выполняет базовую предобработку (разбивает на слова, 
    убирает пунктуацию и пробельные символы, фильтрует стоп-слова. 

    При указании режима предобработки, отличного от базового, нормализует 
    (стеммингом либо лемматизацией). 

    Возможности:
    - сохранение результата (изображения) в файл
    - три уровня предобработки (базовый, стемминг, лемматизация).
    """
    
    if preprocess_mode == "basic":
        return WordCloud().generate(text).to_file()

    return