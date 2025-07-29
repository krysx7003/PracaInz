import json

from Metrics import Metrics
from OCR import Ocr, Ocr_name

REFERENCE_PATH = "./dataset/clean/text_data.json"
image_name = "page1.jpg"

with open(REFERENCE_PATH) as file:
    data = json.load(file)

lines = data[0]["text"].split("\n")
text_arr = [line + "\n" for line in lines if line.strip()]
reference_text = "".join(text_arr)

ocrs = {Ocr(Ocr_name.TESSERACT), Ocr(Ocr_name.EASY), Ocr(Ocr_name.DOCTR)}
metrics = Metrics()

print("namef,{cer_res},{wer_res},{bleu_res},{bert_res}")
for ocr in ocrs:
    ocr.recognize_image(image_name)
    candidate_text = ocr.get_text()
    csv_res = metrics.calculate_scores(candidate_text, reference_text)
    print(f"{ocr.name},{csv_res}")
