# -*- coding: utf-8 -*-
from os import path
from baseaction import BaseAction
from moduleloader import load_module_dir

_drivers = {}


class Sql(BaseAction):
  """ Sql アクション

  SQL に準拠した Database に対してクエリを実行する

  .. note::

    接続先パスワードなどは :ref:`references-actions-preset-label` で定義しておくと、毎回記述する必要がなくなります。
  """

  _DEFAULT_PORT = 3306

  is_pool_connection = False

  @classmethod
  def setup(cls, config):
    global _drivers
    modules, errors = load_module_dir(path.join("actions", "sqldrivers"))
    for module in modules:
      klass = getattr(module, module.__name__.title())
      _drivers[module.__name__] = klass()

  @classmethod
  def teardown(cls):
    pass

  def do_select(self, driver, sql, db, host=None, user=None, password=None, port=_DEFAULT_PORT):
    """ 参照系のクエリ(SELECT, SHOW など)を実行し、タプル形式で結果を取得する

    .. code-block:: yaml

      - サンプルシナリオ

      - action: sql.select
        driver: mysql
        host: localhost
        db: user_db
        user: root
        password: hogehoge
        sql: select * from user where user_id=1
        assert:
         - >
          res.rows[0] is eq
            (1, "nanoha", "2012-04-10 15:57:26"|todatetime, "2012-04-10 15:57:26"|todatetime)

    :param string driver: データベースのドライバ (``mysql`` または ``sqlite`` のみ指定可能)
    :param string sql: 実行するSQL文
    :param string db: データベース名
    :param string host: データベースホスト名 (``mysql`` のみ)
    :param string user: DB接続のためのユーザ (``mysql`` のみ)
    :param string password: DB接続のためのパスワード (``mysql`` のみ)
    :param int port: DB接続先のポート番号 (``mysql`` のみ)
    :return: - **rowcount** (*int*) - 取得した行数
             - **rows** (*list*) - 取得した行(tuple)のリスト
    """
    driver = _drivers[driver]
    conn = driver.connect(host=host, port=port, db=db,
                          user=user, password=password)
    cursor = conn.cursor(driver.base_cursor())

    cursor.execute(sql)
    self.result["rows"] = list(cursor.fetchall())
    self.result["rowcount"] = len(self.result['rows'])

    cursor.close()

    # connectionManager的なのを作ったら個別のcloseはしない
    conn.close()

  def do_selectdict(self, driver, sql, db, host=None, user=None, password=None, port=_DEFAULT_PORT):
    """ 参照系のクエリ(SELECT, SHOW など)を実行し、辞書形式で結果を取得する

    .. code-block:: yaml

      - サンプルシナリオ

      - action: sql.selectdict
        driver: mysql
        host: localhost
        db: user_db
        user: root
        password: hogehoge
        sql: select * from user where user_id=1
        assert:
         - >
          res.rows[0] is eq
            {
             'user_id': 1,
             'user_name': "nanoha",
             'created_date': "2012-04-10 15:57:26"|todatetime,
             'updated_date': "2012-04-10 15:57:26"|todatetime
            }


    :param string driver: データベースのドライバ (``mysql`` または ``sqlite`` のみ指定可能)
    :param string sql: 実行するSQL文
    :param string db: データベース名
    :param string host: データベースホスト名 (``mysql`` のみ)
    :param string user: DB接続のためのユーザ (``mysql`` のみ)
    :param string password: DB接続のためのパスワード (``mysql`` のみ)
    :param int port: DB接続先のポート番号 (``mysql`` のみ)
    :return: - **rowcount** (*int*) - 取得した行数
             - **rows** (*list*) - 取得した行(dict)のリスト、行のキーはカラム名に対応する
    """
    driver = _drivers[driver]
    conn = driver.connect(host=host, port=port, db=db,
                          user=user, password=password)
    cursor = conn.cursor(driver.dict_cursor())

    cursor.execute(sql)
    self.result["rows"] = list(cursor.fetchall())
    self.result["rowcount"] = len(self.result['rows'])

    cursor.close()

    # connectionManager的なのを作ったら個別のcloseはしない
    conn.close()

  def do_update(self, driver, sql, db, host=None, user=None, password=None, port=_DEFAULT_PORT):
    """ 更新系のクエリ(UPDATE, INSERT など)を実行する

    .. code-block:: yaml

      - サンプルシナリオ

      - action: sql.update
        driver: mysql
        host: localhost
        db: user_db
        user: root
        password: hogehoge
        sql: update user set user_name="fate" where user_id=1
        assert:
         - res.rowcount is eq 1

    :param string driver: データベースのドライバ  (``mysql`` または ``sqlite`` のみ指定可能)
    :param string|list sql: 実行するSQL文。リストを渡した場合は複数実行する
    :param string db: データベース名
    :param string host: データベースホスト名 (``mysql`` のみ)
    :param string user: DB接続のためのユーザ (``mysql`` のみ)
    :param string password: DB接続のためのパスワード (``mysql`` のみ)
    :param int port: DB接続先のポート番号 (``mysql`` のみ)
    :return: - **rowcount** (*int*) - 更新した行数、``sql`` に複数のSQL文を渡した場合は最後に実行した結果
             - **rows** (*list*) - 空リスト
    """
    driver = _drivers[driver]

    # update 文は複数実行できるようにする
    if not isinstance(sql, list):
      sql = [sql]

    conn = driver.connect(host=host, port=port, db=db,
                          user=user, password=password)

    for sql_unit in sql:
      # 複数個あるときは結果が上書きされる
      cursor = conn.cursor()

      cursor.execute(sql_unit)
      self.result["rowcount"] = cursor.rowcount
      self.result["rows"] = []
      conn.commit()
      cursor.close()

    # connectionManager的なのを作ったら個別のcloseはしない
    conn.close()

