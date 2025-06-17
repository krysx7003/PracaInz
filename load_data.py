# pylint: disable=missing-module-docstring,missing-function-docstring
import json
import os

import requests

from book_json import BookJson

AMOUNT = 15
TIMEOUT_MAX = 1
AUTHOR = "adam-mickiewicz"
RAW_PATH = "dataset/raw"
CACHE_PATH = "dataset/.cache"
CACHE = True
OVERIDE = False


def is_cached(path: str) -> bool:
    return os.path.exists(path)


def open_json(path: str) -> None | list[BookJson]:
    with open(path, encoding="utf-8") as file:
        data = json.load(file)
        return [BookJson(**book_data) for book_data in data]


def save_json(path: str, response: requests.Response):
    data = response.json()
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def get_book_list() -> None | list[BookJson]:
    url = f"https://wolnelektury.pl/api/authors/{AUTHOR}/books/"
    path = os.path.join(CACHE_PATH, f"{AUTHOR}.json")
    if is_cached(path) and CACHE:
        print(f"File {AUTHOR}.json already exists, skipping url call")
        return open_json(path)

    try:
        print(f"Getting: {url}")
        response = requests.get(url, timeout=TIMEOUT_MAX)

        if response.status_code != 200:
            print("Error: ", response.status_code)
            return None

        books_data = response.json()
        if CACHE:
            print(f"Sqving file {AUTHOR}.json")
            save_json(path, response)

        return [BookJson(**book) for book in books_data]

    except requests.exceptions.RequestException as e:
        print("Error: ", e)
        return None


def extract_name(book: BookJson):
    url_frags = book.url.split("/")
    name = ""
    if url_frags:
        name = url_frags[-2]

    return name


def get_pdf_url(name: str) -> None | str:
    url = f"https://wolnelektury.pl/api/books/{name}"
    try:
        print(f"Getting: {url}")
        response = requests.get(url, timeout=TIMEOUT_MAX)

        if response.status_code != 200:
            print("Error: ", response.status_code)
            return None

        if (data := response.json()) and isinstance(data, dict):
            return data.get("pdf")

        return None

    except requests.exceptions.RequestException as e:
        print("Error: ", e)
        return None


def scrape(pdf_url: str, name: str):
    print("Downloading url: ", pdf_url)
    try:
        print(f"Getting: {pdf_url}")
        response = requests.get(pdf_url, timeout=TIMEOUT_MAX)

        if response.status_code != 200:
            print("Error: ", response.status_code)

        path = os.path.join(RAW_PATH, f"{name}.pdf")
        with open(path, "wb") as file:
            file.write(response.content)

    except requests.exceptions.RequestException as e:
        print("Error: ", e)


def main():
    json_arr = get_book_list()
    if json_arr:
        for i in range(0, AMOUNT):
            name = extract_name(json_arr[i])

            path = os.path.join(RAW_PATH, f"{name}.pdf")
            if OVERIDE or not is_cached(path):
                url = get_pdf_url(name)
                if url:
                    scrape(url, name)
                else:
                    print("Error: Failed to load url")
            else:
                print(f"File {name}.pdf already exists, skipping download")
    else:
        print(f"Error: The author {AUTHOR} has no books")


if __name__ == "__main__":
    main()
