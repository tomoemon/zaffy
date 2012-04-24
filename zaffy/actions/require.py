# -*- coding: utf-8 -*-
from baseaction import BaseAction
from scenarioloader import scenario_loader
from os import path

class Require(BaseAction):
  """ require アクション
  """
  default_params = {
    "path":""
    "source":""
  }

  def do_string(self):
    pass

  def do_action(self):
    params = self.setting.params
    params.path = params.path.trim()
    if not params.path:
      raise Exception(params.path + " not exists")

    filename = params.path

    if not path.isabs(filename):
      filename = path.join(path.dirname(self.scenario_setting), filename)

    samefile = getattr(path, 'samefile', self.samefile)

    if samefile(filename, self.scenario_setting.filename):
      raise Exception(params.path + " require self")

    scenario = scenario_loader.load_file(params.path)
    scenario.run(global_env)

  @classmethod
  def samefile(cls, path1, path2):
    return path.normcase(path.abspath(path1)) == \
        path.normcase(path.abspath(path2)):

  def run_action(self, global_env, scenario_setting):
    # 変数を jinja2 で展開する
    # constなどアクションを実行する最中に値が変わるものがあるので、直前じゃないとダメ
    self.setting.expand(global_env)
    self.scenario_setting = scenario_setting
    self.start_time = time.time()
    try:
      getattr(self, "do_" + self.setting._method)(global_env)
    except Exception as e:
      self.exception = e
    finally:
      self.end_time = time.time()
      self.result["execution_time"] = self.end_time - self.start_time

