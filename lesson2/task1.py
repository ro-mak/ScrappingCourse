import requests
from bs4 import BeautifulSoup

vacancy = input("Please enter vacancy: ")

url = f"https://hh.ru/search/vacancy?area=1&fromSearchLine=true&text={vacancy}"
headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"}
response = requests.get(url, headers=headers)

dom = BeautifulSoup(response.text, 'html.parser')

vacancy_items = dom.find_all("div", {"class": "vacancy-serp-item"})
print(len(vacancy_items))