# -*- coding: utf-8 -*-
from baseaction import BaseAction
import datetime
import pprint
import re
import util

_UNICODE_REGEXP = re.compile(r"\\u([0-9a-f]{4})")


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

  def do_rawprint(self, global_env, scenario, **params):
    """ 与えられた値を文字列化して表示する

    .. code-block:: yaml

       - サンプルシナリオ

       - action: debug  # 省略時は rawprint の呼び出し
         v1: "1 + 2 + 3" #=> 1 + 2 + 3 と表示

    """
    self._write(global_env, scenario, params)

  def do_debug(self, global_env, scenario, **params):
    """ do_rawprint の省略呼び出し """
    self.do_rawprint(global_env, scenario, **params)

  def do_print(self, global_env, scenario, **params):
    """ 与えられた文字列値を python の基本データ型のリテラルとして解釈した後に print する

    .. code-block:: yaml

       - サンプルシナリオ

       - action: debug.print
         v1: "1 + 2 + 3" #=> 6 と表示
         v2: "[1, 2] + [3, 4]" #=> [1, 2, 3, 4] と表示
    """
    dump = {}
    for key, value in params.items():
      if isinstance(value, util.basestring):
        try:
          # debug中で任意のコードが実行されないように、
          # ビルトイン関数を無効にしてリテラルと一部の式だけ解釈できるようにする
          dump[key] = eval(value, {'__builtins__':{}}, {})
        except Exception:
          dump[key] = util.unicode(value)
      else:
        dump[key] = value
    self._write(global_env, scenario, dump)

  def _write(self, global_env, scenario, params):
    formatter = global_env['formatter']
    params['__file__'] = scenario.setting.filename
    params['__index__'] = global_env['action_index']
    formatter.debug("\nDEBUG - {0}".format(datetime.datetime.now()))
    formatter.debug(self._pp(params))

  @staticmethod
  def _pp(obj):
    # 日本語を pprint で表示しようとすると、
    # 以下のように文字コードで表示されてしまうため置換する
    # 'row1': u'\u6570\u5b66\u30ac\u30fc\u30eb'
    pstr = pprint.pformat(obj, width=80, indent=2)
    return _UNICODE_REGEXP.sub(lambda x: util.unichr(int("0x" + x.group(1), 16)), pstr)

