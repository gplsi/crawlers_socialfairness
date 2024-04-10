import requests
from bs4 import BeautifulSoup, Tag
import os
from abc import ABC, abstractmethod


class CrawlerOkdiario(ABC):

    @abstractmethod
    def parse(url):
        headline = date = intro = paragraphs = ''
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        print(url)
        if response.status_code == 200:
            data = response._content
        bs = BeautifulSoup(data, "html.parser")
        if bs:
            sections_head = bs.find_all('h1', {'class': 'entry-title'})
            headline = ''
            if sections_head:
                headline = sections_head[0].text.strip()

            # headline = sections_head[0].text.strip() if not sections_head else ' '

            sections_intro = bs.find_all('h2')
            
            if sections_intro:
                intro = sections_intro[0].text.strip() if not sections_intro else ' '
            else:
                intro = ''
            # intro = ''
            # if sections_intro:
            #     intro = sections_intro[0].text.strip()


#            sections_date = bs.find_all('a', {'li': 'publish-time'})
            sections_date = bs.find_all('time', {"class": "date"})
            date = sections_date[0].a.text.strip()
            sections_body = bs.find_all('div', {'class': 'entry-content'})
            if sections_body:
                paragraphs = ''
                for element in sections_body[0]:
                    if isinstance(element, Tag):
                        if 'p' == element.name:
                            paragraphs += element.text + '\n\n'
                        elif 'h2' == element.name:
                            if (element.attrs['class'][0] == 'title2'):
                                paragraphs += element.text + '\n\n'

            # sections_p = sections_body[0].find_all('p')
            # paragraphs = sections_p[0].text


            text = headline + '\n' + 'Source[{0}]'.format(url) + '\n' + date + '\n' + intro + '\n' + paragraphs
            #text = headline + '\n' + 'Source[{0}]'.format(url) + '\n' + date + '\n' + paragraphs

            return (headline, date, intro + '\n' + paragraphs)