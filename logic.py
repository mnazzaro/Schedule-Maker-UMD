import requests
import json
import time
import mysql.connector

# db = mysql.connector.connect(
#     host="localhost",
#     username="root",
#     password="UMD100",
#     database="schedule-maker-umd"
# )

# cursor = db.cursor()


dsnl_count = 0
dsnl = False
dsns = False

dsns_dssp_count = 0
dshs_dsns_count = 0
dshs_dshu_count = 0
dshs_dssp_count = 0
dshu_dssp_count = 0

dshs_count = 0
dshs = False

dshu_count = 0
dshu = False

dssp_count = 0
dssp = False

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
        courses.remove("MATH140")
        if("MATH141" in courses):
            courses.remove("MATH141")
            course_size = len(courses)
            if(course_size < 2):
                return False
            for c in courses:
                if(is_stat_4XX(c)):
                    # ALL STAT 4XX = 3 credits
                    courses.remove(c)
                    break
            
            for c in courses:
                #cursor.execute("SELECT credits FROM courses WHERE course_id=%s", (c,))

                # if(is_math_stat(c) and \
                #     (cursor.fetchall[0][0] == 3 or cursor.fetchall[0][0] == 4)):
                if(is_math_stat(c)):

                    # if(requires_140(c) == True):
                    courses.remove(c)
                    break
            
            return (course_size - len(courses) == 2)
    
    return False


def lower_level_cs(courses):
    lower_level_reqs = ["CMSC132", "CMSC216", "CMSC250", \
        "CMSC330", "CMSC351"]

    if("CMSC131" in courses or "CMSC133" in courses):
        if(set(lower_level_reqs) <= set(courses)):
            return True
    
    return (False,0)


def UL_concentration(courses):
    disciplines = set(list(map(get_dept, courses)))
    if("CMSC" in disciplines):
        disciplines.remove("CMSC")
    print(disciplines)
    for subj in disciplines:
        if(meets_UL(courses, subj)):
            return True
    
    return (False,0)


def meets_UL(courses, dept):
    UL_credits = 0
    for c in courses:
        course_range = get_course_range(c)
        if(get_dept(c) == dept and \
                (course_range >= 300 and course_range < 500)):
            
            #cursor.execute("SELECT credits FROM courses WHERE course_id=%s", (c,))
            #UL_credits += cursor.fetchall[0][0]
            UL_credits += 3
            print(UL_credits)
    
    return UL_credits >= 12


def general_track(courses):
    systems = ["CMSC411", "CMSC412", "CMSC414", "CMSC416", "CMSC417"]
    info_processing = ["CMSC420", "CMSC421", "CMSC422", \
                       "CMSC423", "CMSC424", "CMSC426", "CMSC427", "CMSC470"]
    SE_PL = ["CMSC430", "CMSC433", "CMSC434", "CMSC435", "CMSC436"]
    theory = ["CMSC451", "CMSC452", "CMSC456", "CMSC457"]
    num_analysis = ["CMSC460", "CMSC466"]
    misc = ["CMSC320", "CMSC389N", "CMSC425", "CMSC454", "CMSC472"]
    total_general_courses = systems + info_processing + \
        SE_PL + theory + num_analysis

    index_list = [0, 0, 0, 0, 0]
    for i in range(len(courses)-1, -1, -1):
        print("i: " + str(i))
        c = courses[i]
        if(c in total_general_courses):
            if(c in systems):
                courses.remove(c)
                index_list[0] = index_list[0] + 1
            elif(c in info_processing):
                courses.remove(c)
                index_list[1] = index_list[1] + 1
            elif(c in SE_PL):
                courses.remove(c)
                index_list[2] = index_list[2] + 1
            elif(c in theory):
                courses.remove(c)
                index_list[3] = index_list[3] + 1
            if(c in num_analysis):
                courses.remove(c)
                index_list[4] = index_list[4] + 1
    
    if(sum(index_list) < 5):
        return False
    
    zero_count = 0
    for i in index_list:
        if(i == 0):
            zero_count += 1
    
    if(zero_count > 2):
        return False
    
    misc_count = 0
    for c in courses:
        if(c in total_general_courses or (c in misc)):
            misc_count += 1
    
    if(misc_count >= 2):
        return True
    
    return (False,0)

