from .Crawler20minutos import Crawler20minutos
from .CrawlerLavanguardia import CrawlerLavanguardia
from .CrawlerElpais import CrawlerElpais
from .CrawlerOkdiario import CrawlerOkdiario
from .CrawlerElMundo import CrawlerElMundo
from .CrawlerElperiodistadigital import CrawlerElperiodistadigital
from .CrawlerElconfidencial import CrawlerElconfidencial
from .CrawlerEldiario import CrawlerEldiario
from .CrawlerABC import CrawlerABC
from .CrawlerElespanol import CrawlerElespanol
from .CrawlerMarca import CrawlerMarca
from .CrawlerNTVespana import CrawlerNTVespana
from .CrawlerTheobjetive import CrawlerTheobjetive
from .CrawlerVozpopuli import CrawlerVozpopuli
from .CrawlerGaceta import CrawlerGaceta
from .CrawlerEldebate import CrawlerEldebate
from .CrawlerMoncloa import CrawlerMoncloa
from .CrawlerAlertaDigital import CrawlerAlertaDigital
from .CrawlerRamblaLibre import CrawlerRamblaLibre
from .CrawlerHispanidad import CrawlerHispanidad

dict_source = {'20minutos': Crawler20minutos,
                'elpais': CrawlerElpais,
                 'okdiario': CrawlerOkdiario,
                'periodistadigital': CrawlerElperiodistadigital,
                'lavanguardia': CrawlerLavanguardia,
                 'elmundo': CrawlerElMundo,
                 'elconfidencial': CrawlerElconfidencial,
                'eldiario': CrawlerEldiario,
                'abc': CrawlerABC,
                'elespanol': CrawlerElespanol,
                'marca': CrawlerMarca,
                'ntvespana': CrawlerNTVespana,
                'theobjective': CrawlerTheobjetive,
                'vozpopuli': CrawlerVozpopuli,
                'gaceta': CrawlerGaceta,
                'eldebate': CrawlerEldebate,
                'moncloa': CrawlerMoncloa,
                'alertadigital': CrawlerAlertaDigital,
                'ramblalibre': CrawlerRamblaLibre,
                'hispanidad': CrawlerHispanidad}


def get_source(url):
    if 'www' in url:
        result = url.split('www.')
    else:
        result = url.split('://')
    source = result[1].split('.')[0]
    return dict_source[source]

class NewsScraper():

    def parse(url):
        news_downloaded = []
        print("Escogiendo scaper de noticia...")
        source_crawler = get_source(str(url))
        print("Descargando noticia...")
        result_tuple = source_crawler.parse(str(url))
        news_downloaded.append({'url': str(url), 'headline': result_tuple[0], 'date': result_tuple[1], 'body': result_tuple[2]})
        print(str(url))
        if not result_tuple[0] or not result_tuple[2]:
            news_downloaded = []
        return news_downloaded
        #f = open(os.getcwd() + '/data_download/news_downloaded.json', "w+")
        #f.write(json.dumps(news_downloaded, indent=4))