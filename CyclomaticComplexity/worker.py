import os, sys, json, requests


def run():
    r = requests.get("http://localhost:5000/cyclomatic") # hardcode for now
    json_data = json.loads(r.text)
    print("Received: {}".format(json_data['sha']))


if __name__ == "__main__":
    run()