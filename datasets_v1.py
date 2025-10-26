import json
import os

from OCR import Ocr, Ocr_name

ocrs = {Ocr(Ocr_name.TESSERACT), Ocr(Ocr_name.EASY), Ocr(Ocr_name.DOCTR), Ocr(Ocr_name.PADDLE)}

image_name = "a01-000u.png"
path = "IAM/data/000/"

image_path = os.path.join(path, image_name)
text_file = image_name.replace(".png", ".json")
ref_path = image_name.replace(".png", "_ref.txt")

data = {"file": image_name, "results": []}

with open(text_file, "w") as out, open(ref_path) as ref_file:
    ref_text = ref_file.read()
    for ocr in ocrs:
        ocr.recognize_image(image_path)
        candidate_text = ocr.get_text()
        data["results"].append({"name": ocr.get_name(), "text": candidate_text})

    json.dump(data, out, indent=4)
