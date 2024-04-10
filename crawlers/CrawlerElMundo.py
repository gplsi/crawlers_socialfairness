import requests
from bs4 import BeautifulSoup, Tag
import os
from abc import ABC, abstractmethod


class CrawlerElMundo(ABC):

    @abstractmethod
    def parse(url):
        headline = date = intro = paragraphs = ''
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            data = response._content
            bs = BeautifulSoup(data, "html.parser")
            if bs:
                sections_head = bs.find_all('h1', {'class': 'ue-c-article__headline js-headline'})
                if sections_head:
                    headline = sections_head[0].text.strip()

                sections_intro = bs.find_all('p', {'class': 'ue-c-article__standfirst'})
                if sections_intro:
                    intro = sections_intro[0].text.strip()

                sections_date = bs.find_all('time')
                date = sections_date[0]['datetime']

                sections_body = bs.find_all('div', {'class': 'ue-l-article__body ue-c-article__body'})
                if sections_body:
                    for element in sections_body[0]:
                        if isinstance(element, Tag):
                            if 'p' == element.name:
                                paragraphs += element.text + '\n\n'

            text = headline + '\n' + 'Source[{0}]'.format(url) + '\n' + date + '\n' + intro + '\n' + paragraphs
            #text = headline + '\n' + 'Source[{0}]'.format(url) + '\n' + date + '\n' + paragraphs

        return (headline, date, intro + '\n' + paragraphs)