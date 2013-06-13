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
from scenariofilter import TagFilter
from scenarioloader import ScenarioLoadError
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
  if not option.targets and not option.interactive:
    option.print_help()
    return

  if option.without_color:
    stdout = Stdout(option.without_debug)
  else:
    stdout = ColoredStdout(option.without_debug)

  formatter = Tap(stdout)
  global_env = init(formatter)

  if option.interactive:
    result = run_console(global_env)
  else:
    result = run_scenario(global_env)

  teardown()
  sys.exit(result)


def run_scenario(global_env):
  formatter = global_env['formatter']
  failed = False
  try:
    agg = Aggregator()
    agg.add_filter(TagFilter(option.tags))
    agg.add_files(option.targets)
  except ScenarioLoadError as e:
    formatter.writer.write("{0}({1}):\n  {2}\n\n".format(e.__class__.__name__, e.error, e.filename))
    formatter.writer.write(util.unicode(e) + "\n")
    failed = True

  runner = ScenarioRunner(agg, formatter)
  failed = failed or runner.run(global_env)

  return int(failed)

def run_console(global_env):
  import console
  console.run(global_env)
  return 0

def teardown():
  for action_klass in action_loader.get_all_action_map().values():
    teardown_method = type.__getattribute__(action_klass, 'teardown')
    teardown_method()


if __name__ == '__main__':
  main()

