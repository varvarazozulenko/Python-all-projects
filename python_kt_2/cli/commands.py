import pathlib
from time import localtime, strftime
from typing import Literal, Annotated

import typer

import python_kt_2.use_cases as use_cases
from .parse_params import get_files_from_path_arguments

app = typer.Typer()


@app.command()
def stats(
    input: Annotated[
        pathlib.Path,
        typer.Argument(
            help="Путь к файлу для анализа", exists=True, readable=True, file_okay=True
        ),
    ],
    output: Annotated[
        pathlib.Path | None,
        typer.Option(
            "--output", "-o", help="Путь к файлу для сохранения отчета", writable=True
        ),
    ] = None,
    pos: Annotated[
        bool, typer.Option(help="Добавить к отчету анализ частей речи")
    ] = False,
):
    """Статистика по текстовому файлу.

    Возможности:
    - подсчёт абзацев, предложений, слов,
    - количество и процент символов по типам,
    - опционально, статистика по частям речи.

    Два формата вывода:
    - форматированный консольный вывод,
    - неформатированный вывод в файл.
    """

    text = input.read_text(encoding="utf-8")
    result = use_cases.stats(text)

    print(result)


@app.command("word-cloud")
def word_cloud(
    input: Annotated[
        pathlib.Path,
        typer.Argument(help="Исходный текстовый файл", exists=True, readable=True),
    ],
    output: pathlib.Path | None = pathlib.Path("/") / f"{strftime('%H_%M_$S', localtime())}_output.png",
    preprocess_mode: Literal["basic", "full"] = "basic",
):
    """Построение облака важных слов.

    Построение облака важных слов

    Возможности:
    - сохранение результата (изображения) в файл
    - два уровня предобработки (базовый, полный).
    """

    text = input.read_text(encoding="utf-8")
    result = use_cases.word_cloud(text, preprocess_mode)

    print(result)



@app.command(name="top-words")
def top_words(
    input: Annotated[
        pathlib.Path,
        typer.Argument(help="Исходный текстовый файл", exists=True, readable=True),
    ],
    output: pathlib.Path | None = None,
    normalize_mode: Literal["stemming", "lemmatization"] = "stemming",
):
    """Подсчет топ-N-важных слов.

    Подсчет топ-N-важных слов

    Возможности:
    - указание N слов,
    - базовая предобработка (фильтр по стоп-словам, токенизация),
    - два типа нормализации (стемминг, лемматизация),
    - запись результатов в файл.

    """

    text = input.read_text(encoding="utf-8")
    result = use_cases.top_words(text, normalize_mode, pos)

    print(result)

