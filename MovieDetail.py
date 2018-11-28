#!/usr/bin/python
# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
from urllib.parse import quote
import string
import urllib3
import pymysql
import re
import MySql
urllib3.disable_warnings()

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit\
        /537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'


class MovieDetail:
    def __init__(self, mysql, url, movietitle):
        self.mysql = mysql
        self.url = url
        self.movietitle = movietitle

    # noinspection PyMethodMayBeStatic
    def get_detail(self):
        print(self.url)
        url = quote(self.url, safe=string.printable)
        headers = {
            'User-Agent': user_agent
        }
        http = urllib3.PoolManager()
        web_data = http.request('GET', url, headers=headers).data
        soup = BeautifulSoup(web_data, 'html.parser', from_encoding='GBK')
        try:
            info = soup.find(class_='info').get_text()
            pass
        except Exception as e:
            print(str(e))
            print(soup.find('body'))
            info = ''
            pass
        mat = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", info)
        time = mat.group(0)
        title = info.replace(time, '').replace('发布时间：', '').replace('片名：', '')
        if len(title) > 0:
            self.movietitle = title

        txt = str(soup.find(class_='txt'))
        txt = pymysql.escape_string(txt)
        bots = []
        a = soup.findAll(name='a', attrs={"href": re.compile(r'^ftp://')})
        bots += a
        b = soup.findAll(name='a', attrs={"href": re.compile(r'^magnet:')})
        bots += b
        c = soup.findAll(name='a', attrs={"href": re.compile(r'^ed2k://')})
        bots += c
        d = soup.findAll(name='a', attrs={"href": re.compile(r'^btbo://')})
        bots += d
        for down in bots:
            res = down.get('href')
            MovieDetail.insetdb(self, self.movietitle, res)
        return time, self.movietitle, txt

    # noinspection PyMethodMayBeStatic
    def insetdb(self, movietitle, res):
        sql = "insert into down(movietitle, res, detailpage)\
         values ('%s', '%s', '%s');" % \
              (movietitle, res, self.url)
        self.mysql.lock_execute(sql=sql)
