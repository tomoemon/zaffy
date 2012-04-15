# -*- coding: utf-8 -*-
import sys
from template import assert_test
from assertionfailed import AssertionFailed

class Scenario(object):
  def __init__(self, actions):
    self.actions = actions

  def run(self, global_env):
    for action_index, action in enumerate(self.actions):
      action._run(global_env)

      try:
        action._assert()
      except AssertionFailed as e:
        e.action_index = action_index
        raise e

