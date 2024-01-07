from selenium import webdriver

from subject_collect import *
import web_scraping


# Assume the subjects required is CMPUT, MATH and STAT


def get_common_subject_list(course_dict):
    subjects = set()

    # Iterate over the dictionary
    for key, values in course_dict.items():
        # Iterate over the list of courses
        for course in values:
            # Split the course code into subject and number
            course_parts = course.split()
            # If course_parts is not empty and the first part of the course code is a subject, add it to the set
            if course_parts and course_parts[0].isalpha() and course_parts[0].isupper() and len(course_parts[0]) > 2:
                subjects.add(course_parts[0])

    # Convert the set to a list
    subjects_list = list(subjects)
    return subjects_list


def run():
    all_subjecs_dictionary = {}
    driver = webdriver.Edge(
        executable_path=r"D:\a_web_driver\msedgedriver.exe")
    faculty = 'Faculty of Science'
    # For now Can only find >=2024
    subject_dict = web_scraping.find_degree_requirement(driver, faculty, 2024, "Honors",
                                                        "Computing Science", "")

    common_subject_list = (get_common_subject_list(subject_dict))
    print(common_subject_list)
    for i in common_subject_list:
        driver1 = webdriver.Edge(
            executable_path=r"D:\a_web_driver\msedgedriver.exe")
        value = run_subject_collect(driver1, i)
        all_subjecs_dictionary[i] = value
        print(all_subjecs_dictionary[i])


run()
