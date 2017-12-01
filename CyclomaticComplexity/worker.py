import os, sys, json, requests, subprocess
from radon.cli.harvest import CCHarvester

def run():
    repoUrl = "https://github.com/fchollet/deep-learning-models"
    subprocess.call(["bash", "workerInitScript.sh", repoUrl])

    r = requests.get("http://localhost:5000/cyclomatic") # hardcode for now
    json_data = json.loads(r.text)
    print("Received: {}".format(json_data['sha']))
    subprocess.call(["bash", "workerGetCommit.sh", json_data['sha']])
    binRadonCCOutput = subprocess.check_output(["radon", "cc", "-s", "-a" , "workerData"])
    radonCCOutput = binRadonCCOutput.decode("utf-8")  # Convert from binary to tring

    print(radonCCOutput)
    avgCCstartPos = radonCCOutput.rfind("(")  # Find last open bracket in radon output
    averageCC = float(radonCCOutput[avgCCstartPos+1:-2])  # Get the average cyclomatic complexity from the output
    print(averageCC)
    r = requests.post("http://localhost:5000/cyclomatic", json={'commitSha': json_data['sha'], 'complexity': averageCC})

if __name__ == "__main__":
    run()