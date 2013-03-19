# -*- coding: utf-8 -*-
import sqlite3

def _dict_factory(cursor, row):
  d = {}
  for idx, col in enumerate(cursor.description):
    d[col[0]] = row[idx]
  return d

class _ConnectionWrapper(object):
  def __init__(self, conn):
    self.conn = conn

  def cursor(self, cursor_type=None):
    if cursor_type:
      self.conn.row_factory = cursor_type
    return self.conn.cursor()

  def commit(self):
    return self.conn.commit()

  def close(self):
    return self.conn.close()

class Sqlite(object):
  def __init__(self):
    pass

  def connect(self, db, host=None, user=None, password=None, port=None):
    con = sqlite3.connect(db)
    return _ConnectionWrapper(con)

  def base_cursor(self):
    return None

  def dict_cursor(self):
    return _dict_factory

