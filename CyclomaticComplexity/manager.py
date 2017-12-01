from flask import Flask
from flask_restful import Resource, Api, reqparse
import os, sys, json, requests


app = Flask(__name__)
api = Api(app)


class fileServer():
    def __init__(self):
        # If time, create directory with files inside and iterate to fill self.files
        # instead of explicit initialisation of files

        r = requests.get("https://api.github.com/repos/fchollet/deep-learning-models/commits")
        json_data = json.loads(r.text)
        print(json_data)
        for x in json_data:
            print("Commit Sha: {}".format(x['sha']))
        print("\n")


if __name__ == "__main__":
    fileS = fileServer()  # Fill fileS with the init values of class fileServer
    app.run(port=5000, debug=True)  # int(sys.argv[1]
