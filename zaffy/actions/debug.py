# -*- coding: utf-8 -*-
from baseaction import BaseAction
import datetime
import pprint
import re


class Debug(BaseAction):
  """ debug アクション
  """

  def do_rawprint(self, global_env, scenario, **params):
    self._write(global_env, scenario, params)

  def do_debug(self, global_env, scenario, **params):
    self.do_rawprint(global_env, scenario, **params)

  def do_print(self, global_env, scenario, **params):
    dump = {}
    for key, value in params.items():
      if isinstance(value, basestring):
        try:
          # debug中で任意のコードが実行されないように、
          # ビルトイン関数を無効にしてリテラルと一部の式だけ解釈できるようにする
          dump[key] = eval(value, {'__builtins__':{}}, {})
        except Exception:
          dump[key] = str(value)
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
    return re.sub(r"\\u([0-9a-f]{4})",
                  lambda x: unichr(int("0x" + x.group(1), 16)), pstr)
