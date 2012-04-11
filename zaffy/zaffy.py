# -*- coding: utf-8 -*-
import yaml
import sys
from scenario import Scenario
from actionsetting import ActionSetting
from pprint import pprint

def load_yaml():
  return yaml.load_all(file(sys.argv[1]))

def create_action(raw_obj):
  if 'action' not in raw_obj:
    raise Exception("no action")
  action, method = raw_obj['action'].split(".")
  class_name = action.title()
  module = __import__("actions." + action, fromlist=[class_name])
  action_klass = getattr(module, class_name)
  setting_obj = ActionSetting()
  setting_obj.set_params(raw_obj, action_klass.default_params)
  setting_obj.set_method(method)
  action_obj = action_klass(setting_obj)
  return action_obj

def create_actions(actions):
  result = []
  for action in actions:
    result.append(create_action(action))
  return result

def main():
  obj = list(load_yaml())
  actions = create_actions(obj[0]['actions'])
  s = Scenario(actions)
  s.run()

if __name__ == '__main__':
  main()