def b_search(course_dict_list, low, high, c):
    if high >= low:
 
        mid = (high + low) // 2
 
        if course_dict_list[mid]["course_id"] == c:
            return [course_dict_list[mid]["gen_ed"], course_dict_list[mid]["credits"]]
 
        elif course_dict_list[mid]["course_id"] > c:
            return b_search(course_dict_list, low, mid - 1, c)
 
        else:
            return b_search(course_dict_list, mid + 1, high, c)
 
    else:
        # Element is not present in the array
        return -1

def fulfills_FS(courses):
    fsaw, fspw, fsoc, fsma, fsar = False, False, False, False, False

    with open("202008.json") as file:
        courses_json = json.load(file)
    
    for c in courses:
        gen_ed = b_search(courses_json, 0, len(courses_json), c)

        if(gen_ed == ["FSAW"]):
            fsaw = True
        elif(gen_ed == ["FSPW"]):
            fspw = True
        elif(gen_ed == ["FSOC"]):
            fsoc = True
        elif(gen_ed == ["FSAR", "FSMA"]):
            fsar = True
            fsma = True
        elif(gen_ed == ["FSAR"]):
            fsar = True
        elif(gen_ed == ["FSMA"]):
            fsma = True


    return (fsaw and fspw and fsoc and fsar and fsma)

