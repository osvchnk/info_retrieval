import os
import urllib.parse
import requests
from bs4 import BeautifulSoup
from utils import get_data_path


def get_links(html: BeautifulSoup) -> list:
    """
    :param html:
    :return: list of unique href from html
    """
    links = []
    for link in html.find_all("a"):
        href = link.get("href")
        if href is not None and href.startswith("/wiki/") \
                and not href.endswith(".jpg") and not href.endswith(".gif") \
                and href not in links:
            links.append(href)
    return links


def get_wiki_body_content(url: str) -> BeautifulSoup:
    """
    :param url:
    :return: parsed body content of wiki page
    """
    response = requests.get(url)
    content = response.content.decode()

    soup = BeautifulSoup(content, "html.parser")
    return soup.find("div", {"id": "mw-content-text"})


def append_links(links: list, new_links: [list, str]) -> list:
    """
    :param links: unique link list
    :param new_links: link list to add for
    :return: link list contains unique elements from "links" and "new_links"
    """
    for new_link in new_links:
        if new_link not in links:
            links.append(new_link)
    return links


count = 0
links = ["/wiki/Художник"]
while len(links) < 100:
    url = "https://ru.wikipedia.org" + links[count]
    body_content = get_wiki_body_content(url)
    links = append_links(links, get_links(body_content))
    count += 1


# create folder for files if not exists
data_path = get_data_path()
files_path = data_path + "\\files"
isExist = os.path.exists(files_path)
if not isExist:
    os.makedirs(files_path)


count = 1
index = open(f"{data_path}/index.txt", "w", encoding="UTF-8")
for link in links:
    url = "https://ru.wikipedia.org" + link
    content = requests.get(url).content.decode("UTF-8")
    with open(f"{files_path}/{count}.html", "w", encoding="UTF-8") as file:
        file.write(content)

    index.write(f"{count}   https://ru.wikipedia.org{urllib.parse.unquote(link)}\n")
    count += 1
index.close()

# create html files archive
os.system(f'rar a <files.rar> <{files_path}>')
