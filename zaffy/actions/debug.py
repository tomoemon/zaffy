# -*- coding: utf-8 -*-
from baseaction import BaseAction
import datetime
import pprint

class Debug(BaseAction):
  """ debug アクション
  """

  def do_rawprint(self, global_env, **params):
    self._write(global_env, params)

  def do_debug(self, global_env, **params):
    self.do_print(global_env, **params)

  def do_print(self, global_env, **params):
    dump = {}
    for key, value in params.items():
      if isinstance(value, basestring):
        try:
          # debug中で任意のコードが実行されないように、
          # ビルトイン関数を無効にしてリテラルと一部の式だけ解釈できるようにする
          dump[key] = eval(value, {'__builtins__':{}}, {})
        except Exception as e:
          dump[key] = str(value)
      else:
        dump[key] = value
    self._write(global_env, dump)

  def _write(self, global_env, params):
    formatter = global_env['formatter']
    formatter.debug("\nDEBUG at {0}".format(datetime.datetime.now()))
    formatter.debug(pprint.pformat(params, width=80, indent=2))

