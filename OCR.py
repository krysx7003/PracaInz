"""Module (OCR)."""

import os
from enum import StrEnum

import easyocr
import pytesseract
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from PIL import Image

IMAGE_PATH = "./dataset"


class Ocr_name(StrEnum):
    """Enum containing all supported ocr models."""

    TESSERACT = "pytesseract"
    EASY = "easyocr"
    DOCTR = "doctr"


class Ocr:
    """Wraper class to handle different needs of ocr models.

    Attributes:
        name (str): Chosen ocr model.
        plain_text (str): Raw output of ocr model.
        text (str): Formatted plain_text.
        reader (Reader): Preinitialized easyocr.Reader. Options ["pl"]
        model (OCRPredictor): Preinitialized doctor.models.OCRPredictor. Options pretrained=True
        easy_text (list[str]): Raw output of easyocr.
    """

    plain_text: str
    text: str
    name: str

    def __init__(self, name: str):
        """Initializes the Ocr.name var. If it is possible the ocr model is initialized.

        Args:
            name (str): Name of the ocr to be used (name must be included in Ocr_name).
        """
        if name in Ocr_name:
            self.name = name
        else:
            raise Exception(f"The ocr: {name} is not supported")

        if self.name == Ocr_name.EASY:
            self.reader = easyocr.Reader(["pl"])

        if self.name == Ocr_name.DOCTR:
            self.model = ocr_predictor(pretrained=True)

    def is_valid(self, path: str, file_type: str = "jpg"):
        """Checks if file on the {path} exists, is a file and is of type {file_type}.

        Args:
            path (str): Path of the file to check.
            file_type (str): File type of file. Needs to work with doctr.io.DocumentFile and PIL.Image. By default "jpg".

        Returns:
            Boolean: True if all conditions are met, otherwise False.
        """
        if not os.path.exists(path):
            return False
        if not os.path.isfile(path):
            return False
        if not path.endswith(file_type):
            return False

        return True

    def recognize_image(self, image_name: str, input_dir: str = "clean"):
        """Uses one of the supported ocr models (specified by var self.name) to read content of the file.

        Args:
            image_name (str): Name of the file to be read(needs to be in ./dataset/{input_dir} directory).
            input_dir (str): Subdirectory of ./dataset containing file {image_name}. By default "clean".

        Raises:
            Exception:  If ./datset/{input_dir}/{image_name} is invalid.
        """
        image_path = os.path.join(IMAGE_PATH, input_dir, image_name)
        if not self.is_valid(image_path):
            raise Exception(f"The path: {image_path} is invalid")

        if self.name == Ocr_name.TESSERACT:
            image = Image.open(image_path)
            self.plain_text = pytesseract.image_to_string(image, lang="pol")

        if self.name == Ocr_name.EASY:
            image = Image.open(image_path)
            self.easy_text = self.reader.readtext(image, detail=0)

        if self.name == Ocr_name.DOCTR:
            img = DocumentFile.from_images(image_path)
            result = self.model(img)
            self.plain_text = result.render()

    def format_text(self):
        """Formats Ocr.plain_text to remove stanza breaks."""
        if self.name == Ocr_name.TESSERACT:
            lines = self.plain_text.split("\n")
            text_arr = [line + "\n" for line in lines if line.strip()]
            self.text = "".join(text_arr)

        if self.name == Ocr_name.EASY:
            text_arr = [line + "\n" for line in self.easy_text]
            self.text = "".join(text_arr)

        if self.name == Ocr_name.DOCTR:
            self.text = self.plain_text

    def get_text(self) -> str:
        """.

        Returns:
            str: Output of ocr formatted using Ocr.format_text.
        """
        self.format_text()
        return self.text
