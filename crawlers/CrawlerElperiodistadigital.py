import requests
from bs4 import BeautifulSoup, Tag
import os
from abc import ABC, abstractmethod


class CrawlerElperiodistadigital(ABC):

    @abstractmethod
    def parse(url):
        headline = date = intro = paragraphs = ''
        response = requests.get(url)
        if response.status_code == 200:
            data = response._content
            bs = BeautifulSoup(data, "html.parser")
            if bs:
                sections_head = bs.find_all('h1', {'class': 'm4p-size-1 m4p-size-t-2 m4p-size-m-3'})
                if sections_head:
                    headline = sections_head[0].text.strip()

                sections_intro = bs.find_all('p', {'class': 'm4p-standfirst'})
                if sections_intro:
                    intro = sections_intro[0].text.strip()

                sections_date = bs.find_all('time', {'class': 'm4p-date'})
                date = sections_date[0].text.strip()

                sections_body = bs.find_all('div', {'class': 'm4p-post-content'})
                if sections_body:
                    for element in sections_body[0]:
                        if isinstance(element, Tag):
                            if ('p' == element.name) or ('h3' == element.name):
                                paragraphs += element.text + '\n\n'
                            elif ('blockquote' == element.name) and not ('class' in element.attrs):
                                for new_elemnet in element:
                                    if ('p' == new_elemnet.name) or ('h3' == new_elemnet.name):
                                        paragraphs += new_elemnet.text + '\n\n'



            text = headline + '\n' + 'Source[{0}]'.format(url) + '\n' + date + '\n\n' + intro + '\n' + paragraphs

            return (headline, date, intro + '\n' + paragraphs)