# -*- coding: utf-8 -*-
from baseaction import BaseAction
from scenarioloader import scenario_loader
import os

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
    path = path.strip()
    if not path:
      raise Exception(path + " not exists")

    if not os.path.isabs(path):
      path = os.path.join(os.path.dirname(scenario.setting.filename), path)

    new_scenario = scenario_loader.load_file(path, scenario)
    new_scenario.run(global_env)
    self.new_scenario = new_scenario

