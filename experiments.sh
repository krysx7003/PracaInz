#!/bin/bash

IAM_PATH="./IAM/data/000"
IAM_REF="./IAM/data/000_ground_truth"

OBD_PATH="./old-books-dataset/300dpi/tiff"
OBD_REF="./old-books-dataset/groundtruth"

POBD_PATH="./dataset/clean"
POBD_REF="./dataset/ground_truth"


BASE_PATH=$POBD_PATH
REF_DIR=$POBD_REF
FILE_TYPE=".png"

for i in {1..5}; do
    RES_DIR="exp1_${i}"

    python utils/push_notification.py \
        "# Running repetition $i"

    for ocr_engine in "pytesseract" "easyocr" "doctr" "paddle"; do
        python datasets_v2.py \
            -b "$BASE_PATH" \
            -ref "$REF_DIR" \
            -res "$RES_DIR" \
            -ft "$FILE_TYPE" \
            -n "$ocr_engine"
    done
    python utils/push_notification.py \
        "# Completed repetition $i"
done

python utils/putils/ush_notification.py \
    "# Experiment finished"

# python datasets_v2.py -b ./dataset/clean -ref ./dataset/ground_truth -res exp1_1 -ft .png -n pytesseract
