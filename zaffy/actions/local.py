# -*- coding: utf-8 -*-
from baseaction import BaseAction


class Local(BaseAction):
  """ Local アクション

  シナリオ単位のローカル変数を保存する
  """
  def do_local(self, scenario, **kwargs):
    """ do_set の省略呼び出し """
    self.do_set(scenario, **kwargs)

  def do_set(self, scenario, **kwargs):
    """ set """
    for key, value in kwargs.items():
      scenario.localvar[key] = value

    self.result = dict(scenario.localvar)

