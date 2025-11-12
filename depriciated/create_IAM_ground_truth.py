import json
import os

files = os.listdir("results/IAM/")

for file in files:
    if not file.endswith(".json"):
        continue

    file_path = "results/IAM/" + file
    with open(file_path) as input:
        data = json.load(input)
        results = data["results"]
        for result in results:
            if result["name"] == "pytesseract":
                file_name = data["file"]
                res_file = "IAM/data/000_ground_truth/" + file_name.replace(".png", ".txt")
                with open(res_file, "w") as output:
                    output.write(result["text"])
