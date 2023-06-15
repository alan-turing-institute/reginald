import os
import urllib.parse

import requests
from bs4 import BeautifulSoup

CONST_BASE_URL = "https://turing.ac.uk"


def url_to_filename(url):
    parsed_url = urllib.parse.urlparse(url)
    file_path = parsed_url.path
    filename = "_".join(file_path.split("/"))
    sanitized_filename = urllib.parse.unquote(filename)

    # Remove any invalid characters from the filename
    valid_chars = "-_.()abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    sanitized_filename = "".join(c for c in sanitized_filename if c in valid_chars)

    return "data/unused/turingacuk/" + sanitized_filename + ".txt"


def check_string(string):
    contains_https = "https" in string
    contains_turing = "turing.ac.uk" in string

    return contains_https and contains_turing


def get_page(url, depth=0):

    if depth > 5:
        return

    print("Depth: ", depth, " URL: ", url)

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.find_all("a")

    for link in links:
        if link is not None:
            href = link.get("href")
            if href is not None:
                if check_string(href):
                    get_page(href, depth + 1)

                elif href.startswith("/"):
                    get_page(CONST_BASE_URL + href, depth + 1)

    # check if url is already in file and if file exists
    if os.path.isfile("urls.txt"):
        with open("urls.txt", "r") as f:
            if url in f.read():
                print("URL already in file")
                return

    # write to file the url
    with open("urls.txt", "a") as f:
        f.write(url + "\n")

    filename = url_to_filename(url)

    with open(filename, "w", encoding="utf-8") as file:
        paragraphs = soup.find_all("p")
        for paragraph in paragraphs:
            text = paragraph.get_text()
            file.write(text + "\n")


if __name__ == "__main__":

    # create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)

    get_page(CONST_BASE_URL)
