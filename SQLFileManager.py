#!/usr/bin/python
# -*- coding: UTF-8 -*-


import threading


mu = threading.Lock()


def create_sql_file():
    open('sql.txt', 'w+', encoding='utf-8')


def lock_test(sql):
    if mu.acquire(True):
        write_to_file(sql)
        mu.release()


def write_to_file(sql):
    fp = open('sql.txt', 'a+')
    print('write start!')
    try:
        fp.write(sql)
    finally:
        fp.close()
        print('write finish!')


def read_sql_file():
    fp = open('sql.txt', 'r+')
    return fp.read()