def fulfills_DS(given_courses):
    # globals
    global dsnl_count
    global dshs_count
    global dshu_count
    global dssp_count
    
    global dsnl
    global dsns
    global dshs
    global dshu
    global dssp

    global dsns_dssp_count
    global dshs_dsns_count
    global dshs_dshu_count
    global dshu_dssp_count
    global dshs_dssp_count

    global i_series_count
    global dvup_count

    with open("202008.json") as file:
        courses_json = json.load(file)

    for c in given_courses:
        course_data = b_search(courses_json, 0, len(courses_json), c)
        gen_ed = course_data[0]

        if(len(gen_ed) == 0):
            continue

        #DSNL
        if(gen_ed == ["DSNL"]):
            global dsnl_count
            dsnl_count += int(course_data[1])

        elif(gen_ed == ["DSNL", "SCIS"]):
            dsnl_count += int(course_data[1])
            # i_series_count += int(course_data[1])

        elif(gen_ed == ["DSNL", "DVUP"]):
            dsnl_count += int(course_data[1])
            # dvup_count += int(course_data[1])

        elif(len(gen_ed) > 0 and "DSNL(fkwh" in gen_ed[0]):
            coreq = gen_ed[0][ 9:gen_ed[0].index(")") ]
            coreq_taken = False

            for course_taken in given_courses:
                if(coreq in course_taken):
                    coreq_taken = True
                    break
            
            if(coreq_taken):
                print(course_data[1])
                dsnl_count += (int(course_data[1]) + 1)
                dsnl = True
            elif("DSNS" in gen_ed[0]):
                dsns = True
        
        # if(len(gen_ed) == 2 and gen_ed[1] == "SCIS"):
        #     i_series_count += int(course_data[1])
        # elif(len(gen_ed) == 2 and gen_ed[1] == "DVUP"):
        #     dvup_count += int(course_data[1])
        # elif(len(gen_ed) == 3 and gen_ed[1] == "DVUP" and gen_ed[2] == "SCIS"):
        #     dvup_count += int(course_data[1])
        #     i_series_count += int(course_data[1])

        # DSNS
        if(gen_ed[0] == "DSNS"):
            dsns = True
        elif(gen_ed[0] == "DSHSDSNS"):
            if(dsns == True):
                dshs_count += int(course_data[1])
            else:
                dshs_dsns_count += int(course_data[1])
        elif(gen_ed[0] == "DSNSDSSP"):
            if(dsns == True):
                dssp_count += int(course_data[1])
            else:
                dsns_dssp_count += int(course_data[1])
        
        # DSHS
        if(gen_ed[0] == "DSHS"):
            dshs_count += int(course_data[1])
        elif(gen_ed[0] == "DSHSDSHU"):
            dshs_dshu_count += int(course_data[1])
        elif(gen_ed[0] == "DSHSDSSP"):
            dshs_dssp_count += int(course_data[1])
        
        # DSHU
        elif(gen_ed[0] == "DSHU"):
            dshu_count += int(course_data[1])
        elif(gen_ed[0] == "DSHUDSSP"):
            dshu_dssp_count += int(course_data[1])
        # DSSP
        elif(gen_ed[0] == "DSSP"):
            dssp_count += int(course_data[1])

    
    if(dsnl_count >= 4):
        dsnl = True
    if(dshs_count >= 6):
        dshs = True
    if(dshu_count >= 6):
        dshu = True
    if(dssp_count >= 6):
        dssp = True

    # Class can be either DSNS or DSHS
    if(dsns is False and dshs is True):
        if(dshs_dsns_count >= 3):
            dshs_dsns_count -= 3
            dsns = True
            # No else because if dshs_dsns is not >= 3, it is 0
    elif(dsns is True and dshs is False):
        diff = 6 - dshs_count # we need 6 credits to satisfy dshs
        if(dshs_dsns_count >= diff):
            dshs_dsns_count -= diff
            dshs = True
            dshs_count += diff
        else:
            # Give the remaining dshs_dsns credits to dshs
             dshs_count += dshs_dsns_count
             dshs_dsns_count = 0
    elif(dsns is False and dshs is False):
        diff = 6 - dshs_count # Amount of dshs credits needed
        if(dshs_dsns_count >= (3 + diff)):
            dshs_dsns_count -= diff
            dsns = True
            dshs = True
            dshs_count += diff
        else:
            # This means dsns = 0 and dshs < 6 and there isn't enough
            # dshs_dsns credits to distribute
            # Ex: dsns = 0, dshs = 0, dshs_dsns = 5
            # if(dshs_dsns) > 3:
            #   give 3 to dsns and the rest (dshs_dsns) to dshs
            # else:
            #   we give all of it to dshs
            if(dshs_dsns_count > 3):
                dsns = True # dsns gets 3 credits
                dshs_count += (dshs_dsns_count - 3) # dshs gets the remaining
            else:
                dshs_count += dshs_dsns_count
                if(dshs_count >= 6):
                    dshs = True
            
            dshs_dsns_count = 0
    
    # Class can be either DSHS or DSHU
    if(dshs is False and dshu is True):
        diff = 6 - dshs_count
        if(dshs_dshu_count >= diff):
            dshs_dshu_count -= diff
            dshs = True
            dshs_count += diff
        else:
            # This means that we have some credits that
            # we can count as dshs, but not enough
            dshs += dshs_dshu_count
            dshs_dshu_count = 0
    elif(dshs is True and dshu is False):
        diff = 6 - dshu_count
        if(dshs_dshu_count >= diff):
            dshs_dshu_count -= diff
            dshu = True
            dshu_count += diff
        else:
            # This means that we have some credits that
            # we can count as dshu, but not enough
            dshu_count += dshs_dshu_count
            dshs_dshu_count = 0
    elif(dshs is False and dshu is False):
        diff1 = 6 - dshs_count
        diff2 = 6 - dshu_count
        if(dshs_dshu_count >= (diff1 + diff2)):
            dshs_dshu_count -= (diff1 + diff2)
            dshs = True
            dshs_count += diff1
            dshu = True
            dshu_count += diff2
        else:
            if(dshs_count + dshs_dshu_count >= 6):
                dshs_count += diff1 # if dshs is close to completion
                                              # give dshs JUST WHAT IT NEEDS
                dshs = True
                dshs_dshu_count -= diff1
            elif(dshu_count + dshs_dshu_count >= 6):
                dshu_count += diff2 # if dshu is close to completion
                                              # give dshu JUST WHAT IT NEEDS
                dshu = True
                dshs_dshu_count -= diff2
            else:
                if(dshs is False and dshu is False):
                    dshs_count += dshs_dshu_count # Just give to dshs and call it a day
                elif(dshs is True and dshu is False):
                    dshu_count += dshs_dshu_count # we MUST give it to dshu
                elif(dshs is False and dshu is True):
                    dshs_count += dshs_dshu_count # we MUST give it to dshs
                dshs_dshu_count = 0

    # Class can be either DSNS or DSSP
    if(dsns is False and dssp is True):
        diff = 3
        if(dsns_dssp_count >= diff):
            dsns_dssp_count -= diff
            dsns = True  
            # No else because if dsns_dssp < 3, it is 0
    elif(dsns is True and dssp is False):
        diff = 6 - dssp_count
        if(dsns_dssp_count >= diff):
            dsns_dssp_count -= diff
            dssp = True
            dssp += diff
        elif(dsns_dssp_count > 0):
            diff = dsns_dssp_count
            dsns_dssp_count = 0
            dssp_count += diff
        else:
            # This means that we have some credits that
            # we can count as dssp, but not enough
            dssp_count += dshs_dshu_count
            dshs_dshu_count = 0
    elif(dsns is False and dssp is False):
        diff1 = 3 # dsns credits needed
        diff2 = 6 - dssp_count # dssp credits needed
        if(dsns_dssp_count >= (diff1 + diff2)):
            dsns_dssp_count -= (diff1 + diff2)
            dsns = True
            dssp = True
            dssp_count += diff2
        else:
            if(dsns_dssp_count >= 3):
                dsns = True                         # if dsns is 0
                                                    # give 3 credits to dsns
                dssp_count += (dsns_dssp_count - 3) # Give the remaining to dssp
            else:
                dssp_count += dsns_dssp_count       # Just give the rest to dssp
            
            dsns_dssp_count = 0
    
    # Class can be either DSHU or DSSP
    if(dshu is False and dssp is True):
        diff = 6 - dshu_count
        if(dshu_dssp_count >= diff):
            dshu_dssp_count -= diff
            dshu = True  
            dshu_count += diff
        else:
            # This means that we have some credits that
            # we can count as dshu, but not enough
            dshu += dshu_dssp_count
            dshu_dssp_count = 0
    elif(dshu is True and dssp is False):
        diff = 6 - dssp_count
        if(dshu_dssp_count >= diff):
            dshu_dssp_count -= diff
            dssp = True
            dssp_count += diff
        else:
            # This means that we have some credits that
            # we can count as dshu, but not enough
            dssp_count += dshu_dssp_count
            dshu_dssp_count = 0

    elif(dshu is False and dssp is False):
        diff1 = 6 - dshu_count
        diff2 = 6 - dssp_count
        if(dshu_dssp_count >= (diff1 + diff2)):
            dshu_dssp_count -= (diff1 + diff2)
            dshu = True
            dshu_count += diff1
            dssp = True
            dssp_count += diff2
        else:
            if(dshu_count + dshu_dssp_count >= 6):
                dshu_count += diff1 # if dshu is close to completion
                                              # give it JUST WHAT IT NEEDS
                dshu = True
                dshu_dssp_count -= diff1
            if(dssp_count + dshu_dssp_count >= 6):
                dssp_count += diff2 # if dssp is close to completion
                                              # give it JUST WHAT IT NEEDS
                dssp = True
                dshu_dssp_count -= diff2
            else:
                if(dshu is False and dssp is False):
                    dshu_count += dshu_dssp_count # Just give to dshu and call it a day
                elif(dshu is True and dssp is False):
                    dssp_count += dshu_dssp_count # Must give it to dssp
                elif(dshu is False and dssp is True):
                    dshu_count += dshu_dssp_count # must give it to dshu
                dshu_dssp_count = 0
    
    # Class can be either DSHS or DSSP
    if(dshs is False and dssp is True):
        diff = 6 - dshs_count
        if(dshs_dssp_count >= diff):
            dshs_dssp_count -= diff
            dshs = True
            dshs_count += diff
        else:
            # This means that we have some credits that
            # we can count as dshs, but not enough
            dshs += dshs_dssp_count
            dshs_dssp_count = 0
    elif(dshs is True and dssp is False):
        diff = 6 - dssp_count
        if(dshs_dssp_count >= diff):
            dshs_dssp_count -= diff
            dssp = True
            dssp_count += diff
        else:
            # This means that we have some credits that
            # we can count as dshu, but not enough
            dssp_count += dshs_dssp_count
            dshs_dssp_count = 0
    elif(dshs is False and dssp is False):
        diff1 = 6 - dshs_count
        diff2 = 6 - dssp_count
        if(dshs_dssp_count >= (diff1 + diff2)):
            dshs_dssp_count -= (diff1 + diff2)
            dshs = True
            dshs_count += diff1
            dssp = True
            dssp_count += diff2
        else:
            if(dshs_count + dshs_dssp_count >= 6):
                dshs_count += diff1 # if dshu is close to completion
                                              # give JUST WHAT IT NEEDS
                dshs = True
                dshs_dssp_count -= diff1
            if(dssp_count + dshs_dssp_count >= 6):
                dssp_count += diff2 # if dssp is close to completion
                                              # give it all to dshu
                dssp = True
                dshs_dssp_count -= diff2
            else:
                if(dshs is False and dssp is False):
                    dshs_count += dshs_dssp_count # Just give to dshu and call it a day
                elif(dshs is True and dssp is False):
                    dssp_count += dshs_dssp_count # MUST give it to dssp
                elif(dshs is False and dssp is True):
                    dshs_count += dshs_dssp_count # MUST give it to dshs
                dshs_dssp_count = 0
    
    print("dsnl: " + str(dsnl))
    print("dsns: " + str(dsns))
    print("dshs: " + str(dshs))
    print("dshu: " + str(dshu))
    print("dssp: " + str(dssp))
    
    return (dsnl and dsns and dshu and dshs and dssp)

