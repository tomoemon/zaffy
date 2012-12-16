# -*- coding: utf-8 -*-
import os
import sys
from template import assert_test
from assertionfailed import AssertionFailed
from baseaction import ActionException

class Scenario(object):
  def __init__(self, setting, actions):
    self.setting = setting
    self.actions = actions

  def run(self, global_env):
    global_env["scenario"] = self
    last_action = None
    for action_index, action in enumerate(self.actions):
      global_env["actions"] = self.actions[0:action_index]
      global_env["last"] = last_action
      global_env["this"] = action
      try:
        action.run_action(global_env)
        action.run_assert(global_env)
      except (ActionException, AssertionFailed) as e:
        e.action_index = action_index
        raise e

      last_action = action

