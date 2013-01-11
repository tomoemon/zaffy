# -*- coding: utf-8 -*-
from baseaction import BaseAction
from scenarioloader import scenario_loader
import os

class Require(BaseAction):
  """ require アクション
  """
  root_path = None

  @classmethod
  def setup(cls, root_path=None):
    cls.root_path = root_path

  def __init__(self, setting):
    super(Require, self).__init__(setting)

  def __getitem__(self, index):
    return self.result['actions'][index]

  def do_require(self, path, global_env, scenario, params=None):
    path = path.strip()
    if not path:
      raise Exception(path + " not exists")

    if not os.path.isabs(path):
      path = os.path.join(os.path.dirname(scenario.setting.filename), path)

    new_scenario = scenario_loader.load_file(path, scenario)
    new_scenario.localvar = params if params else {}
    new_scenario.run(global_env)
    self.result = new_scenario.actions[-1].result

