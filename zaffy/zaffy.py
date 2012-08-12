# -*- coding: utf-8 -*-
import sys
import option
from configloader import ConfigLoader
from actionloader import action_loader
from scenarioloader import scenario_loader
from actionexception import ActionException

def main():
  action_loader.load_actions()
  global_env = {}
  global_env.update(action_loader.get_all_action_map())

  if option.config_file:
    print("using config file: " + option.config_file)
  config_loader = ConfigLoader(option.config_file)
  config_loader.apply_config_to_klass(action_loader.get_all_action_map())
  try:
    scenario = scenario_loader.load_file(option.targets[0])
    scenario.run(global_env)
  except ActionException as e:
    print "--------------------------"
    print(e.stack_trace)
    print(e.original)
    print "--------------------------"

if __name__ == '__main__':
  main()
