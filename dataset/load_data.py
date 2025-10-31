import json
import os
import shutil

import requests

from dataset.book_json import Book
from utils.path import is_valid

AMOUNT = 15
TIMEOUT_MAX = 1
AUTHOR = "adam-mickiewicz"
RAW_DIR = "./dataset/raw"
CACHE_DIR = "./dataset/.cache"


def open_json(path: str) -> list[Book]:
    """Read and deserialize json file.

    Args:
        path (str): Valid json file

    Return:
        list[Book]: List of deserialized json objects
    """
    with open(path, encoding="utf-8") as file:
        data = json.load(file)
        return [Book(**book_data) for book_data in data]


def get_book_list(use_cache: bool) -> None | list[Book]:
    """Makes a request using wolnelektur api listing all books for AUTHOR.

    Args:
        use_cache (bool): If true CACHE_DIR will be searched for {AUTHOR}.json if it exists it will be returned else request will be made and result will be saved.

    Return:
        None: If request failed
        list[Book]: List of deserialized json objects
    """
    url = f"https://wolnelektury.pl/api/authors/{AUTHOR}/books/"
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, f"{AUTHOR}.json")
    if is_valid(path) and use_cache:
        print(f"File {AUTHOR}.json already exists, skipping url call")
        return open_json(path)

    try:
        print(f"Getting: {url}")
        response = requests.get(url, timeout=TIMEOUT_MAX)

        if response.status_code != 200:
            print("Error: ", response.status_code)
            return None

        books_data = response.json()
        if use_cache:
            print(f"Sqving file {AUTHOR}.json")

            data = response.json()
            with open(path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=2, ensure_ascii=False)

        return [Book(**book) for book in books_data]

    except requests.exceptions.RequestException as e:
        print("Error: ", e)
        return None


def extract_name(book: Book) -> str:
    """Splits url of the book to get properly formatted name.

    Args:
        book (Book): Deserialized result of api request

    Returns:
        str: Formatted name.
    """
    url_frags = book.url.split("/")
    name = ""
    if url_frags:
        name = url_frags[-2]

    return name


def get_text_url(name: str) -> None | str:
    """Makes a request using wolnelektur api.

    Args:
        name (str): Name of the book to be searched for.

    Result:
        None: If request failed.
        str: Url of {name}.epub
    """
    url = f"https://wolnelektury.pl/api/books/{name}"
    try:
        print(f"Getting: {url}")
        response = requests.get(url, timeout=TIMEOUT_MAX)

        if response.status_code != 200:
            print("Error: ", response.status_code)
            return None

        if (data := response.json()) and isinstance(data, dict):
            return data.get("epub")

        return None

    except requests.exceptions.RequestException as e:
        print("Error: ", e)
        return None


def scrape(epub_url: str, name: str):
    """Get epub document from wolnelektur and save it to RAW_DIR.

    Args:
        epub_url (str): Url pointing to documnet url.
        name (str): Name of the book.
    """
    print("Downloading url: ", epub_url)
    try:
        print(f"Getting: {epub_url}")
        response = requests.get(epub_url, timeout=TIMEOUT_MAX)

        if response.status_code != 200:
            print("Error: ", response.status_code)

        path = os.path.join(RAW_DIR, f"{name}.epub")

        total_size = int(response.headers.get("content-length", 0))
        print(f"Downloading {total_size} bytes...")

        with open(path, "wb") as file:
            if total_size == 0:
                file.write(response.content)
            else:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            print(f"Progress: {progress:.1f}%", end="\r")

        print(f"\nSuccessfully saved: {path}")

    except requests.exceptions.RequestException as e:
        print("Error: ", e)


def load_data(use_cache: bool = True, purge: bool = False):
    """Load first AMOUNT books from AUTHOR aviable on wolnelektury.pl. Save pdf files in RAW_DIR.

    Args:
        use_cache (bool): If true script will first try to locate file in CACHE_DIR. By default True.
        purge (bool): If true script will clean CACHE_DIR and RAW_DIR on every run.
    """
    if purge:
        print("Purging...")
        shutil.rmtree(RAW_DIR)
        os.makedirs(RAW_DIR)
        shutil.rmtree(CACHE_DIR)
        os.makedirs(CACHE_DIR)

    os.makedirs(RAW_DIR, exist_ok=True)

    json_arr = get_book_list(use_cache)

    if json_arr:
        for i in range(0, AMOUNT):
            name = extract_name(json_arr[i])

            path = os.path.join(RAW_DIR, f"{name}.epub")
            if not use_cache or not is_valid(path, "epub"):
                url = get_text_url(name)
                if url:
                    scrape(url, name)
                else:
                    print("Error: Failed to load url")
            else:
                print(f"File {name}.pdf already exists, skipping download")
    else:
        print(f"Error: The author {AUTHOR} has no books")