def fulfills_iseries(given_courses):
    i_series_count = 0

    with open("202008.json") as file:
        courses_json = json.load(file)

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

def fulfills_diversity(given_courses):
    dvup_count = 0
    dvcc_count = 0

    with open("202008.json") as file:
        courses_json = json.load(file)

    for c in given_courses:
        course_data = b_search(courses_json, 0, len(courses_json), c)
        gen_ed = course_data[0]

        if(len(gen_ed) == 0):
            continue
        
        if("DVUP" in gen_ed):
            dvup_count += int(course_data[1])
        if("DVCC" in gen_ed):
            dvcc_count += int(course_data[1])
    
    return (dvup_count >= 3 and (dvup_count + dvcc_count) >= 4)

def fulfills_gen_ed(courses):
    return ((fulfills_FS(courses) and fulfills_DS(courses)) and \
       (fulfills_iseries(courses) and fulfills_diversity(courses)))
        

def enough_credits(courses):
    credit_sum = 0
    for c in courses:
        credit_sum += 3 # sql stuff

    return credit_sum >= 120

def valid_schedule(c):
    courses = [item for sublist in c for item in sublist]
    ret_val = {
        "enough_credits": (enough_credits(courses), 0),
        "lower_level_math": (lower_level_math(courses), 0),
        "lower_level_cs": (lower_level_cs(courses), 0),
        "upper_level": (UL_concentration(courses), 0),
        "general_track": (general_track(courses), 0),
        "gened": (fulfills_gen_ed(courses), 0)
    }
    return ret_val
    
    # return (enough_credits(courses) and fulfills_gen_ed(courses) and lower_level_math(courses) \
    #     and lower_level_cs(courses) and UL_concentration(courses) \
    #         and general_track(courses))


