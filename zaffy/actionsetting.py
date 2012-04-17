# -*- coding: utf-8 -*-

class DotDict(dict):
  def __setattr__(self, name, value):
    self[name] = value

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
    if '*' in default_params:
      # * を指定している場合は任意のパラメータを受け取る
      for key, value in params.items():
        self.params[key] = value
    else:
      for key, value in default_params.items():
        self.params[key] = params.get(key, value)

    self.assert_list = params.get("assert", self.assert_list)
    if isinstance(self.assert_list, str):
      self.assert_list = [self.assert_list]

    self.assertex_list = params.get("assertex", self.assertex_list)
    if isinstance(self.assertex_list, str):
      self.assertex_list = [self.assertex_list]

