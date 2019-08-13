#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
import MovieList


class MovieThread(threading.Thread):
    def __init__(self, threadid, mysql, categorytitle, href):
        threading.Thread.__init__(self)
        self.threadid = threadid
        self.mysql = mysql
        self.categorytitle = categorytitle
        self.href = href

    def run(self):
        MovieList.MovieList(mysql=self.mysql, categorytitle=self.categorytitle, href=self.href).get_movie_list()

