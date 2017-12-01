import os, sys, json, requests, subprocess
from radon.cli.harvest import CCHarvester

def run():
    repoUrl = "https://github.com/fchollet/deep-learning-models"
    subprocess.call(["bash", "workerInitScript.sh", repoUrl])

    r = requests.get("http://localhost:5000/cyclomatic") # hardcode for now
    json_data = json.loads(r.text)
    print("Received: {}".format(json_data['sha']))
    subprocess.call(["bash", "workerGetCommit.sh", json_data['sha']])
    radonCCOutput = subprocess.check_output(["radon", "cc", "-s", "-a" , "workerData"])

    print(radonCCOutput.decode("utf-8"))

if __name__ == "__main__":
    run()