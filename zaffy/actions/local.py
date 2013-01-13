# -*- coding: utf-8 -*-
from baseaction import BaseAction


class Local(BaseAction):
  """ Localアクション
  scenario単位のローカル変数を保存するアクション
  """
  def do_local(self, scenario, **kwargs):
    self.do_set(scenario, **kwargs)

  def do_set(self, scenario, **kwargs):
    for key, value in kwargs.items():
      scenario.localvar[key] = value

    self.result = scenario.localvar

