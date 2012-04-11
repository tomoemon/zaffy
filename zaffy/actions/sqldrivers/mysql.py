# -*- coding: utf-8 -*-
import pymysql

class Mysql(object):
  def __init__(self):
    pass

  def connect(self, host, port, user, password, db):
    return pymysql.connect(host=host, port=port, user=user, passwd=password, db=db)

  def base_cursor(self):
    return pymysql.cursors.Cursor

  def dict_cursor(self):
    return pymysql.cursors.DictCursor
