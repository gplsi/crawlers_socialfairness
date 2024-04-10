import requests
from bs4 import BeautifulSoup, Tag
import os
from abc import ABC, abstractmethod


class CrawlerVozpopuli(ABC):

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
                sections_head = bs.find_all('h1', {'class': 'post-title'})
                if sections_head:
                    headline = sections_head[0].text.strip()

                sections_intro = bs.find_all('h2', {'class': 'post-subtitle'})
                if sections_intro:
                    intro = sections_intro[0].text.strip()

                sections_date = bs.find_all('p', {'class': 'date-group-published'})
                date = sections_date[0].text.strip()

                sections_body = bs.find_all('div', {'class': 'content-entry'})
                if sections_body:
                    for element in sections_body[0]:
                        if isinstance(element, Tag):
                            if 'p' == element.name:
                                paragraphs += element.text + '\n\n'
                            elif 'h2' == element.name:
                                if (element.attrs['class'][0] == 'wp-block-heading'):
                                    paragraphs += element.text + '\n\n'

            text = headline + '\n' + 'Source[{0}]'.format(url) + '\n' + date + '\n\n' + intro + '\n' + paragraphs

        return (headline, date, intro + '\n' + paragraphs)