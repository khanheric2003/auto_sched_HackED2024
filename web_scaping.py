from requests_html import HTMLSession
from bs4 import BeautifulSoup
from selenium import webdriver

# ININITIALIZE FOR SELENIUM
driver = webdriver.EdgesDriver()

#  finished choosing a link -> request to the link that contain the required subject for the degree

# already got the id of the faculty

# query = "Faculty of Engineering"

# input is degree name


# Ex: bachelor of Engineering, Bachelor of Science Specialization
# bachelor of Engineering/ Bachelor of Comerece/Law - Juris Doctor/ Faculté Saint-Jean (En Français) - all program/ Bachelor of Kinesiology, Sport, and Recreation
# / almost all of bachelor in MEdicine and dentistry/ Nursing/ Pharmacy
#  already have in this page

s = HTMLSession()


def naviagate_degree_url(faculty, query, *subject):
    link_dic = {}
    url = 'https://calendar.ualberta.ca/content.php?catoid=39&navoid=12425#'
    r = s.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
    })

    elements = r.html.find(f'a:contains("{query}")', first=False)

    for a in elements:
        # Get the href attribute of the a element
        link = a.attrs['href']
        text = a.text
        link_dic[text] = link

        # print(f"Text: {text}")
        # print(f"Link: {link}")
        # print(link_dic)
    print("passed t1")
    if faculty == 'Faculty of Science' or faculty == 'Faculty of Art':
        print('Bsc and Ba- continue to second_scrap()')
        return naviagate_degree_url2(link_dic[query], subject)

    return f"https://calendar.ualberta.ca/{link_dic[query]}"


def naviagate_degree_url2(redirect, subject):
    # print("func2")
    link_dic = {}

    s_url = f"https://calendar.ualberta.ca/{redirect}"
    r = s.get(s_url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
    })
    elements = r.html.find(f'a:contains("{subject[0]}")', first=False)
    for a in elements:
        # Get the href attribute of the a element
        link = a.attrs['href']
        text = a.text
        link_dic[text] = link
        # print(link_dic)

    t_url = f"https://calendar.ualberta.ca/{link_dic[subject[0]]}"
    return t_url


def scrap_url(link, main, *minor):
    # main is either Honors or Major
    r = s.get(link, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
    })
    soup = BeautifulSoup(r.text, 'html.parser')

    # Find the div with class 'acalog-core'
    divs = soup.find_all('div', class_='acalog-core')

    # Find the h2 tag within the 'acalog-core' div that contains 'Honors in'

    for div in divs:
        # Check if the div contains an h2 tag with 'Honors in'
        print(div.type())

        h2 = div.find('h2', string=lambda text: main + ' in' in text)
        # if h2:
        #     print("found")
        #     next_div = div.find_next_sibling('div')
        #     if next_div is not None:
        #         next_div_text = next_div.get_text()
        #         print(next_div_text)


# Only Art and science faculty need subjects input
query = "Bachelor of Science (Major and Honors) - Effective Fall 2024"
faculty = "Faculty of Science"
subject = "Applied Mathematics"
link = (naviagate_degree_url(faculty, query, subject))
print(link)

type_of_degree = "Honors"
print(scrap_url(link, type_of_degree))
