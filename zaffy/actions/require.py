# -*- coding: utf-8 -*-
from baseaction import BaseAction
from actionparamsetting import ActionParamSetting
from scenarioloader import scenario_loader
from os import path

class Require(BaseAction):
  """ require アクション
  """
  param_setting = ActionParamSetting(
      allow_any_params=False,
      required=['path']
      )

  @classmethod
  def get_param_setting(cls, method_name):
    return cls.param_setting

  def __init__(self, setting):
    super(Require, self).__init__(setting)
    self.new_scenario = None

  def __getitem__(self, index):
    return self.new_scenario.actions[index]

  def do_require(self, params, global_env, scenario):
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

  def _run_dynamic_method(self, global_env, scenario):
    """ オーバーライド """
    getattr(self, "do_" + self.setting._method)(self.params, global_env, scenario)

