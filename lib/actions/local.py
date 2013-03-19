# -*- coding: utf-8 -*-
from baseaction import BaseAction


class Local(BaseAction):
  """ Local アクション

  シナリオ単位のローカル変数を保存する

  上書き可能なローカル変数をシナリオ内で定義する。:ref:`references-actions-const-label` と異なるのは上書き可能な点と、シナリオ内でのみ有効な点。シナリオ A が、シナリオ B (local アクションを実行する) を :ref:`references-actions-require-label` しても、シナリオ A から B のローカル変数を参照することはできない (:ref:`references-actions-const-label` なら参照可能)
  """
  def do_local(self, scenario, **kwargs):
    """ do_set の省略呼び出し """
    self.do_set(scenario, **kwargs)

  def do_set(self, scenario, **kwargs):
    """ ローカル変数の定義

    .. code-block:: yaml

       - サンプルシナリオ

       - action: local
         user: taro
         pass: taropass

       - action: http.get
         url: http://yahoo.co.jp/
         params:
           user: <<local.user>>
           pass: <<local.pass>>

    :param any (any): 任意のキーで任意の値を指定する
    :return dict: 現在定義されているローカル変数の辞書を返す
  """
    for key, value in kwargs.items():
      scenario.localvar[key] = value

    self.result = dict(scenario.localvar)

