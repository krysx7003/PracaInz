import argparse
import os
import time

from tqdm import tqdm

from Metrics import Metrics
from OCR import Ocr
from utils.path import is_valid_dir
from utils.push_notification import notify_discord

RESULT_DIR = "./results"
HEADER = "cer_res,wer_res,time\n"

metrics = Metrics()


def process(base_path, ref_dir, res_dir, file_type, ocr):
    if not is_valid_dir(base_path):
        exit()

    files = os.listdir(base_path)

    data = HEADER
    for file in tqdm(files, desc=f"Files in {res_dir}", total=len(files)):
        if not file.endswith(file_type):
            exit()

        image_path = os.path.join(base_path, file)

        res_path = os.path.join(RESULT_DIR, res_dir)
        os.makedirs(res_path, exist_ok=True)
        res_path = os.path.join(res_path, ocr.get_name() + ".csv")

        ref_file = file.replace(file_type, ".txt")
        ref_path = os.path.join(ref_dir, ref_file)

        with open(ref_path) as input:
            reference_text = input.read()

            start_time = time.time()
            ocr.recognize_image(input_dir=image_path)
            final_time = time.time() - start_time

            candidate_text = ocr.get_text()
            data += f"{metrics.calculate_scores(candidate_text, reference_text)},{final_time}\n"

    with open(res_path, "w") as out:
        out.write(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--Base")
    parser.add_argument("-ref", "--Reference")
    parser.add_argument("-res", "--Result")
    parser.add_argument("-ft", "--FileType")
    parser.add_argument("-n", "--Name")
    args = parser.parse_args()

    if args.Base:
        base_path = args.Base

    if args.Reference:
        ref_dir = args.Reference

    if args.Result:
        res_dir = args.Result

    if args.FileType:
        file_type = args.FileType

    if args.Name:
        ocr_name = args.Name

    ocr = Ocr(ocr_name)
    notify_discord(
        f"""
        ## Starting experiment with parameters
        - Base path: {base_path}
        - Reference directory: {ref_dir}
        - Result directory {res_dir}
        - File type: {file_type}
        - OCR name: {ocr_name}
        """
    )
    process(base_path, ref_dir, res_dir, file_type, ocr)
    notify_discord("## Experiment completed")
