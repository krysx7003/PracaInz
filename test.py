import json

from tqdm import tqdm

from Metrics import Metrics
from OCR import Ocr, Ocr_name

REFERENCE_PATH = "./dataset/clean/text_data.json"

with open(REFERENCE_PATH) as file:
    data = json.load(file)

ocrs = {Ocr(Ocr_name.TESSERACT), Ocr(Ocr_name.EASY), Ocr(Ocr_name.DOCTR), Ocr(Ocr_name.PADDLE)}
metrics = Metrics()

pages = [item for outer_list in data for item in outer_list]

for page in tqdm(pages, total=len(pages), desc="Pliki do porównania"):
    lines = page["text"].split("\n")
    text_arr = [line + "\n" for line in lines if line.strip()]
    reference_text = "".join(text_arr)

    image_name = page["file_name"]
    res_path = image_name.replace(".jpg", ".json")
    data = []

    with open(res_path, "w") as out:
        for ocr in ocrs:
            ocr.recognize_image(image_name)
            candidate_text = ocr.get_text()
            data.append({"name": ocr.get_name(), "text": candidate_text, "file": image_name})

    json.dump(data, out, indent=4)

    exit()
