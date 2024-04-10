import requests
from bs4 import BeautifulSoup, Tag
import os
from abc import ABC, abstractmethod


class CrawlerElespanol(ABC):

    @abstractmethod
    def parse(url):
        headline = date = intro = paragraphs = ''
        HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            data = response._content
            bs = BeautifulSoup(data, "html.parser")
            if bs:
                sections_head = bs.find_all('h1', {'class': 'article-header__heading article-header__heading--s3'})
                if sections_head:
                    headline = sections_head[0].text.strip()

                sections_intro = bs.find_all('h2', {'class': 'article-header__subheading'})
                if sections_intro:
                    intro = sections_intro[0].text.strip()

                sections_date = bs.find_all('span', {'class': 'article-header__time-date article-header__time--zonan-date'})
                date = sections_date[0].text.strip()

                sections_body = bs.find_all('div', {'class': 'article-body__content'})
                for element in sections_body[0]:
                    if isinstance(element, Tag):
                        if 'id' in element.attrs:
                            if element.attrs['id'].__contains__('paragraph'):
                                paragraphs += element.text + '\n\n'
                        elif 'class' in element.attrs:
                            if (element.attrs['class'][0] == 'p1') or (element.attrs['class'][0] == 'p2') or (element.attrs['class'][0] == 'content__summary-title'):
                                paragraphs += element.text + '\n\n'

            text = headline + '\n' + 'Source[{0}]'.format(url) + '\n' + date + '\n\n' + intro + '\n' + paragraphs

            return (headline, date, intro + '\n' + paragraphs)