# -*- coding: utf-8 -*-
from baseaction import BaseAction
from actionparamsetting import ActionParamSetting

class PresetApplier(object):
  def __init__(self, action_name, preset_name, is_merge):
    self.action_name = action_name
    self.preset_name = preset_name
    self.is_merge = is_merge

  def apply(self, action_params):
    presets = Preset.get_preset_params(self.action_name)
    if presets is None:
      return action_params
    elif self.preset_name == 'default':
      if 'default' not in presets:
        return action_params
    elif self.preset_name not in presets:
      raise Exception("preset name: '" + self.preset_name + "' related to '" + self.action_name + "' action is not defined")

    preset_params = dict(presets[self.preset_name])
    self.apply_params(preset_params, action_params, self.is_merge)
    return preset_params

  @staticmethod
  def apply_params(before, after, is_merge):
    print "APPLY", before, after
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
    print "APPLIED", before


class Preset(BaseAction):
  _presets = {}

  param_setting = ActionParamSetting(
      allow_any_params=True
      )

  @classmethod
  def get_preset_params(cls, action_name):
    return cls._presets.get(action_name, None)

  @classmethod
  def get_applier(cls, action_name, preset_name, is_merge):
    return PresetApplier(action_name, preset_name, is_merge)

  @classmethod
  def reset(cls):
    cls._presets = {}

  def set_preset(self, target_action, params):
    self._presets[target_action] = params

  def _run_dynamic_method(self, global_env, scenario):
    """ オーバーライド """
    self.set_preset(self.setting._method, self.params)
