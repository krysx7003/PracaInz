import os

# from dataset.load_data import load_data
from dataset.separate_pages import TextExtractor

# load_data()
extractor = TextExtractor()
files = os.listdir("./dataset/raw")

i = 0
for file in files:
    if not file.endswith(".epub"):
        continue

    extractor.extract(file, i)
    i += 1
