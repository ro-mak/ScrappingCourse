import requests
from bs4 import BeautifulSoup

url = "https://www.hh.ru"

response = requests.get(url)

dom = BeautifulSoup(response.text, 'html.parser')