from flask import Flask
from flask_restful import Resource, Api, reqparse
import os, sys, json, requests, time


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
            return {'repo': 'https://github.com/fchollet/deep-learning-models'}
        if args['pullStatus'] == True:  # Repo has been pulled, can now increment
            self.server.currNumWorkers += 1
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
            print("finished")
            print(len(self.server.listOfCCs))
            totalAverageCC = 0
            for x in self.server.listOfCCs:
                if x['complexity'] > 0:
                    totalAverageCC += x['complexity']
                else:
                    print("{} has no computable files".format(x['sha']))
            totalAverageCC = totalAverageCC / len(self.server.listOfCCs)
            print("OVERALL CYCLOMATIC COMPLEXITY FOR REPOSITORY: {}".format(totalAverageCC))
        return {'success':True}

#  Created a route at /cyclomatic with an endpoint called cyclomatic
api.add_resource(cyclomaticApi, "/cyclomatic", endpoint="cyclomatic")


class managerServer():
    def __init__(self):
        self.numWorkers = input("Enter number of worker nodes: ")
        self.numWorkers = int(self.numWorkers)
        self.currNumWorkers = 0
        r = requests.get("https://api.github.com/repos/fchollet/deep-learning-models/commits")
        json_data = json.loads(r.text)
        self.commitList = []  # List containing all commit sha values
        for x in json_data:
            self.commitList.append(x['sha'])
            print("Commit Sha: {}".format(x['sha']))
        print("\n")
        self.totalNumberOfCommits = len(self.commitList)
        self.listOfCCs = []
        print("Number of commits: {}".format(self.totalNumberOfCommits))


if __name__ == "__main__":
    managerS = managerServer()  # ini an instance of managerServer()
    app.run(port=5000, debug=True)  # int(sys.argv[1])
