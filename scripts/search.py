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
    return index[normal_form]


def search(query: str, index: dict) -> Union[list, None]:
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

    or_split = query.split("|")
    for s in or_split:
        w = s.split()
        not_words = []
        words = []
        for word in w:
            if word.startswith("-"):
                not_words.append(word)
            else:
                words.append(word)

        result = {}    

    pass


if __name__ == "__main__":
    index_path = f"{get_data_path()}//inverted_indexes.txt"

    morph = pymorphy2.MorphAnalyzer()
    index = read_index(index_path)

    search(input(), index)
