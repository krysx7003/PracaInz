import json
import os

from find_chars import clean_text
from pdf2image import convert_from_path
from pypdf import PdfReader

RAW_PATH = "./raw"
CLEAN_PATH = "./clean"
page_total: int = 0
json_arr: list[dict[str, object]] = []


def parse_pdf(file: str):
    global page_total
    path = os.path.join(RAW_PATH, file)
    reader = PdfReader(path)
    size = len(reader.pages)
    print(f"File {file} has: {size} pages")

    for page_num, page in enumerate(reader.pages[1:], start=1):
        page_file = f"page{page_total}.jpg"
        text = page.extract_text()
        page_data = {
            "file_name": page_file,
            "book_name": file,
            "page": page_num,
            "text": clean_text(text),
        }

        json_arr.append(page_data)

    images = convert_from_path(path)
    for image in enumerate(images):
        page_file = f"page{page_total}.jpg"
        page_total += 1
        page_path = os.path.join(CLEAN_PATH, page_file)
        image.save(page_path, "JPEG")


def open_from_raw():
    raw_dir = os.listdir(RAW_PATH)
    for file in raw_dir:
        parse_pdf(file)

    path = os.path.join(CLEAN_PATH, "text_data.json")
    with open(path, "w") as f:
        json.dump(json_arr, f, indent=2, ensure_ascii=True)
