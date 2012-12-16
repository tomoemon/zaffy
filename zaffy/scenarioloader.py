# -*- coding: utf-8
import yaml
from scenario import Scenario
from scenariosetting import ScenarioSetting
from actionloader import action_loader
from os import path

class ScenarioLoader(object):

  def check_circular_reference(self, filename, from_scenario):
    """ 循環参照チェック """
    refer_list = [filename]
    while from_scenario:
      from_filename = from_scenario.setting.filename
      if from_filename in refer_list:
        refer_list.append(from_filename)
        raise Exception("Circular reference detected: " + str(list(reversed(refer_list))))
      refer_list.append(from_filename)
      from_scenario = from_scenario.setting.from_scenario

  def load_file(self, filename, from_scenario=None):
    filename = path.normcase(path.abspath(filename))
    if from_scenario:
      self.check_circular_reference(filename, from_scenario)
    with open(filename) as fp:
      raw_scenario = list(self.load_yaml(fp))
      scenario = self.parse(raw_scenario)
    scenario.setting.filename = filename
    scenario.setting.from_scenario = from_scenario
    return scenario

  def parse(self, content):
    raw_actions = content[0]
    doc = raw_actions.pop(0)
    if not isinstance(doc, basestring):
      raise Exception("Scenario should have a description at first element: " + str(content))

    setting = ScenarioSetting(doc=doc)
    return Scenario(setting, self.create_actions(raw_actions))

  def load_yaml(self, content):
    """ string でも file でも同じメソッドで読みこめる """
    #print(getattr(content, 'name', content))
    return yaml.load_all(content)

  def create_actions(self, actions):
    result = []
    for action in actions:
      result.append(action_loader.create_action(action))
    return result

scenario_loader = ScenarioLoader()

