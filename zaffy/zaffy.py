# -*- coding: utf-8 -*-
import yaml
import sys
from scenario import Scenario
from pprint import pprint

def load_yaml():
  return yaml.load_all(file(sys.argv[1]))

def create_action(raw_obj):
  if 'action' not in raw_obj:
    raise Exception("no action")
  action, method = raw_obj['action'].split(".")
  class_name = action.title()
  setting_name = action.title() + "Setting"
  module = __import__("actions." + action, fromlist=[class_name, setting_name])
  setting_obj = getattr(module, setting_name)()
  setting_obj.set_params(raw_obj)
  setting_obj.set_method(method)
  action_obj = getattr(module, class_name)(setting_obj)
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
  for action in actions:
    print action.setting.__dict__
    #pprint(action.result)

if __name__ == '__main__':
  main()
