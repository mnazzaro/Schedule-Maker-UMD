"""from flask import Flask

app = Flask (__name__)

@app.route("/", methods=["GET"])
def get ():"""

import requests
import json

req = requests.get("https://api.umd.io/v1/courses?semester=202101&dept_id=CMSC&page=2")
for i in json.loads(req.text):
    print(i["course_id"])


