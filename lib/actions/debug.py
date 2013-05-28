# -*- coding: utf-8 -*-
from baseaction import BaseAction
import debugprinter


class Debug(BaseAction):
  """ Debug アクション

  アクションの実行結果などデバッグ用の出力を行なう。
  事前に実行した別アクションの実行結果や関数実行結果の出力に用いる。

  .. code-block:: yaml

     - サンプルシナリオ

     - action: http.get
       url: http://yahoo.co.jp/

     # 直前のアクションの実行結果から HTTP STATUS を取得して表示
     - action: debug
       res: <<last.res.status>> #=> 200 と表示
  """

  def do_rawprint(self, global_env, **params):
    """ 与えられた値を文字列化して表示する

    .. code-block:: yaml

       - サンプルシナリオ

       - action: debug  # 省略時は rawprint の呼び出し
         v1: "1 + 2 + 3" #=> 1 + 2 + 3 と表示

    """
    global_env['debugprinter'].write(params)

  def do_debug(self, global_env, **params):
    """ do_rawprint の省略呼び出し """
    self.do_rawprint(global_env, **params)

  def do_print(self, global_env, **params):
    """ 与えられた文字列値を python の基本データ型のリテラルとして解釈した後に print する

    .. code-block:: yaml

       - サンプルシナリオ

       - action: debug.print
         v1: "1 + 2 + 3" #=> 6 と表示
         v2: "[1, 2] + [3, 4]" #=> [1, 2, 3, 4] と表示
    """
    global_env['debugprinter'].smart_write(params)

