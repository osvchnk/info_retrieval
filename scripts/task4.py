import pymorphy2
import os
import math

from collections import Counter
from utils import get_data_path
from task2 import get_russian_words_from_wiki_page, is_func_words


def clean_data(data: list, morph: pymorphy2.MorphAnalyzer) -> list:
    """
    Clean word list data: lower case, remove functional words
    :param data: word list
    :param morph: morphological analyzer for Russian language
    :return: token list
    """
    # lower case
    words = list(map(lambda word: word.lower(), data))
    # remove functional words

    for word in words:
        if is_func_words(word, morph) or len(word) == 1:
            words.remove(word)
    return words


def doc_freq(cur_dict: dict, words: list) -> dict:
    for word in set(words):
        if word in cur_dict:
            cur_dict[word] += 1
        else:
            cur_dict[word] = 1
    return cur_dict


def get_lemmas(tokens: list, morph: pymorphy2.MorphAnalyzer) -> list:
    lemmas = []
    for token in tokens:
        lemma = morph.parse(token)[0].normal_form
        lemmas.append(lemma)
    return lemmas


def get_tokens_lemmas(file_path: str):
    with open(file_path, "r", encoding="UTF-8") as file:
        html = file.read()

        words = get_russian_words_from_wiki_page(html)
        tokens = clean_data(words, morph)
        lemmas = get_lemmas(tokens, morph)
    return tokens, lemmas


def get_tf(words: list) -> dict:
    cnt = Counter()
    for word in words:
        cnt[word] += 1

    total = sum(cnt.values())
    tf_dict = {}
    for word in cnt.keys():
        tf_dict[word] = cnt[word] / total
    return tf_dict


def get_idf(df: int, files_num: int = 289) -> float:
    return math.log(files_num/df)


if __name__ == "__main__":

    files_path = get_data_path() + "\\files"
    lemmas_path = f"{get_data_path()}\\lemmas.txt"
    tokens_path = f"{get_data_path()}\\tokens"

    morph = pymorphy2.MorphAnalyzer()

    # count tokens and lemmas document frequency
    df_token = {}
    df_lemma = {}
    for html_file in os.listdir(files_path):
        file_count = html_file.split(".")[0]
        tokens, lemmas = get_tokens_lemmas(f"{files_path}\\{html_file}")

        df_token = doc_freq(df_token, tokens)
        df_lemma = doc_freq(df_lemma, lemmas)

    for html_file in os.listdir(files_path):
        file_count = html_file.split(".")[0]
        tokens, lemmas = get_tokens_lemmas(f"{files_path}\\{html_file}")

        tf_token = get_tf(tokens)
        tf_lemma = get_tf(lemmas)

        with open(f"{get_data_path()}\\tf-idf\\tokens_{file_count}.txt", "w", encoding="UTF-8") as file:
            for token in tf_token.keys():
                file.write(f"{token} {tf_token[token]} {get_idf(df_token[token])}\n")

        with open(f"{get_data_path()}\\tf-idf\\lemmas_{file_count}.txt", "w", encoding="UTF-8") as file:
            for lemma in tf_lemma:
                file.write(f"{lemma} {tf_lemma[lemma]} {get_idf(df_lemma[lemma])}\n")
