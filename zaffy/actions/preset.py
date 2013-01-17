# -*- coding: utf-8 -*-
from baseaction import BaseAction


class _PresetApplier(object):
  DEFAULT_NAME = 'default'

  def __init__(self, action_name, preset_name, is_merge):
    self.action_name = action_name
    self.preset_name = preset_name if preset_name else self.DEFAULT_NAME
    self.is_merge = is_merge

  def apply(self, action_params):
    presets = Preset.get_preset_params(self.action_name)
    if presets is None:
      return action_params
    elif self.preset_name == self.DEFAULT_NAME:
      if self.DEFAULT_NAME not in presets:
        return action_params
    elif self.preset_name not in presets:
      raise Exception("preset '" + self.action_name + "." + self.preset_name + "' is not defined")

    preset_params = dict(presets[self.preset_name])
    self.apply_params(preset_params, action_params, self.is_merge)
    return preset_params

  @staticmethod
  def apply_params(before, after, is_merge):
    for key, value in after.items():
      if key not in before or type(before[key]) is not type(value) or not is_merge:
        # preset に存在しないキー、または型が違う、または上書きモードの場合は上書き
        before[key] = value
      else:
        if isinstance(value, list):
          before[key].extend(value)
        elif isinstance(value, dict):
          before[key].update(value)
        else:
          # 数値・文字列の場合は上書き
          before[key] = value


class Preset(BaseAction):
  _presets = {}

  @classmethod
  def setup(cls, config):
    cls._presets = config

  @classmethod
  def get_preset_params(cls, action_name):
    return cls._presets.get(action_name, None)

  @classmethod
  def get_applier(cls, action_name, preset_name, is_merge):
    return _PresetApplier(action_name, preset_name, is_merge)

  @classmethod
  def reset(cls):
    cls._presets = {}

  def do_preset(self, **params):
    for target_action, presets in params.items():
      self._presets[target_action] = presets

