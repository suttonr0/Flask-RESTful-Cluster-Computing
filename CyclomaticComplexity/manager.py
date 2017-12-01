from flask import Flask
from flask_restful import Resource, Api, reqparse
import os, sys, json, requests


app = Flask(__name__)
api = Api(app)

#  API for dealing with the list of files as a whole
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
        if len(self.server.commitList) == 0:
            return {'sha': -1}
        commitValue = self.server.commitList[0]
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
        if len(self.server.commitList) == 0:
            print("finished")
            print(len(self.server.listOfCCs))
            totalAverageCC = 0
            for x in self.server.listOfCCs:
                totalAverageCC += x['complexity']
            totalAverageCC = totalAverageCC / len(self.server.listOfCCs)
            print("OVERALL CYCLOMATIC COMPLEXITY FOR REPOSITORY: {}".format(totalAverageCC))
        return {'success':True}

#  Created a route at /cyclomatic with an endpoint called cyclomatic
api.add_resource(cyclomaticApi, "/cyclomatic", endpoint="cyclomatic")


class managerServer():
    def __init__(self):
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
