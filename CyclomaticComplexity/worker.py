import os, sys, json, requests, subprocess


def run():
    repoUrl = "https://github.com/fchollet/deep-learning-models"
    subprocess.call(["bash", "workerInitScript.sh", repoUrl])

    r = requests.get("http://localhost:5000/cyclomatic") # hardcode for now
    json_data = json.loads(r.text)
    print("Received: {}".format(json_data['sha']))
    subprocess.call(["bash", "workerGetCommit.sh", json_data['sha']])



if __name__ == "__main__":
    run()