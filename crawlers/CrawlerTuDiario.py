import requests
from bs4 import BeautifulSoup
import os
from abc import ABC, abstractmethod


class CrawlerTuDiario(ABC):

    @abstractmethod
    def parse(url):
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        print(url)
        if response.status_code == 200:
            data = response._content
        bs = BeautifulSoup(data, "html.parser")
        if bs:
            sections_head = bs.find_all('h1', {'class': 'post-title'})
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
            sections_date = bs.find_all('meta', {"property": "article:published_time"})
            if sections_date:
                date = sections_date[0]['content']
#                date = sections_date[0].a.text.strip()
            else:
                date = ''        
            
            sections_body = bs.find_all('div', {'class': 'adsb30'})
            if not sections_body:
                print('')
            # body = sections_body[0].text.strip()
            
            sections_p = bs.find_all('p')
            paragraphs = ''
            for list in sections_p:
                paragraphs += list.text + '\n'

            text = headline + '\n' + 'Source[{0}]'.format(url) + '\n' + date + '\n' + intro + '\n' + paragraphs
            #text = headline + '\n' + 'Source[{0}]'.format(url) + '\n' + date + '\n' + paragraphs

            return text



# class CrawlerElmundo():
#     base_url = 'https://www.snopes.com/fact-check/'
#     first_page = True
#
#     def parse(self, url):
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response._content
#         bs = BeautifulSoup(data, "html.parser")
#         if bs:
#             sections_main = bs.find('main', role='main')
#             sections_list = sections_main.find('div', {'class': 'list-group list-group-flush'}).find_all('a')
#             next_link = bs.find_all('a',{'class': 'page-link'})
#             if self.first_page:
#                 self.first_page = False
#                 url_next_page = next_link[0].get('href')
#             else:
#                 url_next_page = next_link[1].get('href')
#             self.parse(url_next_page)
#             pass

# parse('https://www.20minutos.es/noticia/4652514/0/remedio-lajara-se-convierte-en-la-primera-alcaldesa-de-yecla-en-el-siglo-xxi/')