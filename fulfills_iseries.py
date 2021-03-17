def fulfills_iseries(courses):
    global i_series_count

    with open("202008.json") as file:
        courses_json = json.load(file)

    given_courses = list(courses)
    for c in given_courses:
        course_data = b_search(courses_json, 0, len(courses_json), c)
        gen_ed = course_data[0]

        if(len(gen_ed) == 0):
            continue

        if(gen_ed == ["SCIS"]):
            i_series_count += int(course_data[1])
        elif(len(gen_ed) >= 2 and gen_ed[1] == "SCIS"):
            i_series_count += int(course_data[1])
        elif(len(gen_ed) >= 3 and gen_ed[2] == "SCIS"):
            i_series_count += int(course_data[1])
    
    return (i_series_count >= 6)


    