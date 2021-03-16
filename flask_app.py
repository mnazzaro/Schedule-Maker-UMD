from flask import Flask
from flask import request
import flask

import mysql.connector
import requests
import json

db = mysql.connector.connect(
    host="localhost",
    username="root",
    password="UMD100",
    database="schedule-maker-umd"
)

cursor = db.cursor()

app = Flask (__name__)

@app.route("/search_courses", methods=["GET"])
def search_courses ():
    cursor.execute(f"SELECT course_id, credits FROM courses WHERE course_id LIKE '{(request.args.get('letters')+'%')}'")
    results = cursor.fetchall()
    print (list(map(lambda x: x[0], results[0:3])))
    return {"results": list(map(lambda x: x[0] + " (" + str(x[1]) + ")", results[0:3]))}

if __name__ == "__main__":
    app.run(debug=True, port=3001)
    


