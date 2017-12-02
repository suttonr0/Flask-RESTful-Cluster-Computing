from flask import Flask
from flask_restful import Resource, Api, reqparse
import os, sys, json, requests, time, getpass


app = Flask(__name__)
api = Api(app)

class getRepository(Resource):
    def __init__(self):  # Upon initialisation of the class
        global managerS  # Init the global server
        self.server = managerS  # Init the global server
        super(getRepository, self).__init__()  # Initialising the Resource class
        self.reqparser = reqparse.RequestParser()

        # For every value coming in JSON, you need an argument
        self.reqparser.add_argument('pullStatus', type=int, location = 'json')  # Repeat for multiple variables
        self.reqparser.add_argument('complexity', type=float, location='json')

    def get(self):
        args = self.reqparser.parse_args()
        if args['pullStatus'] == False:  # Repo hasn't been pulled yet
            print("GOT 1")
            return {'repo': "https://github.com/python/bedevere"}  # 'https://github.com/fchollet/deep-learning-models'
        if args['pullStatus'] == True:  # Repo has been pulled, can now increment
            self.server.currNumWorkers += 1
            if self.server.currNumWorkers == self.server.numWorkers:
                self.server.startTime = time.time()  # Start the timer
            print("WORKER NUMBER: {}".format(self.server.currNumWorkers))
    def post(self):
        pass

api.add_resource(getRepository, "/repo", endpoint="repo")


#  API for obtaining commits and posting the cyclomatic results
class cyclomaticApi(Resource):
    def __init__(self):  # Upon initialisation of the class
        global managerS  # Init the global server
        self.server = managerS  # Init the global server
        super(cyclomaticApi, self).__init__()  # Initialising the Resource class
        self.reqparser = reqparse.RequestParser()

        # For every value coming in JSON, you need an argument
        self.reqparser.add_argument('commitSha', type=str, location = 'json')  # Repeat for multiple variables
        self.reqparser.add_argument('complexity', type=float, location='json')
        # self.reqparser.add_argument('version', type=int, location='json')

    def get(self):
        if self.server.currNumWorkers < self.server.numWorkers: # still waiting on workers
            time.sleep(0.1)
            return {'sha': -2}
        if len(self.server.commitList) == 0:  # No more commits to give
            return {'sha': -1}
        commitValue = self.server.commitList[0]  # give next commit in list
        del self.server.commitList[0]  # Remove item from list of commits to compute
        print("Sent: {}".format(commitValue))
        return {'sha':commitValue}


    def post(self):
        args = self.reqparser.parse_args()  # parse the arguments from the POST
        print("Received sha {}".format(args['commitSha']))
        print("Received complexity {}".format(args['complexity']))
        self.server.listOfCCs.append({'sha':args['commitSha'], 'complexity':args['complexity']})
        print(self.server.listOfCCs)
        print(self.server.commitList)
        if len(self.server.listOfCCs) == self.server.totalNumberOfCommits:
            endTime = time.time() - self.server.startTime
            print("finished in {} seconds".format(endTime))
            print(len(self.server.listOfCCs))
            totalAverageCC = 0
            for x in self.server.listOfCCs:
                if x['complexity'] > 0:
                    totalAverageCC += x['complexity']
                else:
                    print("Commit {} has no computable files".format(x['sha']))
            totalAverageCC = totalAverageCC / len(self.server.listOfCCs)
            print("OVERALL CYCLOMATIC COMPLEXITY FOR REPOSITORY: {}".format(totalAverageCC))
        return {'success':True}

#  Created a route at /cyclomatic with an endpoint called cyclomatic
api.add_resource(cyclomaticApi, "/cyclomatic", endpoint="cyclomatic")


class managerServer():
    def __init__(self):
        self.numWorkers = input("Enter number of worker nodes: ")
        # self.repoDirectory = input("Enter the URL for the repository")
        self.numWorkers = int(self.numWorkers)
        self.currNumWorkers = 0  # Number of workers who have connected to the manager
        self.startTime = 0.0  # Start time for the timer
        # request repository info using the github API
        print("Authenticated Github API requests have a rate limit of 5000 per hour to the Github API")
        print("Unauthenticated requests have a limit of 60 requests per hour")
        gitUsername = input("Type your Github username, or press return to not use authenitcated requests: ")
        print(len(gitUsername))
        if len(gitUsername) != 0:
            gitPassword = getpass.getpass("Type your Github password (input is hidden): ")
        morePages = True  # Loop control variable to check if more pages on github API
        currentPage = 1  # Current page of github API repo info
        self.commitList = []  # List containing all commit sha values
        while morePages:
            if len(gitUsername) == 0:
                r = requests.get("https://api.github.com/repos/python/bedevere/commits?page={}&per_page=100".format(currentPage))  # "https://api.github.com/repos/fchollet/deep-learning-models/commits"
            else:
                r = requests.get("https://api.github.com/repos/python/bedevere/commits?page={}&per_page=100".format(currentPage), auth=(gitUsername, gitPassword))
            json_data = json.loads(r.text)
            if len(json_data) < 2:
                morePages = False
                print("All pages iterated through")
            else:
                for x in json_data:
                    self.commitList.append(x['sha'])
                    print("Commit Sha: {}".format(x['sha']))
                print("\n")
                currentPage += 1
        self.totalNumberOfCommits = len(self.commitList)  # Total number of commits in repo
        self.listOfCCs = []
        print("Number of commits: {}".format(self.totalNumberOfCommits))


if __name__ == "__main__":
    managerS = managerServer()  # ini an instance of managerServer()
    app.run(port=5000)  # int(sys.argv[1])  , debug=True
