import pymorphy2

from utils import get_data_path
from task4 import clean_data, get_lemmas


def load_links(file_path: str) -> dict[int, str]:
    """
    loads links with index
    """
    links = {}
    with open(file_path, "r", encoding="UTF-8") as file:
        for line in file.readlines():
            line_items = line.split()
            links[int(line_items[0])] = line_items[1]
    return links


def normalize(q: str, morph: pymorphy2.MorphAnalyzer) -> list[str]:
    """
    get query string,
    returns lemma list
    """
    words = q.split()
    clean = clean_data(words, morph)
    return get_lemmas(clean, morph)


def read_index(file_path: str) -> dict[str, list[int]]:
    """
    reads inverted lemma list (file_path)
    returns dictionary like {lemma1: [file_index1, file_index2, ...], ...}
    """
    index = {}
    with open(file_path, "r", encoding="UTF-8") as file:
        for line in file.readlines():
            items = line.split()
            index[items[0]] = [int(i) for i in items[1:]]
    return index


def get_indexes(indexes: dict[str, list[int]], lemmas: list[str]) -> list[int]:
    """
    returns indexes of files which contain lemmas
    """
    index = set([i for i in range(1, 290)])
    for lemma in lemmas:
        index = index.intersection(indexes[lemma])
    return list(index)


def get_tf_idf(file_index: int, lemmas: list[str]) -> list[float]:
    """
    reads file with corresponding file_index,
    returns list with tf*idf value
    """
    file_path = f"{get_data_path()}\\tf-idf\\lemmas_{file_index}.txt"
    tf_idf_dict = {}
    with open(file_path, "r", encoding="UTF-8") as file:
        for line in file.readlines():
            items = line.split()
            tf_idf_dict[items[0]] = round(float(items[1]) * float(items[2]), 6)

    result = []
    for lemma in lemmas:
        if lemma in tf_idf_dict:
            result.append(tf_idf_dict[lemma])
    return result


def get_doc_relevance(vector: list[float]) -> float:
    """
    Counts document relevance.
    Measure of document relevance is cosine between vectors.
    """
    if len(vector) == 1:
        return vector[0]
    return round(sum(vector) / sum([i ** 2 for i in vector]) ** 0.5, 6)


def vector_search(lemmas: list[str],
                  all_indexes: dict[str, list[int]],
                  links: dict[int, str]) -> list[list[str, float]]:
    indexes = get_indexes(all_indexes, lemmas)
    result = {}
    for index in indexes:
        result[links[index]] = get_doc_relevance(get_tf_idf(index, lemmas))
    sorted_result = [[k, v] for k, v in sorted(result.items(), key=lambda item: item[1], reverse=True)]
    return sorted_result


def check_query(lemmas: list[str], indexes: dict[str, list[int]]) -> list[str]:
    """
    check if lemmas are in indexes
    """
    not_found = []
    for lemma in lemmas:
        if lemma not in indexes.keys():
            not_found.append(lemma)
    return not_found


if __name__ == "__main__":
    index_path = f"{get_data_path()}//inverted_indexes.txt"
    links_path = f"{get_data_path()}//index.txt"

    morph = pymorphy2.MorphAnalyzer()
    index = read_index(index_path)
    links = load_links(links_path)

    print("Введите запрос:")
    while True:
        query = input()
        normalized_query = normalize(query, morph)
        check = check_query(normalized_query, index)

        if len(check) != 0:
            check_str = " ".join(check)
            print(f"Слова {check_str} не найдены")
        else:
            res = vector_search(normalized_query, index, links)
            print(*res, sep="\n")
