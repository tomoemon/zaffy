# -*- coding: utf-8 -*-
import option
from configloader import ConfigLoader
from actionloader import action_loader
from aggregator import Aggregator
from scenariorunner import ScenarioRunner
from formatter.tap import Tap
from writer.stdout import Stdout

def init():
  action_loader.load_actions()

  if option.config_file:
    print("# using config file: " + option.config_file + "\n")
  config_loader = ConfigLoader(option.config_file)
  config_loader.apply_config_to_klass(action_loader.get_all_action_map())

  env = {}
  env.update(action_loader.get_all_action_map())
  return env

def main():
  global_env = init()

  agg = Aggregator()
  agg.add_files(option.targets)

  formatter = Tap(Stdout())
  global_env['formatter'] = formatter

  runner = ScenarioRunner(agg, formatter)
  runner.run(global_env)


if __name__ == '__main__':
  main()
