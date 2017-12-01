from flask import Flask
from flask_restful import Resource, Api, reqparse
import os, sys, json, requests


app = Flask(__name__)
api = Api(app)

#  API for dealing with the list of files as a whole
class cyclomaticApi(Resource):
    def __init__(self):  # Upon initialisation of the class
        global fileS  # Init the global server
        self.server = fileS  # Init the global server
        super(cyclomaticApi, self).__init__()  # Initialising the Resource class
        self.reqparser = reqparse.RequestParser()

        # For every value coming in JSON, you need an argument
        self.reqparser.add_argument('commit', type=str, location = 'json')  # Repeat for multiple variables
        self.reqparser.add_argument('complexity', type=str, location='json')
        # self.reqparser.add_argument('version', type=int, location='json')

    def get(self):
        commitValue = self.server.commitList[self.server.nextCommitToGive]
        self.server.nextCommitToGive += 1  # Move to next commit to hand out
        print("Sent: ".format(commitValue))
        return {'sha':commitValue}


    def post(self):
        return {'success':True}

#  Created a route at /cyclomatic with an endpoint called cyclomatic
api.add_resource(cyclomaticApi, "/cyclomatic", endpoint="cyclomatic")


class fileServer():
    def __init__(self):
        r = requests.get("https://api.github.com/repos/fchollet/deep-learning-models/commits")
        json_data = json.loads(r.text)
        self.commitList = []  # List containing all commit sha values
        for x in json_data:
            self.commitList.append(x['sha'])
            print("Commit Sha: {}".format(x['sha']))
        print("\n")
        self.nextCommitToGive = 0


if __name__ == "__main__":
    fileS = fileServer()  # Fill fileS with the init values of class fileServer
    app.run(port=5000, debug=True)  # int(sys.argv[1])
