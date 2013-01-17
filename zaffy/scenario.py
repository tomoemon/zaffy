# -*- coding: utf-8 -*-
from assertionfailed import AssertionFailed
from baseaction import ActionException


class Scenario(object):
  def __init__(self, setting, doc, actions, parent=None):
    self.setting = setting
    self.doc = doc
    self.actions = actions
    self.finished_action_count = 0
    self.parent = parent
    self.localvar = {}

  def __getattr__(self, item):
    return getattr(self.setting, item)

  def run(self, global_env):
    global_env["scenario"] = self
    global_env["local"] = self.localvar

    while self.finished_action_count < len(self.actions):
      action = self.actions[self.finished_action_count]
      self._run_action(global_env, action)
      self.finished_action_count += 1

    if self.parent:
      global_env["scenario"] = self.parent
      global_env["local"] = self.parent.localvar

  def add_action(self, action):
    self.actions.append(action)

  def _last_action(self):
    if self.finished_action_count > 0:
      return self.actions[self.finished_action_count - 1]
    return None

  def _run_action(self, global_env, action):
    finished_count = self.finished_action_count

    global_env["actions"] = self.actions[0:finished_count]
    global_env["action_index"] = finished_count
    global_env["last"] = self._last_action()
    global_env["this"] = action
    try:
      action.run_action(global_env)
      action.run_assert(global_env)
    except (ActionException, AssertionFailed) as e:
      e.action_index = finished_count
      raise e

