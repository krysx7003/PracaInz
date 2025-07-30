import json

from tqdm import tqdm

from Metrics import Metrics
from OCR import Ocr, Ocr_name

REFERENCE_PATH = "./dataset/clean/text_data.json"
EASY_RES = "./easy_result.csv"
DOCTR_RES = "./doctr_result.csv"
TES_RES = "./tesseract_result.csv"
HEADER = "name,{cer_res},{wer_res},{bleu_res},{bert_res}\n"

with open(REFERENCE_PATH) as file:
    data = json.load(file)

ocrs = {Ocr(Ocr_name.TESSERACT), Ocr(Ocr_name.EASY), Ocr(Ocr_name.DOCTR)}
metrics = Metrics()

pages = [item for outer_list in data for item in outer_list]

with open(EASY_RES, "w") as easy_f, open(DOCTR_RES, "w") as doctr_f, open(TES_RES, "w") as tes_f:
    easy_f.write(HEADER)
    doctr_f.write(HEADER)
    tes_f.write(HEADER)

for page in tqdm(pages, total=len(pages), desc="Pliki do porównania"):
    lines = page["text"].split("\n")
    text_arr = [line + "\n" for line in lines if line.strip()]
    reference_text = "".join(text_arr)

    image_name = page["file_name"]
    for ocr in ocrs:
        ocr.recognize_image(image_name)
        candidate_text = ocr.get_text()
        csv_res = metrics.calculate_scores(candidate_text, reference_text)
        ocr.append_csv(csv_res)
