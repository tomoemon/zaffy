# -*- coding: utf-8 -*-
from os import path
from baseaction import BaseAction
from moduleloader import load_module_dir

drivers = {}

class Sql(BaseAction):
  """ Sql アクション

  SQL に準拠した DB に対してクエリを実行する
  """

  _DEFAULT_PORT = 3306

  is_pool_connection = False

  @classmethod
  def setup(cls, config):
    global drivers
    modules, errors = load_module_dir(path.join("actions", "sqldrivers"))
    for module in modules:
      klass = getattr(module, module.__name__.title())
      drivers[module.__name__] = klass()

  @classmethod
  def teardown(cls):
    pass

  def do_select(self, driver, host, db, user, password, sql, port=_DEFAULT_PORT):
    """ select """
    driver = drivers[driver]
    conn = driver.connect(host=host, port=port, db=db,
                          user=user, password=password)
    cursor = conn.cursor()

    self.result["rowcount"] = cursor.execute(sql)
    self.result["rows"] = [list(row) for row in cursor.fetchall()]

    cursor.close()

    # connectionManager的なのを作ったら個別のcloseはしない
    conn.close()

  def do_selectdict(self, driver, host, db, user, password, sql, port=_DEFAULT_PORT):
    """ dict 形式で結果を取得する select """
    driver = drivers[driver]
    conn = driver.connect(host=host, port=port, db=db,
                          user=user, password=password)
    cursor = conn.cursor(driver.dict_cursor())

    self.result["rowcount"] = cursor.execute(sql)
    self.result["rows"] = list(cursor.fetchall())

    cursor.close()

    # connectionManager的なのを作ったら個別のcloseはしない
    conn.close()

  def do_update(self, driver, host, db, user, password, sql, port=_DEFAULT_PORT):
    """ update (delete, insert 等の更新系クエリ) """
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

