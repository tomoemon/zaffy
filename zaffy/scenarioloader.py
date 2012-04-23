# -*- coding: utf-8
import yaml
from scenario import Scenario
from scenariosetting import ScenarioSetting
from actionloader import action_loader

class ScenarioLoader(object):

  def load_file(self, filename):
    scenario = self.load(file(filename))
    scenario.setting.filename = filename
    return scenario

  def load(self, content):
    yaml_obj = list(self.load_yaml(content))
    raw_actions = yaml_obj[0]
    doc = raw_actions.pop(0)
    if not isinstance(doc, basestring):
      raise Exception("Scenario should have a description at first element: " + content)

    setting = ScenarioSetting(doc=doc, actions=self.create_actions(raw_actions))
    return Scenario(setting)

  def load_yaml(self, content):
    """ string でも file でも同じメソッドで読みこめる """
    print content
    return yaml.load_all(content)

  def create_actions(self, actions):
    result = []
    for action in actions:
      result.append(action_loader.create_action(action))
    return result

