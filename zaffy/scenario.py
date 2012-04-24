# -*- coding: utf-8 -*-
import sys
from template import assert_test
from assertionfailed import AssertionFailed

class Scenario(object):
  def __init__(self, setting, actions):
    self.setting = setting
    self.actions = actions

  def run(self, global_env):
    last_action = None
    global_env["actions"] = self.actions
    for action_index, action in enumerate(self.actions):
      global_env["last"] = last_action
      action.run_action(global_env, self.setting)

      try:
        action.run_assert()
      except AssertionFailed as e:
        e.action_index = action_index
        raise e

      last_action = action

