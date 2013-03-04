# -*- coding: utf-8 -*-
from baseaction import BaseAction
from scenarioloader import scenario_loader
from scenariosetting import ScenarioSetting
import os
import util


class Require(BaseAction):
  """ Require アクション

  外部のシナリオファイルを読み込む
  """
  _root_path = ""

  @classmethod
  def setup(cls, config):
    if 'root_path' in config:
      cls._root_path = os.path.abspath(config['root_path'])

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

  def do_repeat(self, path, global_env, scenario, params):
    """ call 繰り返し呼び出し """
    for param in params:
      self.do_call(path, global_env, scenario, param)

  @staticmethod
  def _replace_root(src_path, new_root):
    split = os.path.split
    head = tail = src_path
    while tail:
      head, tail = split(head)
    return os.path.join(new_root, src_path[len(head):])

  @staticmethod
  def _to_dict(params):
    if isinstance(params, dict):
      return params
    elif isinstance(params, list):
      return dict(enumerate(params))
    elif isinstance(params, (util.basestring, int, bool)):
      return {0: params}
    return {}

  def _load(self, path, global_env, scenario, params):
    path = path.strip()
    if not path:
      raise Exception(path + " not exists")

    if os.path.isabs(path):
      if self._root_path:
        path = self._replace_root(path, self._root_path)
    else:
        path = os.path.join(scenario.dir, path)

    new_scenario = scenario_loader.load(ScenarioSetting(path), scenario)
    new_scenario.localvar = self._to_dict(params)
    new_scenario.run(global_env)
    return new_scenario

