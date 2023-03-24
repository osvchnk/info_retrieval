import pymorphy2
import re
from utils import get_data_path
from bs4 import BeautifulSoup
import os


def get_russian_words_from_wiki_page(html: str) -> list:
    """
    Clean html page data: remove html tags, punctuation
    :param html:
    :return: list of russian words
    """
    soup = BeautifulSoup(html, "html.parser")
    content = str(soup.find("div", {"id": "mw-content-text"}))

    pattern = r"([ёА-я]+[ёА-я-]*)+"
    words = re.findall(pattern, content)
    return words


def is_func_words(word: str, morph: pymorphy2.MorphAnalyzer) -> bool:
    """
    Return info about word is functional or not
    :param word: russian word
    :param morph: morphological analyzer for Russian language
    :return: bool value about word is functional or not
    """
    # междометие, частица, союз, предлог
    func_parts = ['INTJ', 'PRCL', 'CONJ', 'PREP']
    if morph.parse(word)[0].tag.POS in func_parts:
        return True
    return False


def clean_data(data: list, morph: pymorphy2.MorphAnalyzer) -> list:
    """
    Clean word list data: lower case, remove functional words, remove duplicates
    :param data: word list
    :param morph: morphological analyzer for Russian language
    :return: token list
    """
    # lower case, remove duplicates
    words = list(set(map(lambda word: word.lower(), data)))
    # remove functional words
    for word in words:
        if is_func_words(word, morph):
            words.remove(word)
    return words


def create_lemmas_dict(tokens: list, morph: pymorphy2.MorphAnalyzer) -> dict:
    """
    Get tokens, return lemmas
    :param tokens: word list
    :param morph: morphological analyzer for Russian language
    :return: lemmas dictionary like {"normal form": {"word form 1", "word form 2", ...}, ...}
    """
    lemmas = {}
    for token in tokens:
        normal_form = morph.parse(token)[0].normal_form
        if normal_form in lemmas.keys():
            lemmas[normal_form].add(token)
        else:
            lemmas[normal_form] = {token}
    return lemmas


# create folder for files if not exists
def create_folder(name: str, path: str) -> str:
    folder_path = f"{path}\\{name}"
    is_exist = os.path.exists(folder_path)
    if not is_exist:
        os.makedirs(folder_path)
    return folder_path


if __name__ == "__main__":
    tokens_path = create_folder("tokens", get_data_path())
    lemmas_path = create_folder("lemmas", get_data_path())

    files_path = get_data_path() + "\\files"
    morph = pymorphy2.MorphAnalyzer()

    # tokens from all files
    all_tokens = []

    for html_file in os.listdir(files_path):
        file_count = html_file.split(".")[0]
        with open(f"{files_path}\\{html_file}", "r", encoding="UTF-8") as file:
            html = file.read()

            words = get_russian_words_from_wiki_page(html)
            tokens = clean_data(words, morph)

        all_tokens += tokens

        lemmas_dict = create_lemmas_dict(tokens, morph)

        # create tokens file
        with open(f"{tokens_path}\\tokens_{file_count}.txt", "w", encoding="UTF-8") as file:
            for token in tokens:
                file.write(f"{token}\n")

        # create lemmas file
        with open(f"{lemmas_path}\\lemmas_{file_count}.txt", "w", encoding="UTF-8") as file:
            for lemma in lemmas_dict.keys():
                values = ' '.join(value for value in lemmas_dict[lemma])
                file.write(f"{lemma}: {values}\n")


    # remove dublicates
    all_tokens = list(set(all_tokens))

    # lemmas from all files
    all_lemmas = create_lemmas_dict(all_tokens, morph)

    # create file with tokens from all files
    with open(f"{get_data_path()}\\tokens.txt", "w", encoding="UTF-8") as file:
        for token in all_tokens:
            file.write(f"{token}\n")

    # create file with lemmas from all files
    with open(f"{get_data_path()}\\lemmas.txt", "w", encoding="UTF-8") as file:
        for lemma in all_lemmas:
            values = ' '.join(value for value in all_lemmas[lemma])
            file.write(f"{lemma}: {values}\n")

