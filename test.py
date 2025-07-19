import easyocr
import keras_ocr
import pytesseract
from PIL import Image

path = "/home/napnap/Downloads/page1-1.jpg"
image = Image.open(path)
print(pytesseract.get_languages(config=""))
print(pytesseract.image_to_string(image, lang="pol"))

reader = easyocr.Reader(["pl"])
print(reader.readtext(image, detail=0))

pipeline = keras_ocr.pipeline.Pipeline()
prediction_groups = pipeline.recognize(keras_ocr.tools.read(path))
