# -*- coding: utf-8 -*-
from baseaction import BaseAction
from pprint import pformat, pprint
import datetime

class Debug(BaseAction):
  """ debug アクション
  """
  default_params = {
    "*":""
  }

  def do_print(self, params):
    var_str = pformat(params, width=60)
    print("<{2}\nDEBUG: {0}\n  {1}\n".format(datetime.datetime.now(), var_str, self.scenario.setting.filename))

