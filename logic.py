def is_stat_4XX(stat_course):
    if("STAT4" in stat_course):
        return True
    else:
        return False

def get_course_range(course):
    for char in course:
        if(char.isdigit()):
            return int(char) * 100
    
    return -1

def get_dept(course):
    dept = ""
    for char in course:
        if(char.isdigit()):
            return dept
        else:
            dept += char

    return "Not a course"


def is_math_stat(course):
    dept = get_dept(course)
    if(dept == "MATH" or dept == "STAT"):
        return True
    else:
        return False


def lower_level_math(courses):
    if("MATH140" in courses):
        courses.pop("MATH140", None)
        if("MATH141" in courses):
            courses.pop("MATH141")
            course_size = len(courses)
            if(course_size < 2):
                return False
            for c in list(courses):
                if(is_stat_4XX(c)):
                    # ALL STAT 4XX = 3 credits
                    courses.pop(c)
                    break
            
            for c in list(courses):
                if(is_math_stat(c) and (courses.get(c) == 3 or courses.get(c) == 4)):
                    # if(requires_140(c) == True):
                    courses.pop(c)
                    break
            
            if(course_size - len(courses) == 2):
                return True
            else:
                return False
    
    return False


def lower_level_cs(courses):
    lower_level_reqs = {
        "CMSC132": 4,
        "CMSC216": 4,
        "CMSC250": 4,
        "CMSC330": 3,
        "CMSC351": 3
    }
    if("CMSC131" in courses or "CMSC133" in courses):
        if(lower_level_reqs.items() <= courses.items()):
            return True
    
    return False


def UL_concentration(courses):
    disciplines = list(courses)
    disciplines = list(map(get_dept, disciplines))
    disciplines = set(disciplines)
    disciplines.remove("CMSC")
    print(disciplines)
    for subj in disciplines:
        if(meets_UL(courses, subj)):
            return True
    
    return False


def meets_UL(courses, dept):
    UL_credits = 0
    for c in list(courses):
        course_range = get_course_range(c)
        if(get_dept(c) == dept and (course_range >= 300 and course_range < 500)):
            UL_credits += courses[c]
            print(UL_credits)
    
    return UL_credits >= 12


def general_track(courses):
    systems = ["CMSC411", "CMSC412", "CMSC414", "CMSC416", "CMSC417"]
    info_processing = ["CMSC420", "CMSC421", "CMSC422", "CMSC423", "CMSC424", "CMSC426", "CMSC427", "CMSC470"]
    SE_PL = ["CMSC430", "CMSC433", "CMSC434", "CMSC435", "CMSC436"]
    theory = ["CMSC451", "CMSC452", "CMSC456", "CMSC457"]
    num_analysis = ["CMSC460", "CMSC466"]
    
    total_general_courses = systems + info_processing + SE_PL + theory + num_analysis
    index_list = [0, 0, 0, 0, 0]
    for c in list(courses):
        if(c in total_general_courses):
            if(c in systems):
                index_list[0] = index_list[0] + 1
            elif(c in info_processing):
                index_list[1] = index_list[1] + 1
            elif(c in SE_PL):
                index_list[2] = index_list[2] + 1
            elif(c in theory):
                index_list[3] = index_list[3] + 1
            if(c in num_analysis):
                index_list[4] = index_list[4] + 1
    
    if(sum(index_list) < 5):
        return False
    
    zero_count = 0
    for i in index_list:
        if(i == 0):
            zero_count += 1
    
    if(zero_count > 2):
        return False
    
    return True


if __name__ == '__main__':
    c_advanced = {
        "CMSC411": 3,
        "CMSC412": 3,
        "CMSC414": 3,
        "CMSC430": 3,
        "CMSC466": 3
    }

    c = {
        "MATH140": 4,
        "MATH141": 4,
        "STAT410": 3,
        "MATH161": 3, 
        "CMSC131": 4,
        "CMSC132": 4,
        "CMSC216": 4,
        "CMSC250": 4,
        "CMSC330": 3,
        "CMSC351": 3,
        "CMSC401": 3,
        "CMSC402": 3,
        "ART403": 3,
        "ART405": 4,
    }

    print(general_track(c_advanced))
