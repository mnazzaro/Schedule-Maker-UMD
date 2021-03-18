from flask import Flask
from flask import request
from flask import jsonify

import pyodbc
import requests
import json

import logic

server = 'schedule-maker.database.windows.net'
database = 'ScheduleMaker'
username = 'Mark'
password = 'UMD100!!'   
driver= '{ODBC Driver 17 for SQL Server}'

db = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)

cursor = db.cursor()
cursor.fast_executemany = True

app = Flask (__name__)

@app.route("/search_courses", methods=["GET"])
def search_courses ():
    #try:
        results = cursor.execute("SELECT TOP 3 course_id, credits FROM courses WHERE course_id LIKE ?", request.args.get('letters')+'%').fetchall()
        x = list(map(lambda x: list(x), list(results)))
        return jsonify(x)
    

@app.route("/run_schedule", methods=["POST"])
def run_schedule ():
    return logic.valid_schedule(json.loads(request.data), cursor)

if __name__ == "__main__":
    app.run(debug=True, port=3001)
    


