# -*- coding: utf-8 -*-

try:
  import sys
  sys.setdefaultencoding('utf-8')
except:
  pass
finally:
  import site

import option
from configloader import ConfigLoader
from actionloader import action_loader
from aggregator import Aggregator
from scenariorunner import ScenarioRunner
from formatter.tap import Tap
from writer.stdout import Stdout

def init(formatter):
  action_loader.load_actions()
  for error in action_loader.load_error_list:
    formatter.debug("action import: " + unicode(error))

  if option.config_file:
    formatter.debug("config file: " + option.config_file)

  config_loader = ConfigLoader(option.config_file)
  config_loader.setup_klass(action_loader.get_all_action_map())

  env = {"formatter": formatter}
  env.update(action_loader.get_all_action_map())
  return env

def main():
  formatter = Tap(Stdout())
  global_env = init(formatter)

  agg = Aggregator()
  agg.add_files(option.targets)

  runner = ScenarioRunner(agg, formatter)
  runner.run(global_env)

  teardown()

def teardown():
  for action_klass in action_loader.get_all_action_map().values():
    teardown_method = type.__getattribute__(action_klass, 'teardown')
    teardown_method()

if __name__ == '__main__':
  main()
