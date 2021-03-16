def is_stat_4XX(stat_course):
    if("STAT4" in stat_course):
        return True
    else:
        return False


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
    for c in list(courses):
        if(c != "CMSC" and

if __name__ == '__main__':
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
        "CMSC351": 3
    }

    print(lower_level_cs(c))
