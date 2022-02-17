import random
import time
import re

import requests
from bs4 import BeautifulSoup

vacancy = input("Please enter vacancy: ")
base_url = "https://hh.ru"
first_url = base_url + f"/search/vacancy?area=1&fromSearchLine=true&text={vacancy}"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"}
response = requests.get(first_url, headers=headers)
dom = BeautifulSoup(response.text, 'html.parser')

button_next = dom.find("a", {"class": "bloko-button", "data-qa": "pager-next"})

vacancies = []


class Vacancy:
    def __init__(self, name, company, link, min_compensation=None, max_compensation=None, currency=None):
        self.name = name
        self.company = company
        self.min_compensation = min_compensation
        self.max_compensation = max_compensation
        self.currency = currency
        self.link = link

    def __str__(self):
        return f"{self.name}, {self.company}, {self.link}, {self.min_compensation}, {self.max_compensation}, {self.currency}, found at HH.ru"


def find_all_vacancies(dom_arg):
    vacancy_items = dom_arg.find_all("div", {"class": "vacancy-serp-item"})
    for vacancy in vacancy_items:
        try:
            title = vacancy.find("a", {"data-qa": "vacancy-serp__vacancy-title"})
            name = title.text
            link = title['href']
            company = vacancy.find("a", {"data-qa": "vacancy-serp__vacancy-employer"}).text
            sibling = vacancy.find("span", {"data-qa": "vacancy-serp__vacancy-compensation"})
            min_compensation = None
            max_compensation = None
            currency = None
            if sibling is not None:
                compensation = sibling.text
                comp_items = compensation.split(" ")
                if comp_items[0] == "от":
                    m_c = ""
                    for i in range(1, len(comp_items) - 1):
                        m_c += comp_items[i]
                    m_c = re.sub('\W+', '', m_c)
                    min_compensation = int(m_c)
                    currency = comp_items[len(comp_items) - 1]
                elif comp_items[0] == "до":
                    m_c = ""
                    for i in range(1, len(comp_items) - 1):
                        m_c += comp_items[i]
                    m_c = re.sub('\W+', '', m_c)
                    max_compensation = int(m_c)
                    currency = comp_items[len(comp_items) - 1]
                elif len([s for s in comp_items if any(xs in s for xs in ["–"])]) > 0:
                    compensation_without_currency = "".join(comp_items[:len(comp_items)-1])
                    from_to_comp = compensation_without_currency.split("–")
                    from_comp = re.sub('\W+', '', from_to_comp[0])
                    to_comp = re.sub('\W+', '', from_to_comp[1])
                    min_compensation = int(from_comp)
                    max_compensation = int(to_comp)
                    currency = comp_items[len(comp_items) - 1]

                vacancies.append(Vacancy(name, link, company, min_compensation, max_compensation, currency))
        except Exception as e:
            print(e)


def scrape_all_pages(button_next_arg):
    count = 0
    button = button_next_arg
    while count < 1 and button is not None:
        next_link = base_url + button['href']
        print(f"Next page(#{count}) opening url: {next_link}")
        next_response = requests.get(next_link, headers=headers)
        next_dom = BeautifulSoup(next_response.text, 'html.parser')
        find_all_vacancies(next_dom)
        count += 1
        print("Sleeping")
        print(time.time())
        time.sleep(random.Random().randint(1, 4))
        print("Waking up")
        print(time.time())
        button = next_dom.find("a", {"class": "bloko-button", "data-qa": "pager-next"})


scrape_all_pages(button_next)
for i in range(0, 100):
    print("_", end="")
for item in list(map(lambda x: str(x), vacancies)):
    print()
    print(item)
    for i in range(0, 100):
        print("_", end="")
    print()
