# -*- coding: utf-8 -*-
import sys
from template import assert_test
from assertionfailed import AssertionFailed

class Scenario(object):
  def __init__(self, setting):
    self.setting = setting

  def run(self, global_env):
    last_action = None
    actions = self.setting.actions
    for action_index, action in enumerate(actions):
      global_env["last"] = last_action
      action.run_action(global_env)

      try:
        action.run_assert()
      except AssertionFailed as e:
        e.action_index = action_index
        raise e

      last_action = action

