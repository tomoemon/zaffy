# -*- coding: utf-8
import yaml
from scenario import Scenario
from actionloader import action_loader

class ScenarioLoader(object):

  def load(self, filename):
    yaml_obj = list(self.load_yaml(filename))
    raw_actions = yaml_obj[0]
    doc = raw_actions.pop(0)
    if not isinstance(doc, basestring):
      raise Exception("Scenario should have a description at first element")
    return Scenario(doc, self.create_actions(raw_actions))

  def load_yaml(self, filename):
    print filename
    return yaml.load_all(file(filename))

  def create_actions(self, actions):
    result = []
    for action in actions:
      result.append(action_loader.create_action(action))
    return result

