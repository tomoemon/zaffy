# -*- coding: utf-8 -*-
from os import path
from baseaction import BaseAction
from moduleloader import load_module_dir

drivers = {}
modules, errors = load_module_dir(path.join("actions", "sqldrivers"))
for module in modules:
  klass = getattr(module, module.__name__.title())
  drivers[module.__name__] = klass()


class Sql(BaseAction):

  DEFAULT_PORT = 3306

  is_pool_connection = False

  @classmethod
  def setup(cls, config):
    pass

  @classmethod
  def teardown(cls):
    pass

  def do_select(self, driver, host, db, user, password, sql, port=DEFAULT_PORT):
    driver = drivers[driver]
    conn = driver.connect(host=host, port=port, db=db,
                          user=user, password=password)
    cursor = conn.cursor()

    self.result["rowcount"] = cursor.execute(sql)
    self.result["rows"] = [list(row) for row in cursor.fetchall()]

    cursor.close()

    # connectionManager的なのを作ったら個別のcloseはしない
    conn.close()

  def do_selectdict(self, driver, host, db, user, password, sql, port=DEFAULT_PORT):
    driver = drivers[driver]
    conn = driver.connect(host=host, port=port, db=db,
                          user=user, password=password)
    cursor = conn.cursor(driver.dict_cursor())

    self.result["rowcount"] = cursor.execute(sql)
    self.result["rows"] = list(cursor.fetchall())

    cursor.close()

    # connectionManager的なのを作ったら個別のcloseはしない
    conn.close()

  def do_update(self, driver, host, db, user, password, sql, port=DEFAULT_PORT):
    driver = drivers[driver]

    # update 文は複数実行できるようにする
    if not isinstance(sql, list):
      sql = [sql]

    conn = driver.connect(host=host, port=port, db=db,
                          user=user, password=password)

    for sql_unit in sql:
      # 複数個あるときは結果が上書きされる
      cursor = conn.cursor()
      self.result["rowcount"] = cursor.execute(sql_unit)
      self.result["rows"] = []
      conn.commit()
      cursor.close()

    # connectionManager的なのを作ったら個別のcloseはしない
    conn.close()

