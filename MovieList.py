#!/usr/bin/python
# -*- coding: UTF-8 -*-
import ssl

from bs4 import BeautifulSoup
from urllib.parse import quote
import string
import urllib3
import MovieDetail
urllib3.disable_warnings()


user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit\
        /537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
baseurl = "https://www.piaohua.com"


class MovieList:
    def __init__(self, mysql, categorytitle, href):
        self.mysql = mysql
        self.categorytitle = categorytitle
        self.href = href
        self.endpages = 0
        self.currenturl = ''

    # noinspection PyMethodMayBeStatic
    def get_pages(self, soup):
        end = soup.find(class_='end')
        endpages = end.find('a').get('href').replace('list_', '').replace('.html', '')
        return endpages

    # noinspection PyMethodMayBeStatic
    def get_movie_list(self):
        soup = MovieList.get_movie_list_source(self, self.href)
        i = 1
        while i <= int(self.endpages):
            if i != 1:
                index = 'list_%d.html' % i
                soup = MovieList.get_movie_list_source(self, self.href.replace('index.html', index))
            MovieList.get_per_page_movie(self, soup)
            i = i + 1

    # noinspection PyMethodMayBeStatic
    def get_movie_list_source(self, url):
        print(url)
        self.currenturl = url
        headers = {
            'User-Agent': user_agent
        }
        url = quote(url, safe=string.printable)
        http = urllib3.PoolManager(cert_reqs=ssl.CERT_NONE)
        web_data = http.request('GET', url, headers=headers).data
        soup = BeautifulSoup(web_data, 'html.parser', from_encoding='GBK')
        if self.endpages == 0:
            self.endpages = MovieList.get_pages(self, soup)
        return soup

    # noinspection PyMethodMayBeStatic
    def get_per_page_movie(self, soup):
        lis = soup.findAll(class_='col-md-6')
        for li in lis:
            pic = li.find(class_='pic')
            pica = pic.find('a')
            detailurl = baseurl+pica.get('href')
            img = pica.find('img').get('src')
            txt = li.find(class_='txt')
            title = txt.find('font')
            if title is None:
                title = txt.find('b')
            if title is None:
                title = txt.find('a')
            if title is None:
                title = txt
            title = title.get_text()
            p = txt.find('em').get_text()
            try:
                title = title.replace(p, '')
                pass
            except Exception as e:
                print(str(e))
                pass
            time, title, text = MovieDetail.MovieDetail(self.mysql, detailurl, title).get_detail()
            MovieList.insetdb(self, self.categorytitle, title, p, time, text, img)

    # noinspection PyMethodMayBeStatic
    def insetdb(self, categorytitle, title, p, pubtime, details, pic):

        sql = "insert into movie(categorytitle, title, p, pubtime, details, pic, listpage)\
         values ('%s', '%s', '%s', '%s', '%s', '%s', '%s');" % \
              (categorytitle, title, p, pubtime, details, pic, self.currenturl)
        self.mysql.lock_execute(sql=sql)
