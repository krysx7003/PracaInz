import json
import os

import pandas as pd
from tqdm import tqdm

from Metrics import Metrics

metrics = Metrics()

HEADER = "cer_res,wer_res,time\n"
RESULT_DIR = "./results"
DOCTR_RES = "./results/doctr_result.csv"
TES_RES = "./results/tesseract_result.csv"
PADDLE_RES = "./results/paddle_res.csv"
EASY_RES = "./results/easy_result.csv"


def compare_results(dir_name, dataset):
    doctr_results = ""
    tesseract_results = ""
    paddle_results = ""
    easyocr_results = ""

    files = os.listdir(dir_name)
    for file in tqdm(files, total=len(files), desc=f"Files in {dataset}"):
        file_path = os.path.join(dir_name, file)
        with open(file_path) as f:
            data = json.load(f)

        ref_text = data["reference_text"]
        results = data["results"]
        for res in results:
            name = res["name"]
            candidate_text = res["text"]
            time = res["time"]

            scores = f"{metrics.calculate_scores(candidate_text, ref_text)},{time}\n"

            if name == "doctr":
                doctr_results += scores
            elif name == "pytesseract":
                tesseract_results += scores
            elif name == "paddle":
                paddle_results += scores
            elif name == "easyocr":
                easyocr_results += scores

    doctr_file = DOCTR_RES.replace(".csv", f"{dataset}.csv")
    with open(doctr_file, "a") as f:
        f.write(HEADER)
        f.write(doctr_results)

    tesseract_file = TES_RES.replace(".csv", f"{dataset}.csv")
    with open(tesseract_file, "a") as f:
        f.write(HEADER)
        f.write(tesseract_results)

    paddle_file = PADDLE_RES.replace(".csv", f"{dataset}.csv")
    with open(paddle_file, "a") as f:
        f.write(HEADER)
        f.write(paddle_results)

    easy_file = EASY_RES.replace(".csv", f"{dataset}.csv")
    with open(easy_file, "a") as f:
        f.write(HEADER)
        f.write(easyocr_results)


def compile_data(end_str):
    files = os.listdir(RESULT_DIR)
    rows = []

    print(end_str)
    for file in files:
        if not file.endswith(end_str):
            continue

        file_path = os.path.join(RESULT_DIR, file)
        data = pd.read_csv(file_path)
        name = file.split("_")[0]

        row = pd.DataFrame(
            {
                "name": [name],
                "cer_res": [data["cer_res"].mean()],
                "wer_res": [data["wer_res"].mean()],
                "time": [data["time"].mean()],
            }
        )
        rows.append(row)

    rows.sort()
    final_results = pd.concat(rows, ignore_index=True)
    print(final_results)


compile_data("_IAM.csv")
compile_data("_IAM_pl.csv")
compile_data("_obd.csv")
compile_data("_obd_pl.csv")
compile_data("_pobd.csv")
