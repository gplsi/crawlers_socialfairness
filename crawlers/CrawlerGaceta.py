import requests
from bs4 import BeautifulSoup, Tag
import os
from abc import ABC, abstractmethod


class CrawlerGaceta(ABC):

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
                sections_head = bs.find_all('h1', {'class': 'elementor-heading-title elementor-size-default'})
                if sections_head:
                    headline = sections_head[0].text.strip()

                #sections_intro = bs.find_all('h2', {'class': 'post-subtitle'})
                #if sections_intro:
                #    intro = sections_intro[0].text.strip()
                #
                #Parece que no hay un subtitulo claro

                sections_date = bs.find_all('span', {'class': 'elementor-icon-list-text elementor-post-info__item elementor-post-info__item--type-date'})
                date = sections_date[0].text.strip()

                sections_body = bs.find_all('div', {'class': 'elementor-element elementor-element-7193014 contenido-single-general elementor-widget elementor-widget-theme-post-content'})
                section = sections_body[0].select_one('div:first-child')
                if section:
                    for element in section:
                        if isinstance(element, Tag):
                            if 'p' == element.name:
                                if element.find('em'):
                                    print('nada')
                                else:
                                    paragraphs += element.text + '\n\n'



                return (headline, date, intro + '\n' + paragraphs)