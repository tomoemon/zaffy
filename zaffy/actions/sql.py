# -*- coding: utf-8 -*-

from os import path
from load_module import load_module_dir

drivers = {}
modules = load_module_dir(path.join("actions", "sqldrivers"))
for module in modules:
  klass = getattr(module, module.__name__.title())
  drivers[module.__name__] = klass()

class Sql(object):
  default_params = {"driver":"", "host":"", "db":None, "port":3306,
      "user":"", "password":"", "sql":""}

  def __init__(self, setting):
    self.result = {}
    self.exception = None
    self.setting = setting

  def run(self):
    getattr(self, "do_" + self.setting.method)()

  def has_assert(self):
    return bool(self.setting.assert_list)

  def has_assertex(self):
    return bool(self.setting.assertex_list)

  def do_select(self):
    params = self.setting.params
    driver = drivers[params.driver]
    try:
      conn = driver.connect(host=params.host, port=params.port, db=params.db,
          user=params.user, password=params.password)
      cursor = conn.cursor()

      self.result["rowcount"] = cursor.execute(params.sql)
      self.result["rows"] = [list(row) for row in cursor.fetchall()]

      cursor.close()

      # connectionManager的なのを作ったら個別のcloseはしない
      conn.close()
    except Exception as e:
      self.exception = e

  def do_selectdict(self):
    params = self.setting.params
    driver = drivers[params.driver]
    try:
      conn = driver.connect(host=params.host, port=params.port, db=params.db,
          user=params.user, password=params.password)
      cursor = conn.cursor(driver.dict_cursor())

      self.result["rowcount"] = cursor.execute(params.sql)
      self.result["rows"] = list(cursor.fetchall())

      cursor.close()

      # connectionManager的なのを作ったら個別のcloseはしない
      conn.close()
    except Exception as e:
      self.exception = e

  def do_update(self):
    params = self.setting.params
    driver = drivers[params.driver]

    # update 文は複数実行できるようにする
    if not isinstance(params.sql, list):
      params.sql = [params.sql]

    try:
      conn = driver.connect(host=params.host, port=params.port, db=params.db,
          user=params.user, password=params.password)

      for sql in params.sql:
        # 複数個あるときは結果が上書きされる
        cursor = conn.cursor(driver.dict_cursor())
        self.result["rowcount"] = cursor.execute(params.sql)
        self.result["rows"] = []
        cursor.close()

      # connectionManager的なのを作ったら個別のcloseはしない
      conn.close()
    except Exception as e:
      self.exception = e
