import re, datetime

from .firstscrap.pagehandler import PageHandler
from .firstscrap.listhandler import list_handler
from .firstscrap.proxyrefresh import proxy_refresher


class PaginatorNumPagesGetter(PageHandler):
    
    def __init__(self, URL):
        super().__init__()
        self.URL = URL
        self.use_selenium = False

    def extract_data_from_html(self, soup=None, selenium_driver=None):

        a = soup.find('a', attrs={"data-cy": "page-link-last"})
        number_of_pages = int( a.span.get_text().strip() )
        return number_of_pages


class LinksGetter(PageHandler):

    def __init__(self, URL):
        super().__init__()
        self.URL = URL
        self.use_selenium = False

    def extract_data_from_html(self, soup=None, selenium_driver=None):

        links = []
        a_tags = soup.find_all( "a", class_="marginright5 link linkWithHash detailsLink")
        for a in a_tags:
           links.append(a['href']) 
        return links


class AdDataGetter(PageHandler):

    def __init__(self, URL):
        super().__init__()
        self.URL = URL
        self.use_selenium = False

    def extract_data_from_html(self, soup=None, selenium_driver=None):

        em = soup.find('em')
        row_text = em.get_text().strip()
        return row_text


def month_to_int(str_month):
    months = {
        'января': 1,
        'февраля': 2,
        'марта': 3,
        'апреля': 4,
        'мая': 5,
        'июня': 6,
        'июля': 7,
        'августа': 8,
        'сентября': 9,
        'октября': 10,
        'ноября': 11,
        'декабря': 12,
    }
    return months[str_month]


def get_ads_date_time(links_to_ad):
    return list_handler(links_to_ad, AdDataGetter, with_processes=True, process_limit=50)


def get_list_of_links(urls):
    rezult = list_handler(urls, LinksGetter, with_processes=True, process_limit=50)
    #links_to_ad = (item for a_list in rezult for item in a_list)
    links_to_ad = []
    for a_list in rezult:
        for item in a_list:
            links_to_ad.append(item)
    return links_to_ad


def get_paginator_num_pages(URL):
    
    pag_getter = PaginatorNumPagesGetter(URL)
    return pag_getter.execute()

def scrap_data(URL):
    # обновление спискапрокси-верверов
    proxy_refresher()
    #получаем количество страниц пагинатора
    number_of_pages = get_paginator_num_pages(URL)
    # генерируем список url-ов страниц
    urls = (URL + '?page=' + str(i) for i in range(1, number_of_pages+1)) # range(1, number_of_pages+1)

    # получаем список ссылок на страницы объявлений
    links_to_ad = get_list_of_links(urls)

    # получаем данные объявлений (сырая строка)
    result = get_ads_date_time(links_to_ad)
    
    # преобразование сырой строки в дату-время
    re_time = re.compile('([0-1]\d|2[0-3])(:[0-5]\d)') # HH:MM
    re_date = re.compile(r'\d{1,}\s([а-яА-ЯёЁ]){1,}\s\d\d\d\d')   #29 июня 2019  2 июля 2019
    for item in result:
        str_time = re_time.search(item).group(0)
        str_date = re_date.search(item).group(0)

        hour, min = str_time.split(':')
        time = datetime.time(int(hour), int(min), 0)

        str_day, str_month, str_year = str_date.split()
        day = int(str_day)
        year = int(str_year)
        month = month_to_int(str_month)
        date = datetime.date(year, month, day)

        yield (date, time)