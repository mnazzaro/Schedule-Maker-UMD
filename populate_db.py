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

# This function takes a list of course dictionaries and grabs the values from each and sticks them into the MySQL db
def populate_db (cdl):

    for course in cdl:
        if len(course['gen_ed']) > 0: #Check to see if it's a gened class. If it is, the list won't be empty
            gened = json.dumps(course['gen_ed'][0]) 
        else: 
            gened = "[]"
        items = [course['course_id'], course['name'], course['dept_id'], course['credits'], course['description'], gened]
        print (items)
        sql_input = "INSERT INTO courses VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql_input, items)

req = requests.get("https://api.umd.io/v1/courses?semester=202101")
page = 1
while page < 148: #This magic number is the number of pages in the umd.io courses api. It will likely have to change for future semesters
    print (f"Page: {page}, Status Code: {req.status_code}")
    populate_db(json.loads(req.text))
    page += 1
    req = requests.get(f"https://api.umd.io/v1/courses?semester=202101&page={page}")

print ("Committing...")
db.commit()

