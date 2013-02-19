# -*- coding: utf-8 -*-
from baseaction import BaseAction
from scenarioloader import scenario_loader
from scenariosetting import ScenarioSetting
import os


class Require(BaseAction):
  """ Require アクション

  外部のシナリオファイルを読み込む
  """
  _root_path = ""

  @classmethod
  def setup(cls, config):
    cls._root_path = config.get('root_path', '')

  def __getitem__(self, index):
    return self.result['actions'][index]

  def do_require(self, path, global_env, scenario):
    """ パラメータなしの呼び出し """
    new_scenario = self._load(path, global_env, scenario, None)
    self.result = new_scenario.actions[-1].result

  def do_call(self, path, global_env, scenario, params=None):
    """ call パラメータ付き呼び出し """
    new_scenario = self._load(path, global_env, scenario, params)
    self.result = new_scenario.actions[-1].result

  def _load(self, path, global_env, scenario, params):
    path = path.strip()
    if not path:
      raise Exception(path + " not exists")

    if not os.path.isabs(path):
      if self._root_path:
        path = os.path.join(self._root_path, path)
      else:
        path = os.path.join(scenario.dir, path)

    new_scenario = scenario_loader.load(ScenarioSetting(path), scenario)
    new_scenario.localvar = params if params else {}
    new_scenario.run(global_env)
    return new_scenario

