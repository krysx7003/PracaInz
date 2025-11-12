import json
import os
import time

from tqdm import tqdm

from OCR import Ocr, Ocr_name
from utils.path import is_valid_dir

IAM_PATH = "./IAM/data/000"
IAM_REF = "./IAM/data/000_ground_truth"

OBD_PATH = "./old-books-dataset/300dpi/tiff"
OBD_REF = "./old-books-dataset/groundtruth"

POBD_PATH = "./dataset/clean"
POBD_REF = "./dataset/ground_truth"

RESULT_DIR = "./results"

ocrs = {Ocr(Ocr_name.TESSERACT), Ocr(Ocr_name.EASY), Ocr(Ocr_name.DOCTR), Ocr(Ocr_name.PADDLE)}


def process(base_path, ref_dir, res_dir, file_type):
    if not is_valid_dir(base_path):
        exit()

    files = os.listdir(base_path)
    if len(files) > 50:
        files = files[:50]

    for file in tqdm(files, desc=f"Files in {res_dir}", total=len(files)):
        if not file.endswith(file_type):
            exit()

        image_path = os.path.join(base_path, file)

        res_file = file.replace(file_type, ".json")
        res_path = os.path.join(RESULT_DIR, res_dir, res_file)

        ref_file = file.replace(file_type, ".txt")
        ref_path = os.path.join(ref_dir, ref_file)

        with open(ref_path) as input:
            ref_text = input.read()

        data = {"file": file, "reference_text": ref_text, "results": []}

        with open(res_path, "w") as out:
            for ocr in ocrs:
                start_time = time.time()
                ocr.recognize_image(input_dir=image_path)
                final_time = time.time() - start_time

                candidate_text = ocr.get_text()
                data["results"].append(
                    {"name": ocr.get_name(), "text": candidate_text, "time": final_time}
                )

            json.dump(data, out, indent=4)


process(OBD_PATH, OBD_REF, "obd", ".tiff")
process(IAM_PATH, IAM_REF, "IAM", ".png")
process(POBD_PATH, POBD_REF, "pobd", ".png")
