import json, requests, subprocess

def run():
    managerIP = input("Enter the IP of the manager: ")
    managerPort = input("Enter the port of the manager: ")
    numCommitsDone = 0

    r = requests.get("http://{}:{}/repo".format(managerIP,managerPort), json={'pullStatus': False})  # Don't have repo yet
    json_data = json.loads(r.text)
    repoUrl = json_data['repo']
    subprocess.call(["bash", "workerInitScript.sh", repoUrl])  # Call the initialisation script to pull repo

    r = requests.get("http://{}:{}/repo".format(managerIP,managerPort), json={'pullStatus': True})  # Have repo and are now ready

    stillHaveCommits = True
    while stillHaveCommits:
        r = requests.get("http://{}:{}/cyclomatic".format(managerIP,managerPort))  # get commit from manager
        json_data = json.loads(r.text)
        print(json_data)
        print("Received: {}".format(json_data['sha']))
        if json_data['sha'] == -2:  # Polling for manager to start giving commits
            # (manager is still setting up or waiting on workers)
           print("Polling")
        else:
            if json_data['sha'] == -1:
                print("No items left")
                break
            subprocess.call(["bash", "workerGetCommit.sh", json_data['sha']])
            # Call radon on the python repository and store its output
            binRadonCCOutput = subprocess.check_output(["radon", "cc", "-s", "-a" , "workerData"])
            radonCCOutput = binRadonCCOutput.decode("utf-8")  # Convert radon output from binary to string
            print(radonCCOutput)
            # Find last open bracket in radon output to find location of calculated average for repository
            avgCCstartPos = radonCCOutput.rfind("(")
            if radonCCOutput[avgCCstartPos+1:-2] == "":  # There are no files which radon can calculate C.C. for
                print("NO RELEVENT FILES")
                r = requests.post("http://{}:{}/cyclomatic".format(managerIP,managerPort),
                                  json={'commitSha': json_data['sha'], 'complexity': -1})
            else:
                averageCC = float(radonCCOutput[avgCCstartPos+1:-2])  # Get the average cyclomatic complexity from the output
                r = requests.post("http://{}:{}/cyclomatic".format(managerIP,managerPort),
                                  json={'commitSha': json_data['sha'], 'complexity': averageCC})
            numCommitsDone += 1  # Increment the number of commits this node has completed
    print("Completed having computed {} commits (including non-computable commits)".format(numCommitsDone))

if __name__ == "__main__":
    run()
