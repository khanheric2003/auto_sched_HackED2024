from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import Select
import time

# ININITIALIZE FOR SELENIUM

faculty_redirect = {}

global_req_course_dic = {}

next_elements = []

# return


def find_degree_requirement(driver, faculty, start_year, degree_type, subject, certificate):
    url = 'https://calendar.ualberta.ca/content.php?catoid=39&navoid=12425#'
    driver.get(url)
    elements = driver.find_elements(By.ID, 'ent4989')
    for element in elements:
        if faculty in element.text:
            next_element = element.find_element_by_xpath(
                './following-sibling::*')
            if next_element.tag_name == 'a' and 'Go to information for this faculty.' in next_element.text:
                next_element.click()
                break

    if faculty == "Faculty of Science" and start_year >= 2024:
        # choose link that fit the year
        elems = driver.find_elements(By.CSS_SELECTOR, "a")
        for elem in elems:
            if "Effective Fall 2024" in elem.text:
                elem.click()
                break
        elems = driver.find_elements(By.CSS_SELECTOR, "a")
        # choose subject
        for elem in elems:
            if subject == elem.text:
                elem.click()
                break
        if degree_type == "Honors":

            print("passed Honor")
            elems = driver.find_elements(By.CLASS_NAME, "acalog-core")

            h2_elements = driver.find_elements(By.CSS_SELECTOR, "h2")
            for h2_element in h2_elements:
                if ("Honors in " + subject + " Requirements") in h2_element.text:
                    parent_element = h2_element.find_element_by_xpath(
                        '..')  # At Honors in something
                    next_element = parent_element.find_element_by_xpath(
                        './following-sibling::*')
                    # driver.quit()
                    return formatting_course_requirements(next_element.text)

            # couldnt find Honors

        elif degree_type == "Major":
            elems = driver.find_elements(By.CLASS_NAME, "acalog-core")
            h2_elements = driver.find_elements(By.CSS_SELECTOR, "h2")
            for h2_element in h2_elements:
                if ("Major in " + subject + " Requirements") in h2_element.text:
                    parent_element = h2_element.find_element_by_xpath(
                        '..')  # At Major in something
                    next_element = parent_element.find_element_by_xpath(
                        './following-sibling::*')
                    print("passed Major")
                    # driver.quit()
                    return formatting_course_requirements(next_element.text)

    elif degree_type == "Specialization":
        print("Passed1")
        elems = driver.find_elements(By.CSS_SELECTOR, "a")
        for elem in elems:
            if "Bachelor of Science Specialization" in elem.text:
                elem.click()
                break
        elems = driver.find_elements(By.CSS_SELECTOR, "a")

        # CLicked
        for elem in elems:
            if ("Specialization in " + subject) == elem.text:

                elem.click()
                inner_div = elem.find_element_by_xpath('..')
                print("Passed2")
                print(inner_div)

                ''' HAVENT FINISH HERE LOL'''

    elif degree_type == "General":
        elems = driver.find_elements(By.CSS_SELECTOR, "a")
        for elem in elems:
            if "Bachelor of Science General" in elem.text:
                elem.click()
                break
    else:  # Which is old "Honors"
        elems = driver.find_elements(By.CSS_SELECTOR, "a")
        for elem in elems:
            if "Bachelor of Science Honors" in elem.text:
                elem.click()
                break
    '''if faculty == 'Faculty of Engineering':'''
    #     wait = WebDriverWait(driver, 10)
    #     elements = wait.until(
    #         EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))
    # print("passpoint1")
    # for element in elements:
    #     # Check if the a element has the specific href attribute and the text
    #     if 'Qualifying Year' in element.text:
    #         print("passpoint2")
    #         element.click()
    #         break

    # their degree just straight up telling them what to do so.... nvm for engg


# output:dictionary


def formatting_course_requirements(text):
    lines = text.split('\n')
    result = {}
    key = ''
    count = 0
    notes = []

    for line in lines:
        if line.startswith('3 units from:'):
            count += 1
            key = f'{count}-{line}'
            result[key] = []
        elif line.startswith('Foundation Courses') or line.startswith('Senior Courses'):
            key = line
            result[key] = []
        elif line.startswith('Notes:'):
            key = line
        elif line != '':
            course = line.split(' - ')[0]
            if key.startswith('Notes:'):
                notes.append(course)
            elif key:  # Check if key is not empty
                result[key].append(course)

    # Combine all the notes into a single string
    result['Notes:'] = ' '.join(notes)

    print(result)

    return result


# test


# driver = webdriver.Edge(executable_path=r"D:\a_web_driver\msedgedriver.exe")

# url = 'https://calendar.ualberta.ca/content.php?catoid=39&navoid=12425#'
# faculty = 'Faculty of Science'
# # degree type = Honor, Major
# # find_degree_requirement(faculty, 2022, "Specialization",
# # "Computing Science", "")


# driver = webdriver.Edge(
#     executable_path=r"D:\a_web_driver\msedgedriver.exe")
# faculty = 'Faculty of Science'
# print(find_degree_requirement(driver, faculty, 2024, "Honors",
#                               "Computing Science", ""))

# holy

# t = input()
