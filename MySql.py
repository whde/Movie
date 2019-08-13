#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pymysql
import threading


mu = threading.Lock()


class MySql:
    def __init__(self):
        print('mysql __init__')
        self.db1 = pymysql.connect(
            host="localhost",
            user="root",
            passwd="Whde8751643",
            port=3306,
            db="Movie")
        cursor = self.db1.cursor()
        cursor.execute("DROP TABLE IF EXISTS down;")
        cursor.execute("DROP TABLE IF EXISTS movie;")
        cursor.execute("DROP TABLE IF EXISTS category;")
        cursor.execute("""SET SQL_SAFE_UPDATES = 0;""")
        categorysql = '''
        CREATE TABLE category (id int primary key auto_increment,
        title text);
        '''
        try:
            cursor.execute(categorysql)
            pass
        except Exception as e:
            print(str(e))
            pass
        moviesql = '''
        CREATE TABLE movie (id int primary key auto_increment,
        categorytitle text,
        title text,
        p text,
        details text,
        pubtime text,
        pic text,
        listpage text);
        '''
        try:
            cursor.execute(moviesql)
            pass
        except Exception as e:
            print(str(e))
            pass
        downsql = '''
        CREATE TABLE down (id int primary key auto_increment,
        movietitle text,
        res text,
        detailpage text
        );
        '''
        try:
            cursor.execute(downsql)
            pass
        except Exception as e:
            print(str(e))
            pass

    # noinspection PyMethodMayBeStatic
    def lock_execute(self, sql):
        if mu.acquire(True):
            MySql.write_to_db(self, sql)
            mu.release()

    def write_to_db(self, sql):
        print('write start!')
        try:
            cursor = self.db1.cursor()
            cursor.execute(sql)
        except Exception as e:
            print(str(e))
        finally:
            print('write finish!')
