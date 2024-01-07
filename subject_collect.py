from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import Select

import time

# CMPUT
# driver.get("https://calendar.ualberta.ca/content.php?filter%5B27%5D=CMPUT&filter%5B29%5D=&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=39&expand=&navoid=12417&search_database=Filter&filter%5Bexact_match%5D=1#acalog_template_course_filter")

# MATH


# STAT


global_course_dic = {}

# neeeded to change this soon
odd_element_list = []
# input: outer element <tr>


def add_in_course_list(driver, elem):
    temp_course_dic = {}
    strong_elems = elem.find_elements(By.XPATH, ".//strong")
    a_elem = elem.find_element(By.CSS_SELECTOR, "a")
    description = elem.find_element(By.CSS_SELECTOR, "div:not([class])")
    for strong_elem in strong_elems:
        strong_text = strong_elem.text
        value = driver.execute_script(
            "return arguments[0].nextSibling.textContent;", strong_elem).strip()
        temp_course_dic[strong_text] = value

    p, c = preprocessing_description(description.text)
    temp_course_dic["Prequisite"] = p
    temp_course_dic["Corequisite"] = c
    global_course_dic[a_elem.text] = temp_course_dic
    # print(a_elem.text)
    # print(temp_course_dic)
    # print("================================")


def preprocessing_description(text):
    p_index = text.find("Prerequisite")
    c_index = text.find("Corequisite")
    dot_index = text.find(".")
    p = ""
    c = ""
    if p_index != -1:
        p = text[p_index:]
        p = p[:dot_index]
        blank_index = p.find(" ")
        p = text[blank_index:]
    if c_index != -1:
        c = text[c_index:]

    return p, c


''' Testing add_in_course_list on this'''
# Opening the aria-expanded part


def first_traversal(driver, list_of_wtf):

    elems = driver.find_elements(By.CSS_SELECTOR, "td.width")
    for elem in elems:
        a_elem = elem.find_element(By.CSS_SELECTOR, "a")
        if "Topics" in a_elem.text:
            continue

        # print(a_elem.text)
        if any(item in a_elem.text for item in list_of_wtf):
            # print(a_elem.text + "save in odd_element_list")
            # print("================================")
            odd_element_list.append(elem)
            continue
        elem.click()
        time.sleep(0.25)
        # test
        # input: 'elem' is your <tr> element
        add_in_course_list(driver, elem)


# odd case --> second traversal using XPATH and press it
def second_traversal(driver, list_of_wtf):
    for i in list_of_wtf:
        a_elem = driver.find_element(
            By.XPATH, f"//a[contains(text(), {i})]")
        a_elem.click()
        time.sleep(0.25)

    for i in odd_element_list:
        add_in_course_list(driver, i)

    print("---------------------------")
    print("Accessed ALL open elements")


def change_course_filter(driver, course):

    select_element = Select(driver.find_element_by_id('courseprefix'))
    # Select course that want to access the URL to
    select_element.select_by_value(course)

    submit_button = driver.find_element_by_xpath(
        '//input[@type="submit" and @title="Search Database" and @name="search_database"]')
    submit_button.click()


# input: subject name
def read_list_from_file(subject):
    file_path = f"odd_subject_list/{subject}.txt"
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return [line.strip() for line in lines]


def run_subject_collect(driver, subject):
    driver.get("https://calendar.ualberta.ca/content.php?filter%5B27%5D=MATH&filter%5B29%5D=&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=39&expand=&navoid=12417&search_database=Filter&filter%5Bexact_match%5D=1#acalog_template_course_filter")
    list_of_wtf = read_list_from_file(subject)
    change_course_filter(driver, subject)
    first_traversal(driver, list_of_wtf)
    second_traversal(driver, list_of_wtf)
    print("finished with " + subject)
    driver.quit()
    return global_course_dic
# t = input()


# driver = webdriver.Edge(executable_path=r"D:\a_web_driver\msedgedriver.exe")
# driver.get("https://calendar.ualberta.ca/content.php?filter%5B27%5D=MATH&filter%5B29%5D=&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=39&expand=&navoid=12417&search_database=Filter&filter%5Bexact_match%5D=1#acalog_template_course_filter")
# # input elements -- Only required to change these
# list_of_wtf = read_list_from_file("CMPUT")
# change_course_filter("CMPUT")
# first_traversal(list_of_wtf)
# second_traversal(list_of_wtf)
# print(global_course_dic)

# t = input()
