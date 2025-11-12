"""(module) separate_pages."""

import os

import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm

from utils.path import is_valid

RAW_DIR = "./dataset/raw"
CLEAN_DIR = "./dataset/clean"
RES_DIR = "./dataset/ground_truth"
FONTS_DIR = "/usr/share/fonts/truetype/"

# A4 w 300dpi
A4_WIDTH = 2480
A4_HEIGHT = 3508


class TextExtractor:
    margin = 100

    def __init__(self):
        self.set_font()

    def load_file(self, input_path: str):
        book = epub.read_epub(input_path)
        self.book_name = input_path.split("/")[-1]
        items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))

        chapter_items = []
        for item in items:
            if "part" in item.get_name().lower():
                chapter_items.append(item)

        return chapter_items

    def parse_file(self, chapter):
        soup = BeautifulSoup(chapter.get_body_content(), "html.parser")
        target_elements = soup.find_all(
            ["h2", "div"], class_=lambda x: x != "stanza" and x != "stanza-spacer"
        )

        filtered_elements = []
        for element in target_elements:
            if element.name == "h2":
                filtered_elements.append(element)
            elif element.name == "div" and "verse" in element.get("class", []):
                filtered_elements.append(element)

        text_elements = []
        for element in filtered_elements:
            element_text = element.get_text().strip()
            if element_text:
                text_elements.append(element_text)

        text = "\n".join(text_elements)

        return text

    def set_font(self, font_name="ubuntu/Ubuntu-B.ttf", font_size=60):
        font_path = os.path.join(FONTS_DIR, font_name)

        try:
            self.font = ImageFont.truetype(font_path, font_size)
        except:
            print(f"Couldn't set font {font_name}")
            self.font = ImageFont.load_default()

        self.line_height = self.font.getbbox("A")[3] + 10

    def split_pages(self, text: str):
        max_lines = (A4_HEIGHT - 2 * self.margin) // self.line_height

        lines = text.split("\n")
        page_texts = []

        page = ""
        for i, line in enumerate(lines):
            if i % max_lines != 0:
                page += line + "\n"
            else:
                page_texts.append(page)
                page = ""

        if page != "":
            page_texts.append(page)

        return page_texts

    def generate_img(self, output_path, text: str):
        lines = text.split("\n")

        img = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), color="white")
        draw = ImageDraw.Draw(img)

        y_position = self.margin

        for line in lines:
            if y_position + self.line_height < A4_HEIGHT - self.margin:
                draw.text((self.margin, y_position), line, fill="black", font=self.font)
                y_position += self.line_height

        img.save(output_path)  # , dpi=(300, 300)

    def extract(self, path, book_id):
        input_path = os.path.join(RAW_DIR, path)
        if not is_valid(input_path, ".epub"):
            raise Exception(f"The path: {input_path} is invalid")

        chapters = self.load_file(input_path)

        chapter_texts = []
        for chapter in chapters:
            chapter_texts.append(self.parse_file(chapter))

        full_text = "".join(chapter_texts)

        page_texts = self.split_pages(full_text)

        page_id = 0
        for page in tqdm(page_texts, desc="Przetwarzanie stron:", total=len(page_texts)):
            if page.strip() == "":
                continue

            page_file = f"page_{book_id}_{page_id}.png"
            page_path = os.path.join(CLEAN_DIR, page_file)

            res_file = page_file.replace(".png", ".txt")
            res_path = os.path.join(RES_DIR, res_file)
            self.generate_img(page_path, page)

            with open(res_path, "w") as output:
                output.write(page)

            page_id += 1
