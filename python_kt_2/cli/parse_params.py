import pathlib
import itertools
from typing import Iterable


def get_files_from_path_arguments(*args: pathlib.Path) -> Iterable[pathlib.Path]:
    """Возвращает список путей к текстовым файлам

    Проверяет аргументы на соответствие схеме:
    - один и более файлов,
    - либо ровно одна директория
    """

    files_counter, dirs_counter = 0, 0

    for path in args:
        if path.is_dir():
            dirs_counter += 1
        elif path.is_file():
            files_counter += 1

    if dirs_counter > 1:
        raise Exception("Передано более одной директории")

    if dirs_counter and files_counter:
        raise Exception("Смешанное задание директорий и файлов")

    return args
