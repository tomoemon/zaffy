# -*- coding: utf-8 -*-
from baseaction import BaseAction
from scenarioloader import scenario_loader
from os import path

class Require(BaseAction):
  """ require アクション
  """
  root_path = None

  @classmethod
  def apply_config(cls, root_path=None):
    cls.root_path = root_path

  def __init__(self, setting):
    super(Require, self).__init__(setting)
    self.new_scenario = None

  def __getitem__(self, index):
    return self.new_scenario.actions[index]

  def do_require(self, path, global_env, scenario):
    params.path = params.path.strip()
    print params.path
    if not params.path:
      raise Exception(params.path + " not exists")

    filename = params.path

    if not path.isabs(filename):
      filename = path.join(path.dirname(scenario.setting.filename), filename)

    new_scenario = scenario_loader.load_file(filename, scenario)
    new_scenario.run(global_env)
    self.new_scenario = new_scenario

