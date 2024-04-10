import requests
from bs4 import BeautifulSoup, Tag
import os
from abc import ABC, abstractmethod


class CrawlerABC(ABC):

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
            sections_head = bs.find_all('h1', {'class': 'voc-title'})
            headline = ''
            if sections_head:
                headline = sections_head[0].text.strip()

            # headline = sections_head[0].text.strip() if not sections_head else ' '

            sections_intro = bs.find_all('h2', {'class': 'voc-subtitle'})

            # intro = sections_intro[0].text.strip() if not sections_intro else ' '

            intro = ''
            if sections_intro:
                intro = sections_intro[0].text.strip()

            sections_date = bs.find_all('time', {'class': 'voc-author__time'})
            date = sections_date[0].text.strip()
            paragraphs = bs.find_all('p', {'class': 'voc-p'})[0].text + '\n'

            sections_body = bs.find_all('span', {'class': 'paywall'})

            for element in sections_body[0]:
                if isinstance(element, Tag):
                    if 'class' in element.attrs:
                        if element.attrs['class'][0] == 'voc-p':
                            paragraphs += element.text + '\n\n'
                        elif element.name == 'div' and element.attrs['class'][0] == 'voc-c-container':
                            paragraphs += element.text + '\n\n'

            text = headline + '\n' + 'Source[{0}]'.format(url) + '\n' + date + '\n\n' + intro + '\n' + paragraphs

            return (headline, date, intro + '\n' + paragraphs)