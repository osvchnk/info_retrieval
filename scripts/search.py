from typing import Union

import pymorphy2

from utils import get_data_path


def read_index(index_path: str) -> dict:
    """
    Read file with indexes and create dictionary
    :param index_path: file path
    :return: dictionary with indexes
    """
    index = {}
    with open(index_path, "r", encoding="UTF-8") as file:
        for line in file.readlines():
            line_values = line.split()
            index[line_values[0]] = {int(i) for i in line_values[1:]}
    return index


def get_index(word: str, index: dict) -> set:
    normal_form = morph.parse(word)[0].normal_form
    try:
        return index[normal_form]
    except:
        print(f"there is no such word like {word}")


def search(query: str, index: dict) -> Union[set, None]:
    """
    " " - AND
    "-" - NOT
    "|" - OR
    :param query: query string
    :return: index list
    """
    if query.isspace():
        print("empty query")
        return None

    all_files_index = {i for i in range(1, 290)}
    result = all_files_index
    or_split = query.split("|")
    for s in or_split:
        words = s.split()

        for word in words:
            if word.startswith("-"):
                result.difference(get_index(word[1:], index))
            else:
                result.intersection_update(get_index(word, index))

    return result


if __name__ == "__main__":
    index_path = f"{get_data_path()}//inverted_indexes.txt"

    morph = pymorphy2.MorphAnalyzer()
    index = read_index(index_path)

    while True:
        print(search(input(), index))
