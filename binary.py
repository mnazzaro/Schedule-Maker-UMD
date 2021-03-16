import json


def b_search(course_dict_list, low, high, c):
    # Check base case
    if high >= low:
 
        mid = (high + low) // 2
 
        # If element is present at the middle itself
        if course_dict_list[mid]["course_id"] == c:
            return course_dict_list[mid]["gen_ed"]
 
        # If element is smaller than mid, then it can only
        # be present in left subarray
        elif course_dict_list[mid]["course_id"] > c:
            return b_search(course_dict_list, low, mid - 1, c)
 
        # Else the element can only be present in right subarray
        else:
            return b_search(course_dict_list, mid + 1, high, c)
 
    else:
        # Element is not present in the array
        return -1


if __name__ == '__main__':

    with open("202008.json") as file:
        courses = json.load(file)

    #print(courses[5]["course_id"])
    print(b_search(courses, 0, len(courses), "PHYS261"))

