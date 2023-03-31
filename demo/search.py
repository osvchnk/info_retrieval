import pymorphy2

from scripts.task5 import read_index, load_links, normalize, check_query, vector_search
from scripts.utils import get_data_path

index_path = f"{get_data_path()}//inverted_indexes.txt"
links_path = f"{get_data_path()}//index.txt"

morph = pymorphy2.MorphAnalyzer()
index = read_index(index_path)
links = load_links(links_path)


def search(query: str):
    normalized_query = normalize(query, morph)
    check = check_query(normalized_query, index)

    if len(check) != 0:
        return []
    else:
        return vector_search(normalized_query, index, links)
