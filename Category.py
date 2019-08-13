#!/usr/bin/python
# -*- coding: UTF-8 -*-
import ssl

from bs4 import BeautifulSoup
from urllib.parse import quote
import string
import urllib3
import MovieThread

urllib3.disable_warnings()

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit\
        /537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'


class Category:
    def __init__(self, mysql):
        print('Category __init__')
        self.mysql = mysql

    # noinspection PyMethodMayBeStatic
    def get_categorys(self):
        url = "https://www.piaohua.com"
        print(url)
        url = quote(url, safe=string.printable)
        headers = {
            'User-Agent': user_agent
        }
        http = urllib3.PoolManager(cert_reqs=ssl.CERT_NONE)
        web_data = http.request('GET', url, headers=headers).data
        soup = BeautifulSoup(web_data, 'html.parser', from_encoding='GBK')
        nav = soup.find(class_='nav')
        div = nav.find(class_='wp')
        ul = div.find('ul')
        alist = ul.findAll('a')
        list1 = []
        threads = []
        for i in range(len(alist)):
            a = alist[i]
            d = dict()
            href = a.get('href')
            if href.find('html') >= 0:
                href = url+href
                title = a.get_text()
                d['href'] = href
                d['title'] = title
                Category.insetdb(self, title)
                t = MovieThread.MovieThread(str(i), self.mysql, title, href)
                threads.append(t)
                list1.append(d)
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        return list1

    def insetdb(self, categorytitle):
        sql = "insert into category(title) values ('%s');" % categorytitle
        self.mysql.lock_execute(sql=sql)
