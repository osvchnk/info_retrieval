import os
import pymorphy2
from utils import get_data_path


def get_lemmas(lemmas_path: str) -> dict:
    """
    Read lemmas from file and create dictionary where lemmas are keys, set() is value.
    :param lemmas_path: lemmas file path
    :return: dict like {lemma1: set(), lemma2: set(), ...}
    """
    lemmas = {}
    # add normal forms from lemmas.txt
    with open(lemmas_path, "r", encoding="UTF-8") as file:
        for line in file.readlines():
            lemmas[line.split(":")[0]] = set()
    return lemmas


def create_inverted_indexes(lemmas: dict, tokens_path: str) -> dict:
    """
    Read files with tokens
    and add file number where token from to lemmas dictionary value.
    :param lemmas: dictionary with lemmas
    :param tokens_path: tokens file path
    :return: inverted indexes dictionary
    """
    for token_file in os.listdir(tokens_path):
        file_count = token_file.split("_")[1].split(".")[0]
        with open(f"{tokens_path}\\{token_file}", "r", encoding="UTF-8") as file:
            tokens = file.read().split()
        for token in tokens:
            normal_form = morph.parse(token)[0].normal_form
            lemmas[normal_form].add(file_count)
    return lemmas


def write_indexes(path: str):
    """
    Create file with inverted indexes
    :param: file path
    """
    with open(path, "w", encoding="UTF-8") as file:
        for item in inverted_indexes.keys():
            values = " ".join(value for value in inverted_indexes[item])
            file.write(f"{item} {values}\n")


if __name__ == "__main__":
    lemmas_path = f"{get_data_path()}\\lemmas.txt"
    tokens_path = f"{get_data_path()}\\tokens"
    indexes_path = f"{get_data_path()}\\inverted_indexes.txt"

    morph = pymorphy2.MorphAnalyzer()

    lemmas_dict = get_lemmas(lemmas_path)
    inverted_indexes = create_inverted_indexes(lemmas_dict, tokens_path)
    write_indexes(indexes_path)

