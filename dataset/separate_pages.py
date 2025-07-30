"""(module) separate_pages."""

import json
import os

from pdf2image import convert_from_path
from pypdf import PdfReader

from dataset.find_chars import clean_text
from utils.path import is_valid

RAW_DIR = "./dataset/raw"
CLEAN_DIR = "./dataset/clean"
book_id: int = 0


def read_pdf(file_name: str, input_path: str) -> list[dict[str, object]]:
    """Reads content of each page in .pdf file.

    Args:
        file_name (str): Name of the file in RAW_DIR dir to be proccesed.
        input_path (str): Valid path the file is at,

    Returns:
        list[dict[str, object]]: List of json objects structured like {"file_name","book_name","book_id","page","text"}
    """
    reader = PdfReader(input_path)
    size = len(reader.pages)
    print(f"File {file_name} has: {size} pages")

    json_arr: list[dict[str, object]] = []
    for page_num, page in enumerate(reader.pages[1:], start=1):
        page_file = f"page{page_num}_{book_id}.jpg"
        text = page.extract_text()
        page_data = {
            "file_name": page_file,
            "book_name": file_name,
            "book_id": book_id,
            "page": page_num,
            "text": clean_text(text),
        }

        json_arr.append(page_data)

    return json_arr


def split_pdf(input_path: str):
    """Splits file_name into separate pages and saves each one in CLEAN_DIR.

    Args:
        file_name (str): Name of the file in RAW_DIR dir to be proccesed.
        input_path (str): Valid path the file is at,
    """
    images = convert_from_path(input_path)
    for page_num, image in enumerate(images[1:]):
        page_file = f"page{page_num}_{book_id}.jpg"
        page_path = os.path.join(CLEAN_DIR, page_file)
        image.save(page_path, "JPEG")


def open_from_raw():
    """For each file in RAW_DIR runs parse_pdf and saves result to CLEAN_DIR. Finally saves conten of json_arr in CLEAN_DIR/text_data.json.

    Raises:
        Exception: If file_name is invalid
    """
    global book_id

    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(CLEAN_DIR, exist_ok=True)
    files = os.listdir(RAW_DIR)

    json_arr = []
    for file in files:
        input_path = os.path.join(RAW_DIR, file)
        if not is_valid(input_path, ".pdf"):
            raise Exception(f"The path: {input_path} is invalid")

        json_arr.append(read_pdf(file, input_path))
        split_pdf(input_path)
        book_id += 1

    out_path = os.path.join(CLEAN_DIR, "text_data.json")
    with open(out_path, "w") as f:
        json.dump(json_arr, f, indent=2, ensure_ascii=True)
