import requests
from bs4 import BeautifulSoup, Tag
import os
from abc import ABC, abstractmethod


class Crawler20minutos(ABC):

    @abstractmethod
    def parse(url):
        headline = date = intro = paragraphs = ''
        response = requests.get(url)
        if response.status_code == 200:
            data = response._content
            bs = BeautifulSoup(data, "html.parser")
            if bs:
                sections_head = bs.find_all('h1', {'class': 'article-title'})
                if sections_head:
                    headline = sections_head[0].text.strip()

                sections_intro = bs.find_all('div', {'class': 'article-intro'})
                if sections_intro:
                    intro = sections_intro[0].text.strip()

                sections_date = bs.find_all('span', {'class': 'article-date'})
                date = sections_date[0].text.strip()

                sections_body = bs.find_all('div', {'class': 'article-text'})
                if sections_body:
                    for element in sections_body[0]:
                        if isinstance(element, Tag):
                            if 'p' == element.name:
                                if (element.attrs['class'][0] == 'paragraph'):
                                    paragraphs += element.text + '\n\n'
                            elif 'h2' == element.name:
                                paragraphs += element.text + '\n\n'

            text = headline + '\n' + 'Source[{0}]'.format(url) + '\n' + date + '\n\n' + intro + '\n' + paragraphs

            return (headline, date, intro + '\n' + paragraphs)