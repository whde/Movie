#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySql
import Category


if __name__ == "__main__":
    sql = MySql.MySql()
    Category.Category(sql).get_categorys()
    db = sql.db1
    db.commit()
    db.close()
