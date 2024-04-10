import requests
from bs4 import BeautifulSoup, Tag
import os
from abc import ABC, abstractmethod


class CrawlerElpais(ABC):

    @abstractmethod
    def parse(url):
        headline = date = intro = paragraphs = ''
        response = requests.get(url)
        if response.status_code == 200:
            data = response._content
            bs = BeautifulSoup(data, "html.parser")
            if bs:
                sections_head = bs.find_all('h1', {'class': 'a_t'})
                if sections_head:
                    headline = sections_head[0].text.strip()

                sections_intro = bs.find_all('h2', {'class': 'a_st'})
                if sections_intro:
                    intro = sections_intro[0].text.strip()

                sections_date = bs.find_all('a', {'id': 'article_date_p'})
                date = sections_date[0].text.strip()

                sections_body = bs.find_all('div', {'class': 'a_c'})
                if sections_body:
                    for element in sections_body[0]:
                        if isinstance(element, Tag):
                            if 'p' == element.name:
                                paragraphs += element.text + '\n\n'

                text = headline + '\n' + 'Source[{0}]'.format(url) + '\n' + date + '\n\n' + intro + '\n' + paragraphs

        return (headline, date, intro + '\n' + paragraphs)