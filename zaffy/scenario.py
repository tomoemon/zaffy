# -*- coding: utf-8 -*-
from template import assert_test

class ScenarioException(Exception):
  pass

class Scenario(object):
  def __init__(self, actions):
    self.actions = actions

  def run(self):
    for action in self.actions:
      action.run()

      if action.has_assertex():
        self.assertex_test(action)
      elif action.exception:
        raise action.exception

      if action.has_assert():
        self.assert_test(action)

  def assertex_test(self, action):
    variables = {"ex": action.exception, "this": action.__dict__}
    for assert_str in action.setting.assertex_list:
      if not assert_test(assert_str, variables):
        raise AssertionError(assert_str)

  def assert_test(self, action):
    variables = {"res": action.result, "this": action.__dict__}
    for assert_str in action.setting.assert_list:
      if not assert_test(assert_str, variables):
        raise AssertionError(assert_str)


