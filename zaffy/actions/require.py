# -*- coding: utf-8 -*-
from baseaction import BaseAction
from scenarioloader import scenario_loader
from os import path
import time

class Require(BaseAction):
  """ require アクション
  """
  default_params = {
    "path":"",
    "source":""
  }

  def __init__(self, setting):
    super(Require, self).__init__(setting)
    self.new_scenario = None

  def __getitem__(self, index):
    return self.new_scenario.actions[index]

  def do_require(self, params, global_env):
    params.path = params.path.strip()
    if not params.path:
      raise Exception(params.path + " not exists")

    filename = params.path

    if not path.isabs(filename):
      filename = path.join(path.dirname(self.scenario.setting.filename), filename)

    new_scenario = scenario_loader.load_file(filename, self.scenario)
    new_scenario.run(global_env)
    self.new_scenario = new_scenario

  def _run_dynamic_method(self, global_env):
    """ オーバーライド """
    getattr(self, "do_" + self.setting._method)(self.params, global_env)

