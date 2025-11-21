import sys

import requests


def notify_discord(message):
    webhook_url = "https://discord.com/api/webhooks/1361674210795327681/wUsfNLIAinKfmWywtllm8Yen7Euwk7ophvTLizkUab7FjebEiCL86jcCFNNhqN_ikBp7"
    data = {"content": message, "allowed_mentions": {"parse": ["everyone"]}}
    requests.post(webhook_url, json=data)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        notify_discord(sys.argv[1])
    else:
        notify_discord("Test")
