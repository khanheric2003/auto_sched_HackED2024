from langchain.prompts import PromptTemplate
from langchain.chat_models import AzureChatOpenAI
from langchain.llms import AzureOpenAI
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.chains import LLMChain, APIChain
from langchain.chains.api.prompt import API_RESPONSE_PROMPT
from langchain.schema import Document
from langchain.tools import BaseTool
from langchain.agents import ZeroShotAgent, AgentExecutor, AgentType, initialize_agent, Tool, load_tools
from langchain.agents.agent_toolkits.openapi import planner
import pyodbc

import requests


from selenium import webdriver
from subject_collect import *
import web_scraping
from random import randrange

from msedge.selenium_tools import Edge, EdgeOptions
import itertools
# Assume the subjects required is CMPUT, MATH and STAT


url = ""

llm2 = AzureChatOpenAI(

    openai_api_type="azure",

    openai_api_base='',

    openai_api_version="2023-03-15-preview",

    deployment_name='',

    openai_api_key='',

    temperature=0.7,

    max_tokens=600

)
classifier_usecase2 = """<|im_start|>system

Given a sentence, reuiquired dictionary of required subject to take and dicitonarry all of the list of common subject, recommend student to take the course base on their
prefered subject. RENEMBER, this is UNiversity Of Alberta courses only, make order what to take first base on the prequisites and the level of the key when offered,
The output will be the draw course linked to each other and order it in term of year and term. You are permitted to add courses prequisites and corequisites outside the input to add up to the number of courses student choose to study in a term
'1-3 units from:": the first number is the order to take firstm recommended taking the FOundation first then the first "3 units from" coursess, recommend studying from level 100 to 500
The output have to be similar to the below example. Item that have (5-3 units from) shouldnt be appear in the same schedule, For example: only CMPUT 200 or CMPUT 300, cant be both in the schedule
Schedule usually span to 4 years. Never put these format into the schedule "6 units from: any 400-level MATH course (10-3 units from:)"
FOR EXAMPLE:
    Input: 'Foundation Courses': ['CMPUT 174', 'CMPUT 175'], '1-3 units from:': ['MATH 117', 'MATH 134', 'MATH 144', 'MATH 154'], '2-3 units from:': ['MATH 118', 'MATH 136', 'MATH 146', 'MATH 156'], '3-3 units from:': ['MATH 125', 'MATH 127'], '4-3 units from:': ['STAT 151', 'STAT 235', 'STAT 265'], 'Senior Courses': ['CMPUT 201', 'CMPUT 204', 'CMPUT 229', 'CMPUT 272', 'CMPUT 291'], '5-3 units from:': ['CMPUT 200', 'CMPUT 300'], '6-3 units from:': ['CMPUT 399', 'CMPUT 401', 'CMPUT 403', 'CMPUT 469', 'CMPUT 499'], '7-3 units from:': ['STAT 252', 'STAT 266', '18 units from:', 'any 300- and 400-level CMPUT course', '12 units from:', 'any 400-level CMPUT course'], 'Notes:': 'CMPUT 274 can serve as a substitute for CMPUT 174. CMPUT 275 can serve as a substitute for CMPUT 175 and CMPUT 201. If CMPUT 399 is taken, at least 3 units of the 18 units from any 300- and 400-level CMPUT course requirement must be at the 400 level. Upper level CMPUT courses may require specific CMPUT, MATH 
    or STAT courses as prerequisites. These prerequisites must be considered when choosing Science options.'
    and ['STAT', 'MATH', 'CMPUT'].Each course is 3 credit. You have to make it add up to 120. I want to study 5 courses a term
    Output:
Year 1 - Term 1:
- CMPUT 174 (Foundation Course)
- STAT 151 (4-3 units from:)
- MATH 117 (1-3 units from:)
- MATH 118 (2-3 units from:)
- CMPUT 200 (5-3 units from:)

Year 1 - Term 2:
- CMPUT 175 (Foundation Course)
- STAT 235 (4-3 units from:)
- MATH 134 (1-3 units from:)
- MATH 136 (2-3 units from:)
- CMPUT 300 (5-3 units from:)

Year 2 - Term 1:
- CMPUT 201 (Senior Course)
- STAT 265 (4-3 units from:)
- MATH 144 (1-3 units from:)
- MATH 146 (2-3 units from:)
- CMPUT 399 (6-3 units from:)

Year 2 - Term 2:
- CMPUT 291 (Senior Course)
- STAT 252 (7-3 units from:)
- MATH 154 (1-3 units from:)
- MATH 156 (2-3 units from:)
- CMPUT 401 (6-3 units from:)

Year 3 - Term 1:
- CMPUT 272 (Senior Course)
- STAT 266 (7-3 units from:)
- MATH 127 (3-3 units from:)
- CMPUT 403 (6-3 units from:)

Year 3 - Term 2:
- CMPUT 204 (Senior Course)
- CMPUT 402
- CMPUT 455
- CMPUT 469 (6-3 units from:)
- CMPUT 499 (6-3 units from:)

Year 4 - Term 1:
-  MATH 225
-  CMPUT 403
-  MATH 429
-  CMPUT 481

Year 4 - Term 2:
And it will so on til the number of courses add up to 120 credits

<|im_end|>
Input: {request}

<|im_start|>assistant

Output:"""

# response = chain({'input_documents': doc, 'question': query, 'context': hist,
#     'user_info': f'''The user chatting with you is named {name}, with email: {email}.
#     '''},
#  return_only_outputs=False)


proxies = ["172.219.243.90"]
proxy_pool = itertools.cycle(proxies)
chain = LLMChain(
    llm=llm2, prompt=PromptTemplate.from_template(classifier_usecase2))


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


def run(driver, faculty, start_year, degree_type, subject):
    all_subjecs_dictionary = {}
    faculty = 'Faculty of Science'
    # For now Can only find >=2024

    subject_dict = web_scraping.find_degree_requirement(
        driver, faculty, start_year, degree_type, subject, "")

    common_subject_list = (get_common_subject_list(subject_dict))
    print(common_subject_list)
    driver.quit()
    drivers = {}  # Create a dictionary to store your driver instances

    output = (
        chain.run(f"{subject_dict} and [{common_subject_list}] 5 subjects per term "))
    PROXY = ["176.9.119.170:8080", "172.219.243.90", "72.10.160.171"]

    return output
    # webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True
    # for i in common_subject_list:
    #     random_num = (randrange(3))
    #     # forcefully change proxy
    #     webdriver.DesiredCapabilities.CHROME['proxy'] = {
    #         "httpProxy": PROXY[random_num],
    #         "ftpProxy": PROXY[random_num],
    #         "sslProxy": PROXY[random_num],
    #         "proxyType": "MANUAL",
    #     }

    #     drivers[f'driver{i}'] = webdriver.Edge(
    #         executable_path=r"D:\a_web_driver\msedgedriver.exe")

    #     value = run_subject_collect(drivers[f'driver{i}'], i)
    #     all_subjecs_dictionary[i] = value
    #     print(all_subjecs_dictionary[i])


# test here
driver = Edge(
    executable_path=r"D:\a_web_driver\msedgedriver.exe")


# output = run(driver, 'Faculty of Science', 2024, "Honors", "Computing Science")
# print(output)

# output = run(driver, 'Faculty of Science', 2024,
#              "Major", "Applied Mathematics")
# print(output)

output = run(driver, 'Faculty of Science', 2024,
             "Major", "Biochemistry")
print(output)


# not yet done frontend and finished up -- too much lol -- can only implment part of it here
