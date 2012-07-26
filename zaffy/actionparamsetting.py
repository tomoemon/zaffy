# -*- coding: utf-8 -*-
import template
import ast

class DotDict(dict):
  def __setattr__(self, name, value):
    self[name] = value

  def __getattr__(self, name):
    return self.get(name, None)

class ActionParamSetting(object):
  def __init__(self, allow_any_params, required=[], optional={}):
    self.allow_any_params = allow_any_params
    self.required = required
    self.optional = optional
    self.optional.update({'assert':[], 'assertex':[]})

class ActionParams(object):
  def __init__(self, param_setting, raw_params, preset):
    self.param_setting = param_setting
    self.raw_params = raw_params
    self.preset = preset
    self.params = None
    self.assert_list = None
    self.assertex_list = None

  def expand(self, global_env):
    self.params = self.preset.apply(self.raw_params)
    for key, value in self.params.items():
      self._expand_params(self.params, key, value, global_env)

    exists_keys = self.params.keys()
    for required_param in self.param_setting.required:
      if required_param not in self.params:
        raise Exception("required: " + required_param)
      exists_keys.remove(required_param)

    for optional_param, value in self.param_setting.optional.items():
      if optional_param in self.params:
        exists_keys.remove(optional_param)
      else:
        self.params[optional_param] = value

    if not self.param_setting.allow_any_params and exists_keys:
      raise Exception("unknown param: " + exists_keys[0])

    self.assert_list = self.params.get('assert', [])
    if isinstance(self.assert_list, basestring):
      self.assert_list = [self.assert_list]
    self.assertex_list = self.params.get('assertex', [])
    if isinstance(self.assertex_list, basestring):
      self.assertex_list = [self.assertex_list]
    self.params.pop('assert', None)
    self.params.pop('assertex', None)
    self.params = DotDict(self.params)

  def _expand_params(self, parent, key, value, global_env):
    # 文字列の場合はテンプレートとして扱い、
    # 辞書、リストの場合はさらにその中の要素を展開する。
    # ここで指定していない数値等の型はそのまま
    if isinstance(value, basestring):
      new_value = template.expand(value, global_env)
      if isinstance(key, basestring) and key.startswith('+'):
        original_key = key.lstrip('+')
        parent[original_key] = ast.literal_eval(new_value)
        del parent[key]
      else:
        parent[key] = new_value
    elif isinstance(value, dict):
      for k, v in value.items():
        self._expand_params(value, k, v, global_env)
    elif isinstance(value, list):
      for k, v in enumerate(value):
        self._expand_params(value, k, v, global_env)


