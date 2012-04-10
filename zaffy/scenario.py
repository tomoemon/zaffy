# -*- coding: utf-8 -*-
from template import assert_test

class Scenario(object):
  def __init__(self, actions):
    self.actions = actions

  def run(self):
    for action in self.actions:
      action.run()
      if action.has_assert():
        self.test(action)

  def test(self, action):
    variables = {"this": action.result}
    for assert_str in action.setting.assert_list:
      if not assert_test(assert_str, variables):
        raise Exception(assert_str)


