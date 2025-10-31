# from dataset.load_data import load_data

import json

from dataset.separate_pages import TextExtractor

# load_data()
extractor = TextExtractor()
meta_data = []

meta_data.append(extractor.extract("ballady-i-romanse.epub", 1))
# RAW_DIR = "./dataset/raw"
# path = os.path.join(RAW_DIR, "ballady-i-romanse.epub")
# chapters = extractor.load_file(path)
#
# text = ""
# for chapter in chapters:
#     text += extractor.parse_file(chapter)
#
# pages = extractor.split_pages(text)
#
# for i, page in enumerate(pages):
#     extractor.generate_img(f"./tmp/page_{i}.png", page)

with open("./dataset/clean/meta_data.json", "w") as f:
    json.dump(meta_data, f, indent=2, ensure_ascii=True)
