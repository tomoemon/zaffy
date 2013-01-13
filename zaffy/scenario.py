# -*- coding: utf-8 -*-
import os
import sys
from template import assert_test
from assertionfailed import AssertionFailed
from baseaction import ActionException


class Scenario(object):
  def __init__(self, setting, actions, parent=None):
    self.setting = setting
    self.actions = actions
    self.parent = parent
    self.localvar = {}

  def run(self, global_env):
    global_env["scenario"] = self
    global_env["local"] = self.localvar

    last_action = None
    for action_index, action in enumerate(self.actions):
      global_env["actions"] = self.actions[0:action_index]
      global_env["action_index"] = action_index
      global_env["last"] = last_action
      global_env["this"] = action
      try:
        action.run_action(global_env)
        action.run_assert(global_env)
      except (ActionException, AssertionFailed) as e:
        e.action_index = action_index
        raise e
      last_action = action

    global_env["scenario"] = self.parent
    global_env["local"] = self.parent.localvar if self.parent else None
