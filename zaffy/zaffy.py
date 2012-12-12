# -*- coding: utf-8 -*-
import sys
import option
from configloader import ConfigLoader
from actionloader import action_loader
from scenarioloader import scenario_loader
from actionexception import ActionException
from assertionfailed import AssertionFailed

def main():
  action_loader.load_actions()
  global_env = {}
  global_env.update(action_loader.get_all_action_map())

  if option.config_file:
    print("using config file: " + option.config_file)
  config_loader = ConfigLoader(option.config_file)
  config_loader.apply_config_to_klass(action_loader.get_all_action_map())
  for target in option.targets:
    print("\n[running] " + target)
    try:
      scenario = scenario_loader.load_file(target)
      scenario.run(global_env)
    except AssertionFailed as e:
      print("FAILED!")
      print("  action_index: {0}".format(e.action_index))
      print("  assert_index: {0}".format(e.assert_index))
      print("  assertion: " + e.assertion)
      print("  compared: ")
      for i, items in enumerate(e.compared):
        for j, item in enumerate(items):
          print(u"    {0}-{1}: {2}".format(i, j, item))


if __name__ == '__main__':
  main()
