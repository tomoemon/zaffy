# -*- coding: utf-8
import yaml
from scenario import Scenario
from actionsetting import ActionSetting

class ScenarioLoader(object):

  def load(self, filename):
    yaml_obj = list(self.load_yaml(filename))
    first_doc = yaml_obj[0]
    raw_actions = first_doc['actions']
    return Scenario(self.create_actions(raw_actions))

  def load_yaml(self, filename):
    print filename
    return yaml.load_all(file(filename))

  def create_action(self, raw_obj):
    if 'action' not in raw_obj:
      raise Exception("no action")
    action_name, method = raw_obj['action'].split(".")
    action_klass = self.get_action_klass(action_name)
    setting_obj = ActionSetting()
    setting_obj.set_params(raw_obj, action_klass.default_params)
    setting_obj.set_method(method)
    action_obj = action_klass(setting_obj)
    return action_obj

  def get_action_klass(self, action_name):
    class_name = action_name.title()
    module = __import__("actions." + action_name, fromlist=[class_name])
    action_klass = getattr(module, class_name)
    return action_klass

  def create_actions(self, actions):
    result = []
    for action in actions:
      result.append(self.create_action(action))
    return result

