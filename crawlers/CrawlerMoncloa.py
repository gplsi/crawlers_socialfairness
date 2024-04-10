import requests
from bs4 import BeautifulSoup, Tag
import os
from abc import ABC, abstractmethod


class CrawlerMoncloa(ABC):

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
                sections_head = bs.find_all('h1', {'class': 'tdb-title-text'})
                if sections_head:
                    headline = sections_head[0].text.strip()

                sections_intro = bs.find_all('h2')
                if sections_intro:
                   intro = sections_intro[0].text.strip()

                sections_date = bs.find_all('time', {'class': 'entry-date updated td-module-date'})
                date = sections_date[0].text.strip()

                sections_body = bs.find_all('div', {'class': 'td_block_wrap tdb_single_content tdi_57 td-pb-border-top td_block_template_14 td-post-content tagdiv-type'})
                sections_p = sections_body[0].find_all('p')
                paragraphs = ''
                for list in sections_p:
                    paragraphs += list.text + '\n\n'

                return (headline, date, intro + '\n' + paragraphs)