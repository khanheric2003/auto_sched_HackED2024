from selenium import webdriver
from subject_collect import *
import web_scraping
from random import randrange

from msedge.selenium_tools import Edge, EdgeOptions
import itertools
# Assume the subjects required is CMPUT, MATH and STAT

proxies = ["172.219.243.90"]
proxy_pool = itertools.cycle(proxies)


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
    faculty = 'Faculty of Science'
    # For now Can only find >=2024
    driver = Edge(
        executable_path=r"D:\a_web_driver\msedgedriver.exe")
    subject_dict = web_scraping.find_degree_requirement(
        driver, faculty, 2024, "Honors", "Computing Science", "")

    common_subject_list = (get_common_subject_list(subject_dict))
    print(common_subject_list)
    driver.quit()
    drivers = {}  # Create a dictionary to store your driver instances

    PROXY = ["176.9.119.170:8080", "172.219.243.90", "72.10.160.171"]

    webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True
    for i in common_subject_list:
        random_num = (randrange(3))
        # forcefully change proxy
        webdriver.DesiredCapabilities.CHROME['proxy'] = {
            "httpProxy": PROXY[random_num],
            "ftpProxy": PROXY[random_num],
            "sslProxy": PROXY[random_num],
            "proxyType": "MANUAL",
        }

        drivers[f'driver{i}'] = webdriver.Edge(
            executable_path=r"D:\a_web_driver\msedgedriver.exe")

        value = run_subject_collect(drivers[f'driver{i}'], i)
        all_subjecs_dictionary[i] = value
        # print(all_subjecs_dictionary[i])


run()
