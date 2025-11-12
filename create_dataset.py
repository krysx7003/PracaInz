from dataset.load_data import load_data
from dataset.separate_pages import TextExtractor

load_data()
extractor = TextExtractor()

extractor.extract("ballady-i-romanse.epub", 1)
