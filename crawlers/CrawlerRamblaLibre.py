import requests
from bs4 import BeautifulSoup, Tag
import os
from abc import ABC, abstractmethod


class CrawlerRamblaLibre(ABC):

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
                sections_head = bs.find_all('h1')
                if sections_head:
                    headline = sections_head[0].text.strip()

                #sections_intro = bs.find_all('h2')
                #if sections_intro:
                #   intro = sections_intro[0].text.strip()

                sections_date = bs.find_all('time', {'class': 'entry-date published'})
                date = sections_date[0].text.strip()

                sections_body = bs.find_all('div', {'class': 'entry-content'})
                sections_p = sections_body[0].find_all('p')
                paragraphs = ''
                for list in sections_p:
                    paragraphs += list.text + '\n\n'

                return (headline, date, intro + '\n' + paragraphs)