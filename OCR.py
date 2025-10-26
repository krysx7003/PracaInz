"""Module (OCR)."""

import os
from enum import StrEnum

import easyocr
import pytesseract
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from paddleocr import PaddleOCR
from PIL import Image

from utils.path import is_valid

IMAGE_PATH = "./dataset"

EASY_RES = "./results/easy_result.csv"
DOCTR_RES = "./results/doctr_result.csv"
TES_RES = "./results/tesseract_result.csv"
PADDLE_RES = "./results/paddle_res.csv"

HEADER = "name,{cer_res},{wer_res}\n"


class Ocr_name(StrEnum):
    """Enum containing all supported ocr models."""

    TESSERACT = "pytesseract"
    EASY = "easyocr"
    DOCTR = "doctr"
    PADDLE = "paddle"


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

    result_file: str
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

        if self.name == Ocr_name.TESSERACT:
            self.result_file = TES_RES

        if self.name == Ocr_name.EASY:
            self.result_file = EASY_RES
            self.reader = easyocr.Reader(["pl"])

        if self.name == Ocr_name.DOCTR:
            self.result_file = DOCTR_RES
            self.model = ocr_predictor(
                det_arch="db_resnet50", reco_arch="crnn_vgg16_bn", pretrained=True
            )

        if self.name == Ocr_name.PADDLE:
            self.result_file = PADDLE_RES
            self.paddle = PaddleOCR(
                lang="pl",
                use_doc_orientation_classify=False,
                use_doc_unwarping=False,
                use_textline_orientation=False,
            )

        with open(self.result_file, "w") as f:
            f.write(HEADER)

    def append_csv(self, line: str):
        """Appends {line} to self.result_file.

        Args:
            line (str): Csv formatted line.
        """
        with open(self.result_file, "a") as f:
            f.write(line + "\n")

    def recognize_image(self, image_name: str, input_dir: str = "clean"):
        """Uses one of the supported ocr models (specified by var self.name) to read content of the file.

        Args:
            image_name (str): Name of the file to be read(needs to be in ./dataset/{input_dir} directory).
            input_dir (str): Subdirectory of ./dataset containing file {image_name}. By default "clean".

        Raises:
            Exception:  If ./datset/{input_dir}/{image_name} is invalid.
        """
        image_path = os.path.join(IMAGE_PATH, input_dir, image_name)
        # image_name

        if not is_valid(image_path):
            raise Exception(f"The path: {image_path} is invalid")

        if self.name == Ocr_name.TESSERACT:
            image = Image.open(image_path)
            self.plain_text = pytesseract.image_to_string(image, lang="pol")

        if self.name == Ocr_name.EASY:
            self.easy_text = self.reader.readtext(image_path, paragraph=False)

        if self.name == Ocr_name.DOCTR:
            img = DocumentFile.from_images(image_path)
            self.result = self.model(img)

        if self.name == Ocr_name.PADDLE:
            self.result = self.paddle.predict(input=image_path)

    def format_text(self):
        """Formats Ocr.plain_text to remove stanza breaks."""
        if self.name == Ocr_name.TESSERACT:
            lines = self.plain_text.split("\n")
            text_arr = [line + "\n" for line in lines if line.strip()]
            self.text = "".join(text_arr)

        if self.name == Ocr_name.EASY:
            sorted_results = sorted(self.easy_text, key=lambda x: x[0][0][1])

            lines = []
            current_line = []
            current_y = None
            y_threshold = 20

            for bbox, text, confidence in sorted_results:
                y_pos = bbox[0][1]

                if current_y is None:
                    current_y = y_pos
                    current_line.append(text)
                elif abs(y_pos - current_y) <= y_threshold:
                    current_line.append(text)
                else:
                    lines.append(" ".join(current_line))
                    current_line = [text]
                    current_y = y_pos

            if current_line:
                lines.append(" ".join(current_line))

            self.text = "\n".join(lines)

        if self.name == Ocr_name.DOCTR:
            self.text = self.result.render()

        if self.name == Ocr_name.PADDLE:
            text_lines = []
            for res in self.result:
                if "rec_texts" in res:
                    text_lines.extend(res["rec_texts"])

            self.text = "\n".join(text_lines)

    def get_text(self) -> str:
        """.

        Returns:
            str: Output of ocr formatted using Ocr.format_text.
        """
        self.format_text()
        return self.text

    def get_name(self) -> str:
        """ """
        return self.name
