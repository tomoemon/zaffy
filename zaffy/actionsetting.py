# -*- coding: utf-8 -*-
import template

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

  def expand(self, global_env):
    for key, value in self.params.items():
      self._expand_params(self.params, key, value, global_env)

  def _expand_params(self, parent, key, value, global_env):
    if isinstance(value, basestring):
      parent[key] = template.expand(value, global_env)
    elif isinstance(value, dict):
      for k, v in value.items():
        self._expand_params(value, k, v, global_env)
    elif isinstance(value, list):
      for k, v in enumerate(value):
        self._expand_params(value, k, v, global_env)

