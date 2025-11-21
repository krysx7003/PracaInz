import os

# from dataset.load_data import load_data
from dataset.separate_pages import TextExtractor

# load_data()
extractor = TextExtractor()
files = os.listdir("./dataset/raw")
fonts = os.listdir("./fonts")

i = 0
for file in files:
    if not file.endswith(".epub"):
        continue

    for font in fonts:
        extractor.set_font(font)
        extractor.extract(file, i)
    i += 1
