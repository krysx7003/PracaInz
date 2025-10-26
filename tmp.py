import json

from Metrics import Metrics

metrics = Metrics()


def compare_own_results(id, file_name):
    csv_res = ""

    with open("./dataset/clean/text_data.json") as big:
        big_data = json.load(big)
        pages = [item for outer_list in big_data for item in outer_list]
        ref = pages[id]
        ref_text = ref["text"]

    with open(file_name) as f:
        data = json.load(f)

    for res in data:
        name = res["name"]
        candidate_text = res["text"]

        csv_res += f"{name},{metrics.calculate_scores(candidate_text, ref_text)}\n"

    print("Własne")
    print(csv_res)


def compare_iam_results(file_name):
    csv_res = ""
    with open(file_name) as f:
        data = json.load(f)
        ref_file = data["file"]
        results = data["results"]

    with open(ref_file) as f:
        ref_text = f.read()

    for res in results:
        name = res["name"]
        candidate_text = res["text"]

        csv_res += f"{name},{metrics.calculate_scores(candidate_text, ref_text)}\n"

    print("IAM")
    print(csv_res)


compare_own_results(0, "page1_0.json")
compare_iam_results("a01-000u.json")
