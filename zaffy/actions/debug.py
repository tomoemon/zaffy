# -*- coding: utf-8 -*-
from baseaction import BaseAction
from actionparamsetting import ActionParamSetting
from pprint import pformat, pprint
import datetime

class Debug(BaseAction):
  """ debug アクション
  """

  param_setting = ActionParamSetting(
      allow_any_params=True
      )

  def do_rawprint(self, params, scenario):
    var_str = pformat(params, width=60)
    print("<{2}\nDEBUG: {0}\n  {1}\n".format(datetime.datetime.now(), var_str, scenario.setting.filename))

  def do_print(self, params, scenario):
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
    var_str = pformat(dump, width=60)
    print("<{2}\nDEBUG: {0}\n  {1}\n".format(datetime.datetime.now(), var_str, scenario.setting.filename))

  def _run_dynamic_method(self, global_env, scenario):
    """ オーバーライド """
    getattr(self, "do_" + self.setting._method)(self.params, scenario)
