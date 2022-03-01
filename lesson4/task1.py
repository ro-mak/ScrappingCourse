import datetime

from lxml import html
import requests
from pprint import pprint
import re
from pymongo import MongoClient
from pymongo import errors
import hashlib

url = "https://news.mail.ru/"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"
}
response = requests.get(url, headers=headers)
dom = html.fromstring(response.text)

# lenta
#
# result = dom.xpath("//*[self::a[@class='card-mini _topnews'] or self::a[@class='card-big _topnews _news']]")
#

# news.mail
day_news_table = dom.xpath("//table[contains(@class,'daynews__inner')]")[0]
top_news = day_news_table.xpath(".//div[contains(@class,'daynews__item') and not(contains(@class, 'hidden_small'))]")
day_news_list = dom.xpath("//ul[contains(@class,'list list_type_square list_half js-module')]")[0]
text_news = day_news_list.xpath(".//a[contains(@class,'list__text')]")


class NewsItem:
    def __init__(self, source_name, title, link, date):
        self._id = str(int(hashlib.sha256(source_name.encode('utf-8')).hexdigest(), 16) + int(
            hashlib.sha512(title.encode('utf-8')).hexdigest(), 16))
        self.source_name = source_name
        self.title = title
        self.link = link
        self.date = date

    def __str__(self):
        return f"Source: {self.source_name}, title: {self.title} link: {self.link} date: {self.date}"


def remove_special_chars(line):
    spaces = re.sub('\xa0', ' ', line)
    return re.sub('[\\r\\n]', '', spaces)


def connect_to_db():
    client = MongoClient('127.0.0.1', 27017)
    return client['news_db']


def save_to_db(news_item):
    try:
        db = connect_to_db()
        saved_news = db.news
        saved_news.insert_one(news_item.__dict__)
    except errors.DuplicateKeyError:
        print("Duplicate news item")


def print_db_contents():
    db = connect_to_db()
    saved_news = db.news
    result = saved_news.find({})
    for entry in result:
        print(entry)


for top_news_item in top_news:
    top_title = top_news_item.xpath(".//span[contains(@class, 'photo__title')]/text()")[0]
    link = top_news_item.xpath(".//a[contains(@class, 'photo')]/@href")[0]
    news_item = NewsItem("Mail", remove_special_chars(top_title), link, datetime.datetime.today())
    save_to_db(news_item)

for text_news_item in text_news:
    top_title = text_news_item.xpath(".//text()")[0]
    link = text_news_item.xpath("./@href")[0]
    news_item = NewsItem("Mail", remove_special_chars(top_title), link, datetime.datetime.today())
    save_to_db(news_item)

print_db_contents()
