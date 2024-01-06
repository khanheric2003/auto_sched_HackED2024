from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


driver = webdriver.Edge(
    executable_path=r"D:\a_web_driver\msedgedriver.exe")

driver.get("https://calendar.ualberta.ca/content.php?filter%5B27%5D=MATH&filter%5B29%5D=&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=39&expand=&navoid=12417&search_database=Filter&filter%5Bexact_match%5D=1#acalog_template_course_filter")


def change_course_filter(course):
    select_element = Select(driver.find_element_by_id('courseprefix'))
    # Select course that want to access the URL to
    select_element.select_by_value(course)

    submit_button = driver.find_element_by_xpath(
        '//input[@type="submit" and @title="Search Database" and @name="search_database"]')
    submit_button.click()


t = input()
