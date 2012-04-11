# -*- coding: utf-8 -*-

class DotDict(dict):
  def __getattr__(self, name):
    return self[name]

class ActionSetting(object):
  def __init__(self):
    self._parent = None
    self._method = None
    self.params = DotDict()
    self.assert_list = []
    self.assertex_list = []

  def set_method(self, method):
    self.method = method

  def set_params(self, params, default_params):
    for key, value in default_params.items():
      self.params[key] = params.get(key, value)

    self.assert_list = params.get("assert", self.assert_list)
    if isinstance(self.assert_list, str):
      self.assert_list = [self.assert_list]

    self.assertex_list = params.get("assertex", self.assertex_list)
    if isinstance(self.assertex_list, str):
      self.assertex_list = [self.assertex_list]