if __name__ == '__main__':

    # gen_eds_fs = {
    #     "ENGL101": 3,
    #     "ENGL393": 3,
    #     "COMM107": 3,
    #     "MATH140": 4,
    #     "BIOM301": 3
    # }
    # c_advanced = {
    #     "CMSC411": 3,
    #     "CMSC412": 3,
    #     "CMSC414": 3,
    #     "CMSC430": 3,
    #     "CMSC466": 3, 
    #     "CMSC454": 3, 
    #     "CMSC425": 3    
    # }

    # c = {
    #     "MATH140": 4,
    #     "MATH141": 4,
    #     "STAT410": 3,
    #     "MATH161": 3, 
    #     "CMSC131": 4,
    #     "CMSC132": 4,
    #     "CMSC216": 4,
    #     "CMSC250": 4,
    #     "CMSC330": 3,
    #     "CMSC351": 3,
    #     "CMSC401": 3,
    #     "CMSC402": 3,
    #     "ART403": 3,
    #     "ART405": 4,
    # }

    # ds_test_set_1 = {
    #     "AASP200": 3,
    #     "PLCY100": 3,
    #     "CCJS225": 3,
    #     "BSOS201": 3,
    #     "ARHU275": 3,
    #     "AREC200": 3,
    #     "PHYS260": 1,
    #     "PHYS261": 3,
    #     "PHIL220": 3
    # }

    ds_test_set_2 = {
        "AREC200": 3, #DSNS or DSSP --> DSNS
        "ARHU275": 3, #DSHU or DSSP --> DSSP
        "ARHU319A": 3, #DSHU or DSSP --> DSSP
        "ENGL233": 3, #DSHU         --> DSHU
        "CLAS312": 3, #DSHS or DSHU  --> DSHU
        "ANTH266": 3, #DSHS         --> DSHS
        "FMSC302": 3, #DSHS or DSSP --> DSHS
        "AOSC200": 3,
        "AOSC201": 3
    }

    # diversity_test = {
    #     "FMSC110S": 3, #dvcc
    #     "AASP100": 3 # dvup
    # }
    
    ll_math = ["MATH140", "MATH141", "STAT400", "MATH241"]
    UL_test = ["AREC300", "AREC301", "AREC303", "AREC304"]
    gen_track = [""]

    s = [["ENGL101", "MATH140", "COMM107", "CMSC131", "CMSC100"],
                ["CMSC132", "MATH141", "PHYS121", "AASP100"],
                ["CMSC216", "CMSC250", "MATH240", "AMST328X"],
                ["CMSC330", "CMSC351", "STAT400", "PHYS161", "AASP200"],
                ["CMSC411", "CMSC412", "CHIN307", "ECON111", "CMSC414"],
                ["CMSC420", "CMSC451", "ENGL393", "ECON300", "ECON305"],
                ["CMSC320", "CMSC389N", "ECON306", "ARTH260", "CMSC425"],
                ["CMSC472", "ECON311", "ECON312", "ECON317", "ECON321"]]

    start = time.time()
    # print(lower_level_math(ll_math))
    # print(UL_concentration(UL_test))
    # print(general_track(gen_track))
    #print(fulfills_diversity(diversity_test))
    # print(valid_schedule(schedule))

    schedule = [item for sublist in s for item in sublist]
    print(fulfills_FS(schedule))
    print(fulfills_DS(schedule))
    print(fulfills_iseries(schedule))
    print(fulfills_diversity(schedule))

    end = time.time()
    print("Elapsed Time: {time}".format(time = end - start))
