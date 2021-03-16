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

def populate_db (cdl):

    for course in cdl:
        if len(course['gen_ed']) > 0: 
            gened = json.dumps(course['gen_ed'][0]) 
        else: 
            gened = "[]"
        items = [course['course_id'], course['name'], course['dept_id'], course['credits'], course['description'], gened]
        print (items)
        sql_input = "INSERT INTO courses VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql_input, items)

req = requests.get("https://api.umd.io/v1/courses?semester=202101")
page = 1
while page < 148:
    print (f"Page: {page}, Status Code: {req.status_code}")
    populate_db(json.loads(req.text))
    page += 1
    req = requests.get(f"https://api.umd.io/v1/courses?semester=202101&page={page}")

print ("Committing...")
db.commit()

