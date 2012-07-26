# -*- coding: utf-8 -*-

from os import path
from baseaction import BaseAction
from actionparamsetting import ActionParamSetting
from moduleloader import load_module_dir

drivers = {}
modules = load_module_dir(path.join("actions", "sqldrivers"))
for module in modules:
  klass = getattr(module, module.__name__.title())
  drivers[module.__name__] = klass()

class Sql(BaseAction):

  DEFAULT_PORT = 3306

  param_setting = ActionParamSetting(
      allow_any_params=False,
      required=["driver", "host", "db", "user", "password", "sql"],
      optional={'port': DEFAULT_PORT}
      )

  def do_select(self, params):
    driver = drivers[params.driver]
    conn = driver.connect(host=params.host, port=params.port, db=params.db,
        user=params.user, password=params.password)
    cursor = conn.cursor()

    self.result["rowcount"] = cursor.execute(params.sql)
    self.result["rows"] = [list(row) for row in cursor.fetchall()]

    cursor.close()

    # connectionManager的なのを作ったら個別のcloseはしない
    conn.close()

  def do_selectdict(self, params):
    driver = drivers[params.driver]
    conn = driver.connect(host=params.host, port=params.port, db=params.db,
        user=params.user, password=params.password)
    cursor = conn.cursor(driver.dict_cursor())

    self.result["rowcount"] = cursor.execute(params.sql)
    self.result["rows"] = list(cursor.fetchall())

    cursor.close()

    # connectionManager的なのを作ったら個別のcloseはしない
    conn.close()

  def do_update(self, params):
    driver = drivers[params.driver]

    # update 文は複数実行できるようにする
    if not isinstance(params.sql, list):
      params.sql = [params.sql]

    conn = driver.connect(host=params.host, port=params.port, db=params.db,
        user=params.user, password=params.password)

    for sql in params.sql:
      # 複数個あるときは結果が上書きされる
      cursor = conn.cursor()
      self.result["rowcount"] = cursor.execute(sql)
      self.result["rows"] = []
      conn.commit()
      cursor.close()

    # connectionManager的なのを作ったら個別のcloseはしない
    conn.close()

