# -*- coding: utf-8 -*-


class ActionSetting(object):
  def __init__(self):
    self._method = None
    self._action_params = None
    self.params = None
    self.assert_list = None
    self.assertex_list = None

  def set_method(self, method):
    self._method = method

  def set_params(self, action_params):
    self._action_params = action_params

  def expand(self, global_env):
    self._action_params.expand(global_env)
    self.params = self._action_params.params
    self.assert_list = self._action_params.assert_list
    self.assertex_list = self._action_params.assertex_list

