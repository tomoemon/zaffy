#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
if sys.getdefaultencoding() == 'ascii':
  reload(sys)
  sys.setdefaultencoding('utf-8')
  delattr(sys, 'setdefaultencoding')

import option
from configloader import ConfigLoader
from actionloader import action_loader
from aggregator import Aggregator
from scenariorunner import ScenarioRunner
from formatter.tap import Tap
from writer.stdout import ColoredStdout, Stdout
from moduleloader import LoadError
import template
import util


def print_error_list(formatter, prefix, error):
  for error in error.error_list:
    formatter.debug(prefix + str(error))

def init(formatter):
  try:
    action_loader.load_actions()
  except LoadError as e:
    print_error_list(formatter, "action import: ", e)

  try:
    template.load_customtests()
  except LoadError as e:
    print_error_list(formatter, "customtests import: ", e)

  try:
    template.load_customfilters()
  except LoadError as e:
    print_error_list(formatter, "customfilters import: ", e)

  if option.config_file:
    formatter.debug("config file: " + option.config_file)

  config_loader = ConfigLoader(option.config_file)
  config_loader.setup_klass(action_loader.get_all_action_map())

  env = {"formatter": formatter}
  env.update(action_loader.get_all_action_map())
  return env


def main():
  if option.without_color:
    stdout = Stdout(option.without_debug)
  else:
    stdout = ColoredStdout(option.without_debug)
  formatter = Tap(stdout)
  global_env = init(formatter)
  if option.targets:
    agg = Aggregator()
    agg.add_files(option.targets)
    runner = ScenarioRunner(agg, formatter)
    failed = runner.run(global_env)
  else:
    import console
    console.run(global_env)
    failed = False

  teardown()

  if failed:
    sys.exit(1)

def teardown():
  for action_klass in action_loader.get_all_action_map().values():
    teardown_method = type.__getattribute__(action_klass, 'teardown')
    teardown_method()


if __name__ == '__main__':
  main()

